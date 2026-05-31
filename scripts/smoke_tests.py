import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from src.game import (
    Game,
    STATE_COLLECTION,
    STATE_COMPLETED,
    STATE_FINAL,
    STATE_INTRO,
    STATE_LEVEL_SELECT,
    STATE_MENU,
    STATE_PAUSED,
    STATE_PLAYING,
)
from src.levels import create_level, get_level_count
from src.settings import GRAVITY, PLAYER_JUMP_SPEED, PLAYER_SPEED


PLAYER_RECT_SIZE = (36, 56)
FRAGMENT_SUPPORT_TOLERANCE = 44
MAX_SAFE_JUMP_UP = int((PLAYER_JUMP_SPEED * PLAYER_JUMP_SPEED) / (2 * GRAVITY)) + 8
MAX_SAFE_HORIZONTAL_GAP = int(PLAYER_SPEED * 0.9)


def main() -> int:
    pygame.init()
    errors = []

    if get_level_count() != 16:
        errors.append(f"Esperado: 16 fases. Encontrado: {get_level_count()}.")

    for index in range(get_level_count()):
        level = create_level(index)
        label = f"Fase {index + 1}"

        if not level.fragments:
            errors.append(f"{label}: sem fragmentos.")
        if not level.checkpoints:
            errors.append(f"{label}: sem checkpoint.")
        if not level.hazards:
            errors.append(f"{label}: sem area de cuidado.")

        reachable_platforms = _reachable_platform_indexes(level.platforms)

        start_rect = pygame.Rect(level.start_position, PLAYER_RECT_SIZE)
        if any(start_rect.colliderect(hazard) for hazard in level.hazards):
            errors.append(f"{label}: inicio cai em area de cuidado.")

        for checkpoint in level.checkpoints:
            if any(checkpoint.colliderect(hazard) for hazard in level.hazards):
                errors.append(f"{label}: checkpoint sobre area de cuidado: {checkpoint}.")

            respawn = pygame.Rect(
                checkpoint.centerx - PLAYER_RECT_SIZE[0] // 2,
                checkpoint.bottom - PLAYER_RECT_SIZE[1],
                *PLAYER_RECT_SIZE,
            )
            if any(respawn.colliderect(hazard) for hazard in level.hazards):
                errors.append(f"{label}: respawn sobre area de cuidado: {respawn}.")

        for fragment in level.fragments:
            support_index = _find_fragment_support(fragment.rect, level.platforms)
            if support_index is None:
                errors.append(f"{label}: fragmento sem plataforma proxima: {fragment.rect}.")
            elif support_index not in reachable_platforms:
                errors.append(f"{label}: fragmento em plataforma dificil de alcancar: {fragment.rect}.")

    game = Game()
    if game.menu_image is None:
        errors.append("Abertura nao carregou a partir de abertura.png.")
    if not game.player.animations:
        errors.append("Sprite do Mig nao carregou a partir de assets/images/personagem.png.")

    save_path = ROOT / "caminhos_brasil_save.json"
    save_before = save_path.read_bytes() if save_path.exists() else None
    _check_basic_flow(game, errors)
    _check_touch_flow(Game(), errors)
    save_after = save_path.read_bytes() if save_path.exists() else None
    if save_before != save_after:
        errors.append("Fluxo de teste alterou o save local.")

    pygame.quit()

    if errors:
        print("SMOKE TESTS: FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SMOKE TESTS: OK")
    print("- 16 fases encontradas.")
    print("- Fragmentos, checkpoints e areas de cuidado existem em todas as fases.")
    print("- Checkpoints, respawns e inicio nao caem em areas de cuidado.")
    print("- Fragmentos ficam apoiados em plataformas proximas e alcancaveis.")
    print("- Game inicializa em modo dummy com abertura e sprite do Mig.")
    print("- Fluxo basico de menu, nova sessao, checkpoint, cuidado, Esc e final passa sem alterar save.")
    print("- Fluxo basico por toque cobre menu, fase, movimento, pulo, colecao e linha do tempo.")
    print("- Mensagem historica mantem posicao fixa e usa translucidez quando Mig passa por tras.")
    return 0


