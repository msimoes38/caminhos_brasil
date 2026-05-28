from dataclasses import dataclass

import pygame

from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH


@dataclass(frozen=True)
class LevelData:
    title: str
    year: str
    mission: str
    historical_note: str
    intro_text: str
    width: int
    start_position: tuple[int, int]
    platforms: list[tuple[int, int, int, int]]
    goal: tuple[int, int, int, int]


@dataclass(frozen=True)
class Level:
    title: str
    year: str
    mission: str
    historical_note: str
    intro_text: str
    width: int
    start_position: tuple[int, int]
    platforms: list[pygame.Rect]
    goal: pygame.Rect


GROUND_HEIGHT = 64


LEVELS = [
    LevelData(
        title="Chegada dos portugueses",
        year="1500",
        mission="Alcance o marco verde para observar o litoral com seguranca.",
        historical_note=(
            "Em 1500, a expedicao portuguesa chegou ao litoral que depois seria "
            "chamado Brasil."
        ),
        intro_text=(
            "Mig chega a um litoral desconhecido. Antes de explorar, ele precisa "
            "alcancar um ponto seguro para observar a chegada das embarcacoes."
        ),
        width=1600,
        start_position=(80, SCREEN_HEIGHT - GROUND_HEIGHT - 56),
        platforms=[
            (0, SCREEN_HEIGHT - GROUND_HEIGHT, 1600, GROUND_HEIGHT),
            (220, 390, 160, 28),
            (470, 330, 160, 28),
            (690, 265, 150, 28),
            (950, 370, 180, 28),
            (1230, 310, 170, 28),
        ],
        goal=(1480, 250, 42, 60),
    ),
    LevelData(
        title="Ciclo do acucar",
        year="Seculo XVI",
        mission="Atravesse os engenhos e alcance o ponto de encontro.",
        historical_note=(
            "No periodo colonial, a producao de acucar se tornou uma das principais "
            "atividades economicas."
        ),
        intro_text=(
            "Agora Mig visita uma regiao de engenhos. O caminho mostra como o "
            "acucar marcou a economia colonial e a ocupacao do territorio."
        ),
        width=1800,
        start_position=(70, SCREEN_HEIGHT - GROUND_HEIGHT - 56),
        platforms=[
            (0, SCREEN_HEIGHT - GROUND_HEIGHT, 1800, GROUND_HEIGHT),
            (180, 410, 130, 28),
            (360, 355, 130, 28),
            (560, 300, 130, 28),
            (760, 245, 120, 28),
            (1010, 330, 160, 28),
            (1270, 390, 150, 28),
            (1510, 315, 150, 28),
        ],
        goal=(1690, 255, 42, 60),
    ),
]


def get_level_count() -> int:
    return len(LEVELS)


def create_level(index: int) -> Level:
    data = LEVELS[index]

    return Level(
        title=data.title,
        year=data.year,
        mission=data.mission,
        historical_note=data.historical_note,
        intro_text=data.intro_text,
        width=data.width,
        start_position=data.start_position,
        platforms=[pygame.Rect(platform) for platform in data.platforms],
        goal=pygame.Rect(data.goal),
    )
