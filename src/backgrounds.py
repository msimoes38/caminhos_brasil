import pygame

from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_background(screen: pygame.Surface, theme: str, camera_x: int, level_width: int):
    if theme == "sugar":
        _draw_sugar_background(screen, camera_x, level_width)
    elif theme == "interior":
        _draw_interior_background(screen, camera_x, level_width)
    elif theme == "mines":
        _draw_mines_background(screen, camera_x, level_width)
    elif theme in ("colonial_city", "court", "independence", "empire"):
        _draw_historic_city_background(screen, theme, camera_x, level_width)
    elif theme in ("republic", "rural_republic", "vargas", "democracy"):
        _draw_republic_background(screen, theme, camera_x, level_width)
    elif theme in ("dictatorship", "redemocratization"):
        _draw_memory_background(screen, theme, camera_x, level_width)
    elif theme == "contemporary":
        _draw_contemporary_background(screen, camera_x, level_width)
    else:
        _draw_coast_background(screen, camera_x, level_width)


def _draw_coast_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((122, 194, 235))
    _draw_sun(screen, (820, 88))
    _draw_clouds(screen, camera_x, [(140, 96), (430, 70), (760, 120), (1160, 82)])

    ocean_y = 350
    pygame.draw.rect(screen, (58, 143, 190), (0, ocean_y, SCREEN_WIDTH, 112))
    pygame.draw.rect(screen, (232, 207, 132), (0, 430, SCREEN_WIDTH, 54))

    for world_x in range(120, level_width, 260):
        x = world_x - int(camera_x * 0.35)
        pygame.draw.line(screen, (106, 174, 204), (x, ocean_y + 42), (x + 120, ocean_y + 42), 3)

    _draw_ship(screen, 1120 - int(camera_x * 0.25), 320)


def _draw_sugar_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((132, 196, 226))
    _draw_sun(screen, (810, 86))
    _draw_clouds(screen, camera_x, [(180, 80), (650, 112), (1180, 76)])

    _draw_hills(screen, camera_x, level_width, (104, 165, 95), 335, 0.18)
    pygame.draw.rect(screen, (192, 172, 92), (0, 390, SCREEN_WIDTH, 94))

    for world_x in range(-40, level_width, 50):
        x = world_x - int(camera_x * 0.55)
        pygame.draw.line(screen, (64, 132, 70), (x, 392), (x + 10, 345), 4)
        pygame.draw.line(screen, (92, 158, 82), (x + 8, 392), (x + 24, 350), 4)

    _draw_engenho(screen, 1200 - int(camera_x * 0.35), 330)


def _draw_interior_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((126, 189, 220))
    _draw_sun(screen, (805, 92))
    _draw_clouds(screen, camera_x, [(220, 88), (520, 118), (980, 78), (1420, 112)])

    _draw_hills(screen, camera_x, level_width, (86, 145, 92), 328, 0.15)
    _draw_hills(screen, camera_x, level_width, (62, 122, 78), 372, 0.28)
    pygame.draw.rect(screen, (113, 160, 88), (0, 410, SCREEN_WIDTH, 74))

    for world_x in range(80, level_width, 140):
        x = world_x - int(camera_x * 0.45)
        _draw_tree(screen, x, 380)


def _draw_mines_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((136, 183, 213))
    _draw_sun(screen, (805, 88))
    _draw_clouds(screen, camera_x, [(180, 92), (620, 84), (1120, 118)])
    _draw_hills(screen, camera_x, level_width, (114, 118, 112), 330, 0.12)
    _draw_hills(screen, camera_x, level_width, (84, 92, 94), 385, 0.25)
    pygame.draw.rect(screen, (142, 122, 88), (0, 415, SCREEN_WIDTH, 62))

    for world_x in range(140, level_width, 310):
        x = world_x - int(camera_x * 0.45)
        _draw_mine_entrance(screen, x, 388)


def _draw_historic_city_background(
    screen: pygame.Surface,
    theme: str,
    camera_x: int,
    level_width: int,
):
    sky = {
        "colonial_city": (142, 190, 220),
        "court": (150, 198, 226),
        "independence": (128, 194, 224),
        "empire": (146, 190, 214),
    }[theme]
    screen.fill(sky)
    _draw_sun(screen, (812, 82))
    _draw_clouds(screen, camera_x, [(160, 92), (560, 74), (980, 108)])
    _draw_hills(screen, camera_x, level_width, (98, 148, 105), 366, 0.16)
    pygame.draw.rect(screen, (190, 172, 128), (0, 410, SCREEN_WIDTH, 66))

    colors = {
        "colonial_city": ((230, 214, 170), (120, 80, 60)),
        "court": ((224, 198, 146), (116, 88, 72)),
        "independence": ((226, 214, 150), (72, 122, 76)),
        "empire": ((216, 204, 178), (96, 82, 120)),
    }[theme]
    for world_x in range(-80, level_width, 220):
        x = world_x - int(camera_x * 0.38)
        _draw_colonial_house(screen, x, 344, colors[0], colors[1])

    if theme == "court":
        _draw_palace(screen, 1120 - int(camera_x * 0.28), 300)
    elif theme == "independence":
        _draw_flag_marker(screen, 1110 - int(camera_x * 0.28), 314, (58, 142, 82))


