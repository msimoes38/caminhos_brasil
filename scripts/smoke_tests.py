import json
import os
import platform
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


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
    STATE_QUIZ,
)
from src.levels import (
    create_level,
    get_active_pill_count,
    get_history_blocks,
    get_level_count,
    get_level_pill_bank,
    get_level_pill_count,
    get_stage_moment_summary,
)
from src.settings import (
    GRAVITY,
    PLAYER_COYOTE_TIME,
    PLAYER_JUMP_BUFFER_TIME,
    PLAYER_JUMP_SPEED,
    PLAYER_SPEED,
)


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
        expected_active_pills = get_active_pill_count(index)

        if get_level_pill_count(index) != 10:
            errors.append(f"{label}: banco deve ter 10 pilulas.")
        _check_pill_bank(index, label, errors)
        if len(level.fragments) != expected_active_pills:
            errors.append(
                f"{label}: esperadas {expected_active_pills} pilulas ativas. "
                f"Encontradas: {len(level.fragments)}."
            )
        if not level.checkpoints:
            errors.append(f"{label}: sem checkpoint.")
        if not level.hazards:
            errors.append(f"{label}: sem area de cuidado.")
        _check_level_quiz(level, label, errors)
        _check_quiz_uses_active_pill(level, label, errors)

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
                errors.append(f"{label}: pilula sem plataforma proxima: {fragment.rect}.")
            elif support_index not in reachable_platforms:
                errors.append(f"{label}: pilula em plataforma dificil de alcancar: {fragment.rect}.")

        mission = level.side_mission
        if not mission.title.strip() or not mission.prompt.strip() or not mission.complete_message.strip():
            errors.append(f"{label}: missao extra com texto vazio.")
        mission_support_index = _find_fragment_support(mission.rect, level.platforms)
        if mission_support_index is None:
            errors.append(f"{label}: missao extra sem plataforma proxima: {mission.rect}.")
        elif mission_support_index not in reachable_platforms:
            errors.append(f"{label}: missao extra em plataforma dificil de alcancar: {mission.rect}.")
        if any(mission.rect.colliderect(hazard) for hazard in level.hazards):
            errors.append(f"{label}: missao extra sobre area de cuidado: {mission.rect}.")
        if any(mission.rect.colliderect(fragment.rect) for fragment in level.fragments):
            errors.append(f"{label}: missao extra sobre pilula ativa: {mission.rect}.")
        if index == 1 and len(level.checkpoints) < 2:
            errors.append("Fase 2: esperados checkpoints suficientes para orientar o engenho.")

        moment = level.stage_moment
        if not moment.title.strip() or not moment.message.strip() or not moment.icon.strip():
            errors.append(f"{label}: momento observavel com texto ou icone vazio.")
        moment_support_index = _find_fragment_support(moment.rect, level.platforms)
        if moment_support_index is None:
            errors.append(f"{label}: momento observavel sem plataforma proxima: {moment.rect}.")
        elif moment_support_index not in reachable_platforms:
            errors.append(f"{label}: momento observavel em plataforma dificil de alcancar: {moment.rect}.")
        if any(moment.rect.colliderect(hazard) for hazard in level.hazards):
            errors.append(f"{label}: momento observavel sobre area de cuidado: {moment.rect}.")
        if moment.rect.colliderect(mission.rect.inflate(18, 14)):
            errors.append(f"{label}: momento observavel sobre missao extra: {moment.rect}.")
        if any(moment.rect.colliderect(fragment.rect.inflate(18, 14)) for fragment in level.fragments):
            errors.append(f"{label}: momento observavel sobre pilula ativa: {moment.rect}.")

    _check_progress_store(errors)
    _check_touch_detection(errors)
    _check_build_web_bridge_patch(errors)
    _check_history_blocks(errors)
    _check_control_tuning(errors)

    game = Game()
    if game.menu_image is None:
        errors.append("Abertura nao carregou a partir de abertura.png.")
    if not game.player.animations:
        errors.append("Sprite do Mig nao carregou a partir de assets/images/personagem.png.")
    _check_generated_sounds(game, errors)

    save_path = ROOT / "caminhos_brasil_save.json"
    save_before = save_path.read_bytes() if save_path.exists() else None
    _check_basic_flow(game, errors)
    _check_first_minute_rituals(errors)
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
    print("- Todas as fases tem banco com 10 pilulas e selecao ativa 4/5.")
    print("- Checkpoints, respawns e inicio nao caem em areas de cuidado.")
    print("- Pilulas ficam apoiadas em plataformas proximas e alcancaveis.")
    print("- Missoes extras e momentos observaveis ficam em plataformas alcancaveis e fora das areas de cuidado.")
    print("- Game inicializa em modo dummy com abertura e sprite do Mig.")
    print("- Guardiao do Portal pergunta sobre pilula ativa, aceita erro com dica e conclui com resposta correta.")
    print("- Colecao historica acumula descobertas, lembrancas da viagem e celebra album 10/10.")
    print("- ProgressStore salva/carrega no arquivo local, helper web e localStorage simulado com fallback seguro.")
    print("- Deteccao touch inicial reconhece flag JS, maxTouchPoints, matchMedia e ignora desktop simulado.")
    print("- Build limpo injeta a ponte web de touch/save e preserva o icone do manifest.")
    print("- Selos da jornada cobrem os blocos historicos sem repetir fases e com frase de contexto.")
    print("- Controles mantem pulo, coyote time e buffer em faixa suave para criancas.")
    print("- Sons gerados cobrem portal, dica do Guardiao, coleta, checkpoints e selos.")
    print("- Fluxo basico de menu, nova sessao, missao extra, checkpoint, cuidado, Esc e final passa sem alterar save.")
    print("- Ritual da primeira descoberta e do primeiro portal aparece em uma jornada limpa.")
    print("- Fluxo basico por toque cobre menu, fase, movimento, pulo, colecao, quiz e linha do tempo.")
    print("- Momentos observaveis aparecem no cenario, entram no Caderno e a colecao destaca a descoberta recente.")
    print("- Mensagem historica mantem posicao fixa e usa translucidez quando Mig passa por tras.")
    return 0


