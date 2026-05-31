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


def get_level_count() -> int:
    return len(LEVELS)


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
