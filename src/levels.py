from dataclasses import dataclass

import pygame

from src.level_data import LEVELS, KnowledgePill, QuizData


@dataclass(frozen=True)
class Fragment:
    rect: pygame.Rect
    info: str
    pill_index: int
    quiz: QuizData


@dataclass(frozen=True)
class SideMission:
    rect: pygame.Rect
    title: str
    prompt: str
    complete_message: str
    icon: str


@dataclass(frozen=True)
class StageMoment:
    rect: pygame.Rect
    title: str
    message: str
    icon: str
    color: tuple[int, int, int]


@dataclass(frozen=True)
class Level:
    title: str
    year: str
    mission: str
    historical_note: str
    intro_text: str
    theme: str
    width: int
    start_position: tuple[int, int]
    platforms: list[pygame.Rect]
    goal: pygame.Rect
    fragments: list[Fragment]
    hazards: list[pygame.Rect]
    checkpoints: list[pygame.Rect]
    quiz: QuizData | None
    active_pill_indexes: tuple[int, ...]
    quiz_pill_index: int | None
    side_mission: SideMission
    stage_moment: StageMoment


@dataclass(frozen=True)
class HistoryBlock:
    name: str
    short_label: str
    level_indexes: tuple[int, ...]
    phrase: str


HISTORY_BLOCKS = (
    HistoryBlock("Primeiros contatos", "1", (0,), "Muitos povos já viviam aqui."),
    HistoryBlock("Brasil colonial", "C", (1, 2, 3, 4, 5), "Trabalho, caminhos e poder mudaram o território."),
    HistoryBlock("Independência e Império", "I", (6, 7, 8), "O país mudou de forma, mas muitos desafios continuaram."),
    HistoryBlock("República e democracia", "R", (9, 10, 11, 12, 13, 14), "Participação, direitos e memória ajudam a cuidar do Brasil."),
    HistoryBlock("Brasil de hoje", "H", (15,), "A história continua com cidadania, diversidade e futuro."),
)


SIDE_MISSION_DATA = (
    ("Observe o marco do litoral", "Encontre o marco de memória perto da praia.", "Marco observado! A memória começa pelos povos que já viviam aqui.", "marker"),
    ("Ative a placa do engenho", "Procure a placa de cuidado no caminho da cana.", "Placa ativada! Trabalho e respeito caminham juntos nesta fase.", "sign"),
    ("Encontre o mapa das trilhas", "Toque no mapa antigo das rotas do interior.", "Mapa encontrado! Rios e trilhas guardam muitos saberes.", "map"),
    ("Acenda a lanterna das minas", "Procure uma lanterna segura entre as montanhas.", "Lanterna acesa! Ela ajuda Mig a observar as mudanças das vilas.", "lamp"),
    ("Leia a carta de ideias", "Encontre uma carta na praça colonial.", "Carta lida! Ideias também fazem parte da história.", "letter"),
    ("Visite a biblioteca da corte", "Procure o pequeno livro perto da cidade.", "Livro visitado! Conhecimento circulou por novos espaços.", "book"),
    ("Observe o marco da mudança", "Toque no símbolo da independência.", "Marco observado! Mudanças políticas pedem perguntas e cuidado.", "flag"),
    ("Registre o jardim imperial", "Encontre o selo do jardim.", "Jardim registrado! O Império teve diferenças e continuidades.", "garden"),
    ("Guarde a memória da liberdade", "Procure o símbolo de memória e dignidade.", "Memória guardada! Liberdade e dignidade merecem respeito.", "memory"),
    ("Toque o sino da praça", "Encontre o pequeno sino republicano.", "Sino tocado! A República trouxe novas disputas e escolhas.", "bell"),
    ("Confira os trilhos do café", "Procure a placa dos caminhos do café.", "Trilhos conferidos! Economia e política marcaram esse período.", "rails"),
    ("Sintonize o rádio da cidade", "Encontre o rádio da Era Vargas.", "Rádio sintonizado! Comunicação também conta história.", "radio"),
    ("Leia o cartaz da participação", "Procure o cartaz cívico da praça.", "Cartaz lido! Democracia precisa de diálogo e respeito.", "poster"),
    ("Acenda a luz da memória", "Encontre uma luz de cuidado no caminho.", "Luz acesa! Memória ajuda a valorizar direitos.", "light"),
    ("Abra o livro cidadão", "Procure o livro da Constituição.", "Livro aberto! Direitos são construídos com participação.", "constitution"),
    ("Conecte o presente", "Encontre o símbolo de conexão do Brasil de hoje.", "Conexão feita! O presente também faz parte da história.", "connection"),
)