class _FakeLocalStorage:
    def __init__(self):
        self.values = {}

    def getItem(self, key: str):
        return self.values.get(key)

    def setItem(self, key: str, value: str):
        self.values[key] = value


class _FailingLocalStorage:
    def getItem(self, _key: str):
        raise RuntimeError("localStorage indisponivel")

    def setItem(self, _key: str, _value: str):
        raise RuntimeError("localStorage indisponivel")


class _FakeWebSaveHelpers:
    def __init__(self, key: str):
        self.key = key
        self.values = {}
        self.localStorage = _FailingLocalStorage()

    def caminhosReadSave(self):
        return self.values.get(self.key)

    def caminhosWriteSave(self, data: str):
        self.values[self.key] = data
        return True

    def caminhosClearSave(self):
        self.values.pop(self.key, None)
        return True


class _FakeMediaQuery:
    def __init__(self, matches: bool):
        self.matches = matches


class _FakeNavigator:
    def __init__(
        self,
        max_touch_points: int = 0,
        ms_max_touch_points: int = 0,
        user_agent: str = "Mozilla/5.0 desktop",
    ):
        self.maxTouchPoints = max_touch_points
        self.msMaxTouchPoints = ms_max_touch_points
        self.userAgent = user_agent


class _FakeBrowserWindow:
    def __init__(
        self,
        navigator: _FakeNavigator | None = None,
        matching_queries: set[str] | None = None,
        touch_start: bool = False,
        touch_context=None,
    ):
        self.navigator = navigator or _FakeNavigator()
        self.matching_queries = matching_queries or set()
        if touch_context is not None:
            self.caminhosTouchContext = touch_context
        if touch_start:
            self.ontouchstart = None

    def matchMedia(self, query: str):
        return _FakeMediaQuery(query in self.matching_queries)

    def __contains__(self, item: str) -> bool:
        return item == "ontouchstart" and hasattr(self, "ontouchstart")