def _find_fragment_support(
    fragment_rect: pygame.Rect,
    platforms: list[pygame.Rect],
) -> int | None:
    for index, platform in enumerate(platforms):
        if (
            abs(fragment_rect.bottom - platform.top) <= FRAGMENT_SUPPORT_TOLERANCE
            and platform.left <= fragment_rect.centerx <= platform.right
        ):
            return index

    return None


def _reachable_platform_indexes(platforms: list[pygame.Rect]) -> set[int]:
    reachable = {0}
    changed = True

    while changed:
        changed = False
        for index, platform in enumerate(platforms):
            if index in reachable:
                continue
            if any(
                _can_reach_platform(platforms[source_index], platform)
                for source_index in reachable
            ):
                reachable.add(index)
                changed = True

    return reachable


def _can_reach_platform(source: pygame.Rect, target: pygame.Rect) -> bool:
    jump_up = source.top - target.top
    if jump_up > MAX_SAFE_JUMP_UP:
        return False

    return _horizontal_gap(source, target) <= MAX_SAFE_HORIZONTAL_GAP


def _horizontal_gap(first: pygame.Rect, second: pygame.Rect) -> int:
    if first.right < second.left:
        return second.left - first.right
    if second.right < first.left:
        return first.left - second.right
    return 0


def _check_basic_flow(game: Game, errors: list[str]):
    game._handle_keydown(pygame.K_RETURN)
    if game.state != STATE_INTRO:
        errors.append("Enter no menu nao abriu a introducao da jornada salva.")

    game._handle_keydown(pygame.K_m)
    if game.state != STATE_MENU:
        errors.append("M nao voltou ao menu a partir da introducao.")

    game._handle_keydown(pygame.K_s)
    if game.state != STATE_LEVEL_SELECT:
        errors.append("S no menu nao abriu a linha do tempo.")

    game._handle_keydown(pygame.K_m)
    game._handle_keydown(pygame.K_n)
    if not game.temporary_session:
        errors.append("N nao iniciou uma nova jornada temporaria.")
    if game.level_index != 0 or game.highest_unlocked_level != 0:
        errors.append("Nova jornada temporaria nao recomecou na fase 1.")
    if game.collection_entries:
        errors.append("Nova jornada temporaria nao limpou a colecao em memoria.")

    game._handle_keydown(pygame.K_RETURN)
    if game.state != STATE_PLAYING:
        errors.append("Enter na introducao nao iniciou a fase.")

    game.player.rect.midbottom = (300, 190)
    message_box = game._get_message_box_rect(710, 82)
    text_alpha = game._draw_message_panel(message_box)
    if message_box.topleft != (24, 126):
        errors.append("Mensagem historica mudou de posicao em vez de permanecer estavel.")
    if text_alpha >= 255:
        errors.append("Mensagem historica nao ficou translucida quando Mig passou por tras.")

    game._handle_keydown(pygame.K_c)
    if game.state != STATE_COLLECTION:
        errors.append("C nao abriu a colecao.")
    game._handle_keydown(pygame.K_c)
    if game.state != STATE_PLAYING:
        errors.append("C nao voltou da colecao para a fase.")

    checkpoint = game.level.checkpoints[0]
    game.player.rect.center = checkpoint.center
    game._update(1 / 60)
    if not game.active_checkpoints:
        errors.append("Checkpoint nao foi ativado ao tocar nele.")

    respawn_position = game.respawn_position
    hazard = game.level.hazards[0]
    game.player.rect.center = hazard.center
    game._update(1 / 60)
    if game.player.rect.topleft != respawn_position:
        errors.append("Area de cuidado nao retornou Mig ao respawn ativo.")

    game.fragments = []
    game.player.rect.center = game.level.goal.center
    game._update(1 / 60)
    if game.state != STATE_COMPLETED:
        errors.append("Portal liberado nao concluiu a fase.")

    game._handle_keydown(pygame.K_RETURN)
    if game.level_index != 1 or game.state != STATE_INTRO:
        errors.append("Enter na conclusao nao avancou para a fase seguinte.")

    game._load_level(get_level_count() - 1, STATE_PLAYING)
    game.fragments = []
    game.player.rect.center = game.level.goal.center
    game._update(1 / 60)
    game._handle_keydown(pygame.K_RETURN)
    if game.state != STATE_FINAL:
        errors.append("Ultima fase nao levou para a tela final.")

    game._load_level(1, STATE_PLAYING)
    game._handle_keydown(pygame.K_ESCAPE)
    if game.state != STATE_MENU:
        errors.append("Esc nao voltou para a tela inicial.")
    if not game.running:
        errors.append("Esc encerrou o runtime em vez de manter o jogo aberto.")