STAGE_MOMENT_DATA = (
    ("Brisa do litoral", "Uma brisa passa pelo marco e lembra que muitos povos ja viviam aqui.", "shell", (126, 198, 214)),
    ("Roda do engenho", "A roda gira devagar. Trabalho e cuidado precisam ser lembrados juntos.", "wheel", (124, 184, 92)),
    ("Mapa das trilhas", "O mapa mostra rios e caminhos conhecidos por muita gente antes das novas rotas.", "map", (226, 202, 128)),
    ("Lanterna das minas", "A lanterna ilumina vilas que cresceram com mudancas e desafios.", "lamp", (218, 196, 118)),
    ("Carta na praca", "A carta lembra que ideias podem inspirar perguntas sobre o futuro.", "letter", (226, 202, 128)),
    ("Livro da corte", "O livro aberto mostra que conhecimento tambem circula pela cidade.", "book", (204, 222, 236)),
    ("Marco da mudanca", "O marco convida Mig a observar escolhas politicas com cuidado.", "flag", (126, 176, 92)),
    ("Luz do jardim", "A luz do jardim ajuda a notar continuidades e diferencas.", "garden", (248, 220, 116)),
    ("Memoria da liberdade", "A luz suave lembra dignidade, liberdade e respeito.", "memory", (238, 232, 210)),
    ("Sino da praca", "O sino marca novas disputas, escolhas e participacao.", "bell", (226, 168, 74)),
    ("Trilhos do cafe", "Os trilhos mostram como economia e politica se cruzaram.", "rails", (156, 118, 72)),
    ("Radio da cidade", "O radio leva noticias e mostra a forca da comunicacao.", "radio", (170, 180, 178)),
    ("Cartaz do dialogo", "O cartaz lembra que democracia precisa de conversa e respeito.", "poster", (190, 206, 146)),
    ("Luz da memoria", "A luz acesa ajuda a lembrar direitos e democracia.", "light", (238, 232, 210)),
    ("Livro cidadao", "O livro aberto fala de direitos construidos com participacao.", "constitution", (82, 150, 214)),
    ("Conexao do presente", "A conexao acende: o presente tambem faz parte da historia.", "connection", (82, 150, 214)),
)


def get_level_count() -> int:
    return len(LEVELS)


def get_history_blocks() -> tuple[HistoryBlock, ...]:
    return HISTORY_BLOCKS


def get_level_title(index: int) -> str:
    data = LEVELS[index]
    return f"{data.year} - {data.title}"


def get_level_plain_title(index: int) -> str:
    return LEVELS[index].title


def get_level_fragment_count(index: int) -> int:
    return len(LEVELS[index].pill_bank)


def get_total_fragment_count() -> int:
    return sum(len(level.pill_bank) for level in LEVELS)


def get_level_pill_count(index: int) -> int:
    return len(LEVELS[index].pill_bank)


def get_level_pill_infos(index: int) -> list[str]:
    return [pill.info for pill in LEVELS[index].pill_bank]


def get_level_pill_bank(index: int) -> tuple[KnowledgePill, ...]:
    return tuple(LEVELS[index].pill_bank)


def get_side_mission_summary(index: int) -> tuple[str, str]:
    title, _prompt, complete_message, _icon = SIDE_MISSION_DATA[index]
    return title, complete_message


def get_stage_moment_summary(index: int) -> tuple[str, str]:
    title, message, _icon, _color = STAGE_MOMENT_DATA[index]
    return title, message