def _check_touch_detection(errors: list[str]):
    missing_window = object()
    original_window = getattr(platform, "window", missing_window)
    detector = Game.__new__(Game)

    try:
        platform.window = _FakeBrowserWindow(touch_context=True)
        if not detector._detect_touch_context():
            errors.append("Deteccao touch nao reconheceu window.caminhosTouchContext.")

        platform.window = _FakeBrowserWindow(
            navigator=_FakeNavigator(max_touch_points=1),
            touch_context=False,
        )
        if detector._detect_touch_context():
            errors.append("Deteccao touch nao priorizou window.caminhosTouchContext falso.")

        platform.window = _FakeBrowserWindow(
            navigator=_FakeNavigator(max_touch_points=1),
        )
        if not detector._detect_touch_context():
            errors.append("Deteccao touch nao reconheceu navigator.maxTouchPoints.")

        platform.window = _FakeBrowserWindow(
            matching_queries={"(pointer: coarse)"},
        )
        if not detector._detect_touch_context():
            errors.append("Deteccao touch nao reconheceu matchMedia pointer coarse.")

        platform.window = _FakeBrowserWindow(
            matching_queries={"(hover: none)"},
        )
        if not detector._detect_touch_context():
            errors.append("Deteccao touch nao reconheceu matchMedia hover none.")

        platform.window = _FakeBrowserWindow(touch_start=True)
        if not detector._detect_touch_context():
            errors.append("Deteccao touch nao reconheceu ontouchstart.")

        platform.window = _FakeBrowserWindow(
            navigator=_FakeNavigator(user_agent="Mozilla/5.0 desktop"),
        )
        if detector._detect_touch_context():
            errors.append("Deteccao touch marcou desktop simulado como touch.")

        detector.state = STATE_MENU
        detector.touch_ui_enabled = False
        detector.keyboard_input_seen = False
        platform.window = _FakeBrowserWindow(touch_context=True)
        detector._refresh_late_touch_context()
        if not detector.touch_ui_enabled:
            errors.append("Rechecagem tardia no menu nao ativou layout touch.")
    finally:
        if original_window is missing_window:
            if hasattr(platform, "window"):
                delattr(platform, "window")
        else:
            platform.window = original_window


