from dataclasses import dataclass

import pygame

from src.level_data import LEVELS


@dataclass(frozen=True)
class Fragment:
    rect: pygame.Rect
    info: str


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


def get_level_count() -> int:
    return len(LEVELS)


def get_level_title(index: int) -> str:
    data = LEVELS[index]
    return f"{data.year} - {data.title}"


def get_level_plain_title(index: int) -> str:
    return LEVELS[index].title


def get_level_fragment_count(index: int) -> int:
    return len(LEVELS[index].fragments)


def get_total_fragment_count() -> int:
    return sum(len(level.fragments) for level in LEVELS)


def create_level(index: int) -> Level:
    data = LEVELS[index]

    return Level(
        title=data.title,
        year=data.year,
        mission=data.mission,
        historical_note=data.historical_note,
        intro_text=data.intro_text,
        theme=data.theme,
        width=data.width,
        start_position=data.start_position,
        platforms=[pygame.Rect(platform) for platform in data.platforms],
        goal=pygame.Rect(data.goal),
        fragments=[
            Fragment(rect=pygame.Rect(fragment.area), info=fragment.info)
            for fragment in data.fragments
        ],
        hazards=[pygame.Rect(hazard) for hazard in data.hazards],
        checkpoints=[pygame.Rect(checkpoint) for checkpoint in data.checkpoints],
    )