def get_active_pill_count(index: int) -> int:
    return 4 if index == 0 else 5


def create_level(
    index: int,
    active_pill_indexes: tuple[int, ...] | None = None,
    quiz_pill_index: int | None = None,
) -> Level:
    data = LEVELS[index]
    if active_pill_indexes is None:
        active_pill_indexes = tuple(range(get_active_pill_count(index)))
    active_pill_indexes = tuple(
        pill_index
        for pill_index in active_pill_indexes
        if 0 <= pill_index < len(data.pill_bank)
    )
    if not active_pill_indexes:
        active_pill_indexes = (0,)

    if quiz_pill_index not in active_pill_indexes:
        quiz_pill_index = active_pill_indexes[0]

    platforms = [pygame.Rect(platform) for platform in data.platforms]
    fragments = _fragments_from_pills(platforms, data.pill_bank, active_pill_indexes, index)
    side_mission = _side_mission_for_level(platforms, fragments, index)
    stage_moment = _stage_moment_for_level(platforms, fragments, side_mission, index)
    return Level(
        title=data.title,
        year=data.year,
        mission=data.mission,
        historical_note=data.historical_note,
        intro_text=data.intro_text,
        theme=data.theme,
        width=data.width,
        start_position=data.start_position,
        platforms=platforms,
        goal=pygame.Rect(data.goal),
        fragments=fragments,
        hazards=[pygame.Rect(hazard) for hazard in data.hazards],
        checkpoints=[pygame.Rect(checkpoint) for checkpoint in data.checkpoints],
        quiz=_quiz_for_pill(data.pill_bank[quiz_pill_index], index, quiz_pill_index),
        active_pill_indexes=active_pill_indexes,
        quiz_pill_index=quiz_pill_index,
        side_mission=side_mission,
        stage_moment=stage_moment,
    )


def _fragments_from_pills(
    platforms: list[pygame.Rect],
    pill_bank: list[KnowledgePill],
    active_pill_indexes: tuple[int, ...],
    level_index: int,
) -> list[Fragment]:
    usable_platforms = platforms[1:]
    selected_platforms = _distributed_platforms(usable_platforms, len(active_pill_indexes))
    fragments = []

    for order, pill_index in enumerate(active_pill_indexes):
        platform = selected_platforms[order]
        pill = pill_bank[pill_index]
        fragments.append(
            Fragment(
                rect=pygame.Rect(platform.centerx - 12, platform.top - 40, 24, 24),
                info=pill.info,
                pill_index=pill_index,
                quiz=_quiz_for_pill(pill, level_index, pill_index),
            )
        )

    return fragments