def _check_progress_store(errors: list[str]):
    import src.progress as progress_module

    original_save_path = progress_module.SAVE_PATH
    missing_window = object()
    original_window = getattr(platform, "window", missing_window)

    try:
        with TemporaryDirectory() as temp_dir:
            progress_module.SAVE_PATH = Path(temp_dir) / "save.json"
            if hasattr(platform, "window"):
                delattr(platform, "window")

            store = progress_module.ProgressStore(4)
            store.save(3, [("Fase", "Info")], {1, 8})
            loaded = store.load()
            if loaded["highest_unlocked_level"] != 3:
                errors.append("ProgressStore local nao preservou maior fase desbloqueada.")
            if loaded["completed_levels"] != {1}:
                errors.append("ProgressStore local nao filtrou fases concluidas invalidas.")
            if loaded["collection_entries"] != [("Fase", "Info")]:
                errors.append("ProgressStore local nao preservou a colecao em formato valido.")

            progress_module.SAVE_PATH.write_text(
                json.dumps(
                    {
                        "highest_unlocked_level": 99,
                        "completed_levels": [0, "x", 3, 9],
                        "collection_entries": [
                            ["Fase", "Info"],
                            ["Fase", "Info"],
                            ["incompleta"],
                            [12, "ruim"],
                        ],
                    }
                ),
                encoding="utf-8",
            )
            loaded = store.load()
            if loaded["highest_unlocked_level"] != 3:
                errors.append("ProgressStore local nao limitou maior fase ao total de fases.")
            if loaded["completed_levels"] != {0, 3}:
                errors.append("ProgressStore local nao normalizou completed_levels.")
            if loaded["collection_entries"] != [("Fase", "Info")]:
                errors.append("ProgressStore local nao removeu entradas ruins ou duplicadas.")

            helper_window = _FakeWebSaveHelpers(progress_module.WEB_SAVE_KEY)
            platform.window = helper_window
            store.save(1, [("Helper", "Pill")], {0, 1})
            if progress_module.WEB_SAVE_KEY not in helper_window.values:
                errors.append("ProgressStore web nao gravou usando helper JS.")
            loaded = store.load()
            if loaded["highest_unlocked_level"] != 1 or loaded["completed_levels"] != {0, 1}:
                errors.append("ProgressStore web nao carregou progresso salvo via helper JS.")
            if loaded["collection_entries"] != [("Helper", "Pill")]:
                errors.append("ProgressStore web nao carregou colecao salva via helper JS.")

            storage = _FakeLocalStorage()
            platform.window = type("Window", (), {"localStorage": storage})()
            store.save(2, [("Web", "Pill")], {0, 2})
            if progress_module.WEB_SAVE_KEY not in storage.values:
                errors.append("ProgressStore web nao gravou na chave esperada do localStorage.")
            loaded = store.load()
            if loaded["highest_unlocked_level"] != 2 or loaded["completed_levels"] != {0, 2}:
                errors.append("ProgressStore web nao carregou progresso salvo no localStorage.")
            if loaded["collection_entries"] != [("Web", "Pill")]:
                errors.append("ProgressStore web nao carregou colecao salva no localStorage.")

            storage.values[progress_module.WEB_SAVE_KEY] = json.dumps(
                {
                    "highest_unlocked_level": 7,
                    "completed_levels": [1, "ruim", 2],
                    "collection_entries": [
                        ["Web", "Pill"],
                        ["Web", "Pill"],
                        ["ruim"],
                    ],
                }
            )
            loaded = store.load()
            if loaded["highest_unlocked_level"] != 3:
                errors.append("ProgressStore web nao limitou maior fase ao total de fases.")
            if loaded["completed_levels"] != {1, 2}:
                errors.append("ProgressStore web nao filtrou completed_levels invalidos.")
            if loaded["collection_entries"] != [("Web", "Pill")]:
                errors.append("ProgressStore web nao removeu entradas ruins ou duplicadas.")

            platform.window = type("Window", (), {"localStorage": _FailingLocalStorage()})()
            try:
                store.save(1, [("Fallback", "Ok")], {1})
                loaded = store.load()
            except Exception as exc:
                errors.append(f"ProgressStore quebrou quando localStorage falhou: {exc}.")
            else:
                if not isinstance(loaded["collection_entries"], list):
                    errors.append("ProgressStore com localStorage falhando retornou formato invalido.")
    finally:
        progress_module.SAVE_PATH = original_save_path
        if original_window is missing_window:
            if hasattr(platform, "window"):
                delattr(platform, "window")
        else:
            platform.window = original_window


def _check_build_web_bridge_patch(errors: list[str]):
    import scripts.build_pygbag_clean as build_script

    with TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        index_path = temp_root / "web" / "index.html"
        index_path.parent.mkdir()
        index_path.write_text(
            "<html><head><style></style></head><body></body></html>",
            encoding="utf-8",
        )
        if not build_script.patch_web_bridge(index_path):
            errors.append("Patch da ponte web touch/save falhou em index.html valido.")
            return

        html = index_path.read_text(encoding="utf-8")
        expected_markers = (
            "window.caminhosTouchContext",
            "window.caminhosReadSave",
            "window.caminhosWriteSave",
            "window.caminhosClearSave",
            "caminhos_brasil_save_v1",
        )
        for marker in expected_markers:
            if marker not in html:
                errors.append(f"Patch da ponte web nao inseriu marcador {marker}.")

        if not build_script.patch_web_bridge(index_path):
            errors.append("Patch da ponte web nao foi idempotente.")
        html_after_second_patch = index_path.read_text(encoding="utf-8")
        if html_after_second_patch != html:
            errors.append("Patch da ponte web duplicou conteudo ao rodar novamente.")

        original_staging_dir = build_script.STAGING_DIR
        staging_dir = temp_root / "staging"
        staging_dir.mkdir()
        (staging_dir / "abertura.png").write_bytes(b"fake-icon")
        build_script.STAGING_DIR = staging_dir
        try:
            if not build_script.patch_web_app_metadata(index_path):
                errors.append("Patch de metadados web falhou em index.html valido.")
            if not (index_path.parent / "manifest.webmanifest").exists():
                errors.append("Patch de metadados web nao criou manifest.webmanifest.")
            if not (index_path.parent / "abertura.png").exists():
                errors.append("Patch de metadados web nao copiou abertura.png para o build final.")
        finally:
            build_script.STAGING_DIR = original_staging_dir