def _check_touch_flow(game: Game, errors: list[str]):
    _tap(game, game._menu_touch_actions()[0][1].center)
    if game.state != STATE_INTRO:
        errors.append("Toque em continuar no menu nao abriu a introducao.")

    _tap(game, game._intro_box_rect().center)
    if game.state != STATE_PLAYING:
        errors.append("Toque na introducao nao iniciou a fase.")

    left_rect = game._touch_control_rects()["left"]
    pointer_id = ("test", 1)
    game._handle_pointer_down(left_rect.center, pointer_id)
    game._update(1 / 60)
    if game._touch_direction() != -1 or game.player.velocity.x >= 0:
        errors.append("Botao virtual esquerdo nao moveu Mig para a esquerda.")
    game._handle_pointer_up(left_rect.center, pointer_id)
    game.player.velocity.x = 0

    right_rect = game._touch_control_rects()["right"]
    pointer_id = ("test", 2)
    game._handle_pointer_down(right_rect.center, pointer_id)
    game._update(1 / 60)
    if game._touch_direction() != 1 or game.player.velocity.x <= 0:
        errors.append("Botao virtual direito nao moveu Mig para a direita.")
    game._handle_pointer_up(right_rect.center, pointer_id)

    jump_rect = game._touch_control_rects()["jump"]
    pointer_id = ("test", 3)
    game.player.on_ground = True
    game._handle_pointer_down(jump_rect.center, pointer_id)
    game._update(1 / 60)
    if not game.player.jump_started:
        errors.append("Toque rapido em pular nao acionou o buffer de pulo.")
    game._handle_pointer_up(jump_rect.center, pointer_id)

    collection_rect = game._touch_control_rects()["collection"]
    pointer_id = ("test", 4)
    game._handle_pointer_down(collection_rect.center, pointer_id)
    game._handle_pointer_up(collection_rect.center, pointer_id)
    if game.state != STATE_COLLECTION:
        errors.append("Botao virtual C nao abriu a colecao.")
    _tap(game, game._collection_back_button_rect().center)
    if game.state != STATE_PLAYING:
        errors.append("Botao Voltar da colecao nao retornou para a fase.")

    pause_rect = game._touch_control_rects()["pause"]
    pointer_id = ("test", 5)
    game._handle_pointer_down(pause_rect.center, pointer_id)
    game._handle_pointer_up(pause_rect.center, pointer_id)
    if game.state != STATE_PAUSED:
        errors.append("Botao virtual P nao pausou a fase.")
    _tap(game, game._pause_touch_actions()[0][1].center)
    if game.state != STATE_PLAYING:
        errors.append("Toque em Continuar nao voltou da pausa para a fase.")

    game.state = STATE_MENU
    _tap(game, game._menu_touch_actions()[2][1].center)
    if game.state != STATE_LEVEL_SELECT:
        errors.append("Toque em linha do tempo no menu nao abriu a selecao de fases.")
    _tap(game, game._level_select_row_rects()[0][1].center)
    if game.state != STATE_INTRO:
        errors.append("Toque em fase liberada na linha do tempo nao abriu a introducao.")


def _tap(game: Game, position: tuple[int, int]):
    pointer_id = ("tap", position)
    game._handle_pointer_down(position, pointer_id)
    game._handle_pointer_up(position, pointer_id)


if __name__ == "__main__":
    raise SystemExit(main())