def _draw_republic_background(
    screen: pygame.Surface,
    theme: str,
    camera_x: int,
    level_width: int,
):
    screen.fill((134, 190, 220))
    _draw_sun(screen, (810, 88))
    _draw_clouds(screen, camera_x, [(210, 88), (640, 110), (1160, 82)])

    if theme == "rural_republic":
        _draw_hills(screen, camera_x, level_width, (92, 150, 82), 350, 0.18)
        pygame.draw.rect(screen, (178, 150, 92), (0, 402, SCREEN_WIDTH, 76))
        for world_x in range(0, level_width, 180):
            x = world_x - int(camera_x * 0.48)
            pygame.draw.line(screen, (92, 78, 58), (x, 430), (x + 130, 430), 4)
            pygame.draw.circle(screen, (66, 94, 70), (x + 32, 376), 18)
            pygame.draw.circle(screen, (66, 94, 70), (x + 62, 366), 22)
    else:
        ground = (178, 172, 152) if theme == "republic" else (154, 166, 170)
        pygame.draw.rect(screen, ground, (0, 405, SCREEN_WIDTH, 72))
        for world_x in range(-60, level_width, 190):
            x = world_x - int(camera_x * 0.42)
            _draw_city_block(screen, x, 330, theme)

    if theme == "vargas":
        _draw_factory(screen, 1200 - int(camera_x * 0.32), 315)
    elif theme == "democracy":
        _draw_flag_marker(screen, 1180 - int(camera_x * 0.32), 320, (82, 150, 214))


def _draw_memory_background(
    screen: pygame.Surface,
    theme: str,
    camera_x: int,
    level_width: int,
):
    if theme == "dictatorship":
        screen.fill((132, 150, 164))
        accent = (96, 112, 124)
    else:
        screen.fill((128, 188, 216))
        accent = (76, 154, 120)

    _draw_clouds(screen, camera_x, [(190, 92), (720, 78), (1120, 112)])
    pygame.draw.rect(screen, (166, 166, 150), (0, 408, SCREEN_WIDTH, 70))
    for world_x in range(-40, level_width, 210):
        x = world_x - int(camera_x * 0.42)
        _draw_city_block(screen, x, 335, theme)

    for world_x in range(240, level_width, 520):
        x = world_x - int(camera_x * 0.35)
        _draw_memory_wall(screen, x, 356, accent)


def _draw_contemporary_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((126, 196, 224))
    _draw_sun(screen, (810, 82))
    _draw_clouds(screen, camera_x, [(120, 90), (520, 116), (930, 78), (1320, 106)])
    pygame.draw.rect(screen, (132, 176, 154), (0, 410, SCREEN_WIDTH, 66))

    for world_x in range(-70, level_width, 150):
        x = world_x - int(camera_x * 0.4)
        _draw_modern_building(screen, x, 322 + (world_x % 3) * 10)

    for world_x in range(120, level_width, 420):
        x = world_x - int(camera_x * 0.48)
        _draw_tree(screen, x, 390)


def _draw_sun(screen: pygame.Surface, position: tuple[int, int]):
    pygame.draw.circle(screen, (248, 220, 116), position, 38)


def _draw_clouds(screen: pygame.Surface, camera_x: int, positions: list[tuple[int, int]]):
    for world_x, y in positions:
        x = world_x - int(camera_x * 0.2)
        pygame.draw.circle(screen, (242, 248, 250), (x, y), 20)
        pygame.draw.circle(screen, (242, 248, 250), (x + 24, y - 10), 25)
        pygame.draw.circle(screen, (242, 248, 250), (x + 52, y), 20)
        pygame.draw.rect(screen, (242, 248, 250), (x, y, 54, 20))


def _draw_hills(
    screen: pygame.Surface,
    camera_x: int,
    level_width: int,
    color: tuple[int, int, int],
    base_y: int,
    parallax: float,
):
    points = [(0, SCREEN_HEIGHT)]
    for world_x in range(-120, level_width + 260, 220):
        x = world_x - int(camera_x * parallax)
        points.append((x, base_y - 36))
        points.append((x + 110, base_y - 78))
        points.append((x + 220, base_y - 32))
    points.append((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.draw.polygon(screen, color, points)


def _draw_ship(screen: pygame.Surface, x: int, y: int):
    if x < -140 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.polygon(screen, (100, 71, 48), [(x, y + 38), (x + 110, y + 38), (x + 88, y + 58), (x + 20, y + 58)])
    pygame.draw.line(screen, (74, 52, 38), (x + 52, y + 38), (x + 52, y - 28), 4)
    pygame.draw.polygon(screen, (240, 230, 190), [(x + 56, y - 24), (x + 56, y + 28), (x + 98, y + 22)])


def _draw_engenho(screen: pygame.Surface, x: int, y: int):
    if x < -180 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (139, 95, 58), (x, y + 40, 120, 70))
    pygame.draw.polygon(screen, (96, 65, 46), [(x - 12, y + 40), (x + 60, y - 5), (x + 132, y + 40)])
    pygame.draw.rect(screen, (226, 199, 134), (x + 18, y + 62, 28, 48))
    pygame.draw.rect(screen, (92, 68, 48), (x + 70, y + 62, 32, 24))
    pygame.draw.circle(screen, (86, 74, 58), (x - 18, y + 86), 28, 5)
    pygame.draw.line(screen, (86, 74, 58), (x - 46, y + 86), (x + 10, y + 86), 4)
    pygame.draw.line(screen, (86, 74, 58), (x - 18, y + 58), (x - 18, y + 114), 4)


def _draw_tree(screen: pygame.Surface, x: int, y: int):
    if x < -80 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (92, 68, 44), (x + 18, y, 16, 54))
    pygame.draw.circle(screen, (48, 112, 70), (x + 12, y - 2), 28)
    pygame.draw.circle(screen, (62, 132, 78), (x + 36, y - 8), 32)
    pygame.draw.circle(screen, (54, 122, 72), (x + 24, y - 34), 26)