def _check_pill_bank(index: int, label: str, errors: list[str]):
    bank = get_level_pill_bank(index)
    seen_infos = set()

    for pill_index, pill in enumerate(bank):
        pill_label = f"{label}, pilula {pill_index + 1}"
        if not pill.info.strip():
            errors.append(f"{pill_label}: texto vazio.")
        if not pill.question.strip():
            errors.append(f"{pill_label}: pergunta vazia.")
        if len(pill.options) != 3:
            errors.append(f"{pill_label}: deve ter 3 alternativas.")
        elif any(not option.strip() for option in pill.options):
            errors.append(f"{pill_label}: alternativa vazia.")
        if not 0 <= pill.correct_index < len(pill.options):
            errors.append(f"{pill_label}: indice correto fora do intervalo.")
        if not pill.hint.strip():
            errors.append(f"{pill_label}: dica vazia.")
        if pill.info in seen_infos:
            errors.append(f"{pill_label}: texto duplicado no banco.")
        seen_infos.add(pill.info)


def _check_level_quiz(level, label: str, errors: list[str]):
    quiz = level.quiz
    if quiz is None:
        errors.append(f"{label}: sem quiz do Guardiao do Portal.")
        return

    if not quiz.question.strip():
        errors.append(f"{label}: pergunta do quiz vazia.")
    if len(quiz.options) != 3:
        errors.append(f"{label}: quiz deve ter 3 alternativas.")
    elif any(not option.strip() for option in quiz.options):
        errors.append(f"{label}: alternativa vazia no quiz.")
    if not 0 <= quiz.correct_index < len(quiz.options):
        errors.append(f"{label}: indice correto do quiz fora do intervalo.")
    if not quiz.hint.strip():
        errors.append(f"{label}: dica do quiz vazia.")


def _check_quiz_uses_active_pill(level, label: str, errors: list[str]):
    if level.quiz is None:
        return
    if level.quiz_pill_index not in level.active_pill_indexes:
        errors.append(f"{label}: quiz nao veio de uma pilula ativa.")
        return
    active_questions = {fragment.quiz.question for fragment in level.fragments}
    if level.quiz.question not in active_questions:
        errors.append(f"{label}: quiz nao corresponde as pilulas ativas.")


def _check_history_blocks(errors: list[str]):
    blocks = get_history_blocks()
    if len(blocks) != 5:
        errors.append(f"Selos da jornada: esperados 5 blocos. Encontrados: {len(blocks)}.")

    covered_levels = []
    for block in blocks:
        if not block.name.strip() or not block.short_label.strip():
            errors.append("Selos da jornada: bloco com nome ou rotulo vazio.")
        if not block.phrase.strip():
            errors.append(f"Selos da jornada: bloco {block.name} sem frase de contexto.")
        if not block.level_indexes:
            errors.append(f"Selos da jornada: bloco {block.name} nao tem fases.")
        covered_levels.extend(block.level_indexes)

    expected_levels = list(range(get_level_count()))
    if sorted(covered_levels) != expected_levels:
        errors.append("Selos da jornada nao cobrem todas as fases em ordem valida.")
    if len(set(covered_levels)) != len(covered_levels):
        errors.append("Selos da jornada repetem alguma fase em mais de um bloco.")


def _check_control_tuning(errors: list[str]):
    if not 640 <= PLAYER_JUMP_SPEED <= 660:
        errors.append("Ajuste de pulo saiu da faixa suave esperada.")
    if not 0.16 <= PLAYER_COYOTE_TIME <= 0.2:
        errors.append("Coyote time saiu da faixa esperada para perdao no pulo.")
    if not 0.18 <= PLAYER_JUMP_BUFFER_TIME <= 0.22:
        errors.append("Buffer de pulo saiu da faixa esperada para toque/teclado.")