def _distributed_platforms(platforms: list[pygame.Rect], count: int) -> list[pygame.Rect]:
    if count <= 0:
        return []
    if not platforms:
        return [pygame.Rect(120 + index * 64, 392, 120, 28) for index in range(count)]
    if count == 1:
        return [platforms[min(len(platforms) - 1, len(platforms) // 2)]]
    if count >= len(platforms):
        return platforms[:count]

    last_index = len(platforms) - 1
    chosen_indexes = []
    used_indexes = set()
    for order in range(count):
        desired = round(order * last_index / (count - 1))
        chosen = _nearest_unused_platform_index(desired, last_index, used_indexes)
        used_indexes.add(chosen)
        chosen_indexes.append(chosen)

    chosen_indexes.sort()
    return [platforms[index] for index in chosen_indexes]


def _nearest_unused_platform_index(
    desired: int,
    last_index: int,
    used_indexes: set[int],
) -> int:
    if desired not in used_indexes:
        return desired

    for distance in range(1, last_index + 1):
        left = desired - distance
        if left >= 0 and left not in used_indexes:
            return left
        right = desired + distance
        if right <= last_index and right not in used_indexes:
            return right

    return desired


def _side_mission_for_level(
    platforms: list[pygame.Rect],
    fragments: list[Fragment],
    level_index: int,
) -> SideMission:
    title, prompt, complete_message, icon = SIDE_MISSION_DATA[level_index]
    usable_platforms = platforms[1:]
    if usable_platforms:
        preferred_index = min(len(usable_platforms) - 1, 1 + (level_index % 3))
        platform_order = [usable_platforms[preferred_index]] + [
            platform
            for index, platform in enumerate(usable_platforms)
            if index != preferred_index
        ]
        rect = _free_side_mission_rect(platform_order, fragments, level_index)
    else:
        rect = pygame.Rect(220 + level_index * 12, 356, 36, 36)

    return SideMission(
        rect=rect,
        title=title,
        prompt=prompt,
        complete_message=complete_message,
        icon=icon,
    )


def _free_side_mission_rect(
    platforms: list[pygame.Rect],
    fragments: list[Fragment],
    level_index: int,
) -> pygame.Rect:
    for platform in platforms:
        candidate_offsets = [platform.centerx - platform.x - 18]
        if platform.width >= 124:
            edge_offsets = [28, platform.width - 64]
            if level_index % 2:
                edge_offsets.reverse()
            candidate_offsets = edge_offsets + candidate_offsets

        for offset_x in candidate_offsets:
            rect = pygame.Rect(platform.x + offset_x, platform.top - 56, 36, 36)
            if not any(rect.colliderect(fragment.rect.inflate(12, 8)) for fragment in fragments):
                return rect

    platform = platforms[0]
    return pygame.Rect(platform.x + 12, platform.top - 56, 36, 36)


def _stage_moment_for_level(
    platforms: list[pygame.Rect],
    fragments: list[Fragment],
    side_mission: SideMission,
    level_index: int,
) -> StageMoment:
    title, message, icon, color = STAGE_MOMENT_DATA[level_index]
    usable_platforms = platforms[1:]
    if usable_platforms:
        preferred_index = min(len(usable_platforms) - 1, 2 + (level_index % 4))
        platform_order = [usable_platforms[preferred_index]] + [
            platform
            for index, platform in enumerate(usable_platforms)
            if index != preferred_index
        ]
        rect = _free_stage_moment_rect(platform_order, fragments, side_mission, level_index)
    else:
        rect = pygame.Rect(320 + level_index * 12, 350, 38, 42)

    return StageMoment(
        rect=rect,
        title=title,
        message=message,
        icon=icon,
        color=color,
    )


def _free_stage_moment_rect(
    platforms: list[pygame.Rect],
    fragments: list[Fragment],
    side_mission: SideMission,
    level_index: int,
) -> pygame.Rect:
    fallback_rect = None
    fallback_distance = -1

    for platform in platforms:
        candidate_offsets = [platform.width // 2 - 19]
        if platform.width >= 136:
            edge_offsets = [34, platform.width - 72]
            if level_index % 2 == 0:
                edge_offsets.reverse()
            candidate_offsets = edge_offsets + candidate_offsets

        for offset_x in candidate_offsets:
            rect = pygame.Rect(platform.x + offset_x, platform.top - 62, 38, 42)
            if any(rect.colliderect(fragment.rect.inflate(18, 14)) for fragment in fragments):
                continue
            if rect.colliderect(side_mission.rect.inflate(18, 14)):
                continue
            distance = abs(rect.centerx - side_mission.rect.centerx)
            if distance > fallback_distance:
                fallback_rect = rect
                fallback_distance = distance
            if rect.colliderect(side_mission.rect.inflate(340, 120)):
                continue
            return rect

    if fallback_rect is not None:
        return fallback_rect

    platform = platforms[0]
    return pygame.Rect(platform.x + 16, platform.top - 62, 38, 42)


def _quiz_for_pill(pill: KnowledgePill, level_index: int, pill_index: int) -> QuizData:
    option_order = list(range(len(pill.options)))
    rotation = (level_index + pill_index) % len(option_order)
    option_order = option_order[rotation:] + option_order[:rotation]
    return QuizData(
        question=pill.question,
        options=tuple(pill.options[index] for index in option_order),
        correct_index=option_order.index(pill.correct_index),
        hint=pill.hint,
    )