def _draw_mine_entrance(screen: pygame.Surface, x: int, y: int):
    if x < -100 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.polygon(screen, (92, 82, 74), [(x, y + 54), (x + 48, y), (x + 96, y + 54)])
    pygame.draw.rect(screen, (48, 48, 52), (x + 30, y + 24, 36, 30))
    pygame.draw.line(screen, (170, 144, 86), (x + 18, y + 54), (x + 78, y + 54), 4)


def _draw_colonial_house(
    screen: pygame.Surface,
    x: int,
    y: int,
    wall_color: tuple[int, int, int],
    roof_color: tuple[int, int, int],
):
    if x < -150 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, wall_color, (x, y + 34, 120, 76))
    pygame.draw.polygon(screen, roof_color, [(x - 10, y + 34), (x + 60, y - 4), (x + 130, y + 34)])
    pygame.draw.rect(screen, (86, 70, 58), (x + 18, y + 66, 24, 44))
    pygame.draw.rect(screen, (98, 132, 152), (x + 68, y + 58, 28, 24))
    pygame.draw.rect(screen, (56, 58, 64), (x + 68, y + 58, 28, 24), 2)


def _draw_palace(screen: pygame.Surface, x: int, y: int):
    if x < -220 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (226, 204, 156), (x, y + 60, 180, 96))
    pygame.draw.polygon(screen, (138, 94, 74), [(x - 12, y + 60), (x + 90, y + 8), (x + 192, y + 60)])
    for column_x in (x + 24, x + 70, x + 116):
        pygame.draw.rect(screen, (236, 226, 194), (column_x, y + 72, 18, 84))
    pygame.draw.rect(screen, (74, 68, 62), (x + 78, y + 104, 30, 52))


def _draw_flag_marker(
    screen: pygame.Surface,
    x: int,
    y: int,
    color: tuple[int, int, int],
):
    if x < -80 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (64, 64, 64), (x, y, 5, 86))
    pygame.draw.rect(screen, color, (x + 5, y + 8, 58, 32))
    pygame.draw.rect(screen, (244, 220, 94), (x + 22, y + 16, 20, 16))


def _draw_city_block(screen: pygame.Surface, x: int, y: int, theme: str):
    if x < -110 or x > SCREEN_WIDTH + 80:
        return

    color = {
        "republic": (202, 194, 170),
        "vargas": (154, 164, 166),
        "democracy": (190, 198, 178),
        "dictatorship": (124, 132, 138),
        "redemocratization": (190, 198, 178),
    }.get(theme, (190, 194, 184))
    pygame.draw.rect(screen, color, (x, y, 92, 90))
    pygame.draw.rect(screen, (74, 86, 96), (x + 16, y + 20, 18, 18))
    pygame.draw.rect(screen, (74, 86, 96), (x + 56, y + 20, 18, 18))
    pygame.draw.rect(screen, (74, 70, 64), (x + 36, y + 54, 22, 36))


def _draw_factory(screen: pygame.Surface, x: int, y: int):
    if x < -180 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (122, 122, 120), (x, y + 58, 160, 88))
    pygame.draw.polygon(screen, (104, 104, 102), [(x, y + 58), (x + 32, y + 30), (x + 64, y + 58)])
    pygame.draw.polygon(screen, (104, 104, 102), [(x + 64, y + 58), (x + 96, y + 28), (x + 128, y + 58)])
    pygame.draw.rect(screen, (90, 84, 78), (x + 126, y, 24, 146))


def _draw_memory_wall(
    screen: pygame.Surface,
    x: int,
    y: int,
    color: tuple[int, int, int],
):
    if x < -120 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, color, (x, y, 112, 64))
    pygame.draw.rect(screen, (236, 232, 210), (x + 18, y + 16, 76, 28))


def _draw_modern_building(screen: pygame.Surface, x: int, y: int):
    if x < -90 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (126, 142, 154), (x, y, 72, 118))
    for row in range(4):
        for column in range(2):
            pygame.draw.rect(screen, (198, 226, 232), (x + 14 + column * 28, y + 18 + row * 24, 14, 14))