def _check_generated_sounds(game: Game, errors: list[str]):
    if not game.sounds.enabled:
        return

    for key in ("collect", "checkpoint", "correct", "portal", "hint", "seal"):
        if key not in game.sounds.sounds:
            errors.append(f"Som gerado ausente: {key}.")


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
    saved_collection_count = len(game.collection_entries)
    game._handle_keydown(pygame.K_n)
    if not game.temporary_session:
        errors.append("N nao iniciou uma nova jornada temporaria.")
    if game.level_index != 0 or game.highest_unlocked_level != 0:
        errors.append("Nova jornada temporaria nao recomecou na fase 1.")
    if len(game.collection_entries) != saved_collection_count:
        errors.append("Nova jornada temporaria alterou a colecao acumulativa em memoria.")
    if not game.level.active_pill_indexes or game.level.quiz_pill_index not in game.level.active_pill_indexes:
        errors.append("Nova jornada temporaria nao sorteou pilulas ativas validas.")
    session_pill_choices = game.level.active_pill_indexes
    session_quiz_choice = game.level.quiz_pill_index
    game._load_level(0, STATE_INTRO)
    if game.level.active_pill_indexes != session_pill_choices:
        errors.append("Voltar para a mesma fase mudou as pilulas da sessao.")
    if game.level.quiz_pill_index != session_quiz_choice:
        errors.append("Voltar para a mesma fase mudou a pergunta da sessao.")

    collection_before = len(game.collection_entries)
    first_info = game.level.fragments[0].info
    entry = (game.level.title, first_info)
    expected_collection_count = collection_before + (0 if entry in game.collection_entry_set else 1)
    game._add_collection_entry(first_info)
    game._add_collection_entry(first_info)
    if len(game.collection_entries) != expected_collection_count:
        errors.append("Colecao historica duplicou uma pilula ja descoberta.")
    for pill in get_level_pill_bank(0):
        game._add_collection_entry(pill.info)
    if not any(
        row_type == "header" and "completo" in text
        for row_type, text in game._collection_rows()
    ):
        errors.append("Colecao nao destaca album completo ao reunir 10 descobertas.")
    if game.recent_collection_entry is None:
        game.recent_collection_entry = (game.level.title, first_info)
    recent_info = game.recent_collection_entry[1]
    if not any(row_type == "favorite_header" for row_type, _text in game._collection_rows()):
        errors.append("Colecao nao destaca a descoberta recente da jornada.")
    if not any(row_type == "favorite_item" and recent_info in text for row_type, text in game._collection_rows()):
        errors.append("Colecao nao mostra a pilula recente em card proprio.")

    game._handle_keydown(pygame.K_RETURN)
    if game.state != STATE_PLAYING:
        errors.append("Enter na introducao nao iniciou a fase.")
    if "andar" not in (game._tutorial_hint_text() or ""):
        errors.append("Tutorial inicial nao orientou movimento enquanto a acao nao foi feita.")

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
    rows = game._collection_rows()
    expected_counter = f"/{get_level_pill_count(0)} descobertas"
    if not any(row_type == "header" and expected_counter in text for row_type, text in rows):
        errors.append("Colecao nao mostra contador baseado no banco completo da fase.")
    if len(rows) > game._collection_visible_rows():
        previous_scroll = game.collection_scroll
        game._handle_keydown(pygame.K_DOWN)
        if game.collection_scroll <= previous_scroll:
            errors.append("Colecao nao rolou com seta para baixo.")
    game._handle_keydown(pygame.K_c)
    if game.state != STATE_PLAYING:
        errors.append("C nao voltou da colecao para a fase.")

    mission = game.level.side_mission
    mission_count_before = len(game.side_missions_completed)
    game.player.velocity.update(0, 0)
    game.player.rect.center = mission.rect.center
    game._update(0)
    if not game.side_mission_completed or game.level_index not in game.side_missions_completed:
        errors.append("Missao extra nao foi concluida ao tocar no marcador.")
    if len(game.side_missions_completed) != mission_count_before + 1:
        errors.append("Missao extra nao atualizou o contador da sessao.")
    if not game.feedback_message:
        errors.append("Missao extra nao mostrou feedback positivo.")
    memory_rows = game._collection_rows()
    if not any(
        row_type == "memory_header" and "Lembranças da viagem" in text
        for row_type, text in memory_rows
    ):
        errors.append("Colecao nao mostra a secao de lembrancas da viagem.")
    if not any(
        row_type == "memory_item" and mission.complete_message in text
        for row_type, text in memory_rows
    ):
        errors.append("Colecao nao mostra a missao extra observada como lembranca.")

    moment = game.level.stage_moment
    _trigger_x, micro_message, _micro_color = game._micro_event_data()
    game.feedback_message = ""
    game.feedback_message_timer = 0
    game.fragment_message = ""
    game.fragment_message_timer = 0
    game.player.rect.center = moment.rect.center
    game._update_micro_event()
    if game.level_index not in game.micro_events_seen:
        errors.append("Momento observavel da fase nao foi registrado ao tocar no objeto.")
    if game.feedback_message != micro_message:
        errors.append("Momento observavel da fase nao mostrou a mensagem contextual esperada.")
    moment_title, moment_message = get_stage_moment_summary(game.level_index)
    if moment_message != micro_message:
        errors.append("Resumo do momento observavel nao corresponde ao dado da fase.")
    moment_rows = game._collection_rows()
    if not any(row_type == "memory_item" and moment_title in text for row_type, text in moment_rows):
        errors.append("Colecao nao mostra momento observavel como lembranca da viagem.")
    if not game.recent_collection_entry or game.recent_collection_entry[0] != "Lembrança da viagem":
        errors.append("Momento observavel nao virou lembranca recente no Caderno.")
    if not any(
        row_type == "favorite_item" and moment_title in text and "memory_item" not in text
        for row_type, text in moment_rows
    ):
        errors.append("Caderno nao destaca momento observavel recente com texto legivel.")

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
    if game.state != STATE_QUIZ:
        errors.append("Portal liberado nao abriu o Guardiao do Portal.")
    elif game.level.quiz_pill_index not in game.level.active_pill_indexes:
        errors.append("Guardiao do Portal perguntou sobre pilula fora da jogada.")
    if not game._guardian_intro_text():
        errors.append("Guardiao do Portal nao gerou texto de contexto.")
    if not game._guardian_focus_text().startswith(("Lembre da", "A pergunta")):
        errors.append("Guardiao do Portal nao mostrou foco na pilula usada pela pergunta.")

    quiz = game.level.quiz
    wrong_index = (quiz.correct_index + 1) % len(quiz.options)
    game._submit_quiz_answer(wrong_index)
    if game.state != STATE_QUIZ:
        errors.append("Resposta errada no quiz nao manteve a fase no Guardiao do Portal.")
    if not game.quiz_feedback:
        errors.append("Resposta errada no quiz nao mostrou dica.")
    if "aprendendo" not in game.quiz_feedback:
        errors.append("Resposta errada no quiz nao manteve tom acolhedor.")

    game._submit_quiz_answer(quiz.correct_index)
    if game.state != STATE_COMPLETED:
        errors.append("Resposta correta no quiz nao concluiu a fase.")
    first_block, first_block_completed, first_block_total, first_block_earned = game._history_block_progress()[0]
    if not first_block_earned or first_block_completed != first_block_total:
        errors.append(f"Selo {first_block.name} nao foi conquistado ao concluir a fase 1.")
    if game.recent_history_block_seal != first_block.name:
        errors.append("Tela de conclusao nao registrou o selo recem-conquistado.")

    game._handle_keydown(pygame.K_RETURN)
    if game.level_index != 1 or game.state != STATE_INTRO:
        errors.append("Enter na conclusao nao avancou para a fase seguinte.")

    game._load_level(get_level_count() - 1, STATE_PLAYING)
    game.fragments = []
    game.player.rect.center = game.level.goal.center
    game._update(1 / 60)
    if game.state != STATE_QUIZ:
        errors.append("Ultima fase nao abriu o Guardiao do Portal antes do final.")
    game._submit_quiz_answer(game.level.quiz.correct_index)
    game._handle_keydown(pygame.K_RETURN)
    if game.state != STATE_FINAL:
        errors.append("Ultima fase nao levou para a tela final.")
    final_memory_lines = game._final_memory_recap_lines()
    if not any("guardadas no Caderno" in line for line in final_memory_lines):
        errors.append("Tela final nao resume lembrancas guardadas no Caderno.")
    if not any(moment_title in line for line in final_memory_lines):
        errors.append("Tela final nao relembra momento observavel marcante.")

    game._load_level(1, STATE_PLAYING)
    game._handle_keydown(pygame.K_ESCAPE)
    if game.state != STATE_MENU:
        errors.append("Esc nao voltou para a tela inicial.")
    if not game.running:
        errors.append("Esc encerrou o runtime em vez de manter o jogo aberto.")


def _check_first_minute_rituals(errors: list[str]):
    game = Game()
    game.temporary_session = True
    game.collection_entries = []
    game.collection_entry_set = set()
    game.completed_levels = set()
    game.session_discovery_count = 0
    game.first_discovery_ritual_seen = False
    game.first_portal_ritual_seen = False
    game._load_level(0, STATE_PLAYING)

    first_fragment = game.fragments[0]
    game.player.rect.center = first_fragment.rect.center
    game._collect_fragments()
    if not game.first_discovery_ritual_seen:
        errors.append("Primeira pilula da jornada limpa nao marcou o ritual de descoberta.")
    if not game.fragment_message.startswith("Primeira descoberta!"):
        errors.append("Primeira pilula da jornada limpa nao mostrou mensagem especial.")
    if not game.effects:
        errors.append("Primeira pilula da jornada limpa nao gerou particulas especiais.")

    game.fragments = []
    game._open_quiz_or_complete()
    if game.state != STATE_QUIZ:
        errors.append("Primeiro portal da jornada limpa nao abriu o Guardiao.")
    if not game.first_portal_ritual_seen:
        errors.append("Primeiro portal da jornada limpa nao marcou o ritual especial.")
    if "primeiro portal" not in game.guardian_ritual_message.lower():
        errors.append("Primeiro portal da jornada limpa nao mostrou fala especial do Guardiao.")


def _check_touch_flow(game: Game, errors: list[str]):
    game.temporary_session = True

    _tap(game, game._menu_touch_actions()[0][1].center)
    if game.state != STATE_INTRO:
        errors.append("Toque em continuar no menu nao abriu a introducao.")

    _tap(game, game._intro_box_rect().center)
    if game.state != STATE_PLAYING:
        errors.append("Toque na introducao nao iniciou a fase.")

    left_rect = game._touch_control_rects()["left"]
    if left_rect.colliderect(game._get_player_screen_rect()):
        errors.append("Botao virtual esquerdo cobre o Mig no inicio da fase.")

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
    if game._gameplay_touch_action_at((jump_rect.left - 6, jump_rect.centery)) != "jump":
        errors.append("Area de toque do pulo nao aceita margem proxima ao botao.")
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

    game.fragments = []
    game.player.rect.center = game.level.goal.center
    game._update(1 / 60)
    if game.state != STATE_QUIZ:
        errors.append("Toque no portal liberado nao abriu o Guardiao do Portal.")
    else:
        quiz = game.level.quiz
        wrong_index = (quiz.correct_index + 1) % len(quiz.options)
        _tap(game, game._quiz_option_rects()[wrong_index].center)
        if game.state != STATE_QUIZ:
            errors.append("Toque em alternativa errada nao manteve o quiz aberto.")
        _tap(game, game._quiz_option_rects()[quiz.correct_index].center)
        if game.state != STATE_COMPLETED:
            errors.append("Toque em alternativa correta nao concluiu a fase.")

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
