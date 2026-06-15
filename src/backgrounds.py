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
    _draw_sun_glitter(screen, ocean_y, 820 - int(camera_x * 0.08))
    for band in range(4):
        y = ocean_y + 14 + band * 24
        pygame.draw.line(screen, (82, 164, 202), (0, y), (SCREEN_WIDTH, y + 6), 2)
    for band in range(3):
        _draw_layered_wave(screen, camera_x, ocean_y + 28 + band * 26, level_width, band)
    pygame.draw.rect(screen, (232, 207, 132), (0, 430, SCREEN_WIDTH, 54))
    pygame.draw.line(screen, (248, 238, 190), (0, 430), (SCREEN_WIDTH, 430), 5)

    for world_x in range(120, level_width, 260):
        x = world_x - int(camera_x * 0.35)
        pygame.draw.line(screen, (106, 174, 204), (x, ocean_y + 42), (x + 120, ocean_y + 42), 3)
        pygame.draw.arc(screen, (238, 248, 246), (x - 20, ocean_y + 60, 86, 24), 0.15, 2.9, 2)

    for world_x in range(70, level_width, 180):
        x = world_x - int(camera_x * 0.42)
        _draw_beach_grass(screen, x, 426)
    for world_x in range(140, level_width, 220):
        _draw_shell(screen, world_x - int(camera_x * 0.46), 448 + (world_x // 220) % 2 * 12)

    _draw_birds(screen, camera_x, [(260, 118), (620, 96), (980, 132), (1360, 104)])
    _draw_coastal_marker(screen, 560 - int(camera_x * 0.32), 386)
    _draw_ship(screen, 1120 - int(camera_x * 0.25), 320)


def _draw_sugar_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((132, 196, 226))
    _draw_sun(screen, (810, 86))
    _draw_clouds(screen, camera_x, [(180, 80), (650, 112), (1180, 76)])

    _draw_hills(screen, camera_x, level_width, (104, 165, 95), 335, 0.18)
    pygame.draw.rect(screen, (192, 172, 92), (0, 390, SCREEN_WIDTH, 94))

    for world_x in range(-120, level_width, 180):
        x = world_x - int(camera_x * 0.18)
        pygame.draw.ellipse(screen, (112, 170, 92), (x, 324, 160, 52))

    for world_x in range(-40, level_width, 50):
        x = world_x - int(camera_x * 0.55)
        pygame.draw.line(screen, (64, 132, 70), (x, 392), (x + 10, 345), 4)
        pygame.draw.line(screen, (92, 158, 82), (x + 8, 392), (x + 24, 350), 4)

    for world_x in range(360, level_width, 460):
        _draw_cane_bundle(screen, world_x - int(camera_x * 0.42), 382)
    for world_x in range(520, level_width, 620):
        _draw_care_sign(screen, world_x - int(camera_x * 0.36), 370)
    _draw_water_channel(screen, camera_x, level_width)
    _draw_engenho(screen, 1200 - int(camera_x * 0.35), 330)


def _draw_interior_background(screen: pygame.Surface, camera_x: int, level_width: int):
    screen.fill((126, 189, 220))
    _draw_sun(screen, (805, 92))
    _draw_clouds(screen, camera_x, [(220, 88), (520, 118), (980, 78), (1420, 112)])

    _draw_hills(screen, camera_x, level_width, (86, 145, 92), 328, 0.15)
    _draw_hills(screen, camera_x, level_width, (62, 122, 78), 372, 0.28)
    pygame.draw.rect(screen, (113, 160, 88), (0, 410, SCREEN_WIDTH, 74))
    _draw_river_path(screen, camera_x, level_width)

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
    _draw_mine_tracks(screen, camera_x, level_width)

    for world_x in range(140, level_width, 310):
        x = world_x - int(camera_x * 0.45)
        _draw_mine_entrance(screen, x, 388)
    _draw_mine_cart(screen, 760 - int(camera_x * 0.35), 388)


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
    elif theme == "colonial_city":
        _draw_church(screen, 1120 - int(camera_x * 0.3), 304)
    elif theme == "empire":
        _draw_garden_lamp(screen, 1120 - int(camera_x * 0.3), 352)


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
        _draw_radio_tower(screen, 760 - int(camera_x * 0.32), 314)
    elif theme == "democracy":
        _draw_flag_marker(screen, 1180 - int(camera_x * 0.32), 320, (82, 150, 214))
        _draw_civic_posters(screen, 760 - int(camera_x * 0.34), 352)
    elif theme == "republic":
        _draw_bandstand(screen, 1120 - int(camera_x * 0.32), 350)
    elif theme == "rural_republic":
        _draw_coffee_sacks(screen, 930 - int(camera_x * 0.34), 376)


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
        _draw_memory_ribbons(screen, x + 18, 346, accent)

    if theme == "redemocratization":
        _draw_constitution_book(screen, 1180 - int(camera_x * 0.32), 356)
        _draw_civic_lights(screen, 820 - int(camera_x * 0.3), 312)
    else:
        _draw_memory_candles(screen, 1180 - int(camera_x * 0.32), 382)
        _draw_civic_lights(screen, 820 - int(camera_x * 0.3), 328)


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
    _draw_connection_nodes(screen, camera_x, level_width)
    _draw_school_front(screen, 1040 - int(camera_x * 0.36), 324)
    _draw_solar_panels(screen, 690 - int(camera_x * 0.34), 386)


def _draw_sun(screen: pygame.Surface, position: tuple[int, int]):
    pygame.draw.circle(screen, (248, 220, 116), position, 38)


def _draw_sun_glitter(screen: pygame.Surface, ocean_y: int, sun_x: int):
    for index in range(7):
        width = 84 - index * 8
        y = ocean_y + 18 + index * 11
        x = sun_x - width // 2 + (index % 2) * 10
        pygame.draw.line(screen, (150, 210, 222), (x, y), (x + width, y), 2)
        pygame.draw.line(screen, (238, 248, 232), (x + 18, y + 3), (x + width - 12, y + 3), 1)


def _draw_layered_wave(
    screen: pygame.Surface,
    camera_x: int,
    y: int,
    level_width: int,
    band: int,
):
    color = (204, 236, 232) if band == 0 else (132, 194, 214)
    for world_x in range(-180 + band * 44, level_width, 210):
        x = world_x - int(camera_x * (0.22 + band * 0.05))
        pygame.draw.arc(screen, color, (x, y, 96, 26), 0.18, 2.9, 2)
        pygame.draw.arc(screen, color, (x + 64, y + 2, 76, 20), 0.18, 2.9, 2)


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
    for angle in range(0, 360, 45):
        endpoint = (
            x - 18 + int(28 * pygame.math.Vector2(1, 0).rotate(angle).x),
            y + 86 + int(28 * pygame.math.Vector2(1, 0).rotate(angle).y),
        )
        pygame.draw.line(screen, (124, 96, 66), (x - 18, y + 86), endpoint, 2)


def _draw_water_channel(screen: pygame.Surface, camera_x: int, level_width: int):
    points = []
    for world_x in range(-80, level_width + 160, 160):
        x = world_x - int(camera_x * 0.5)
        y = 420 + ((world_x // 160) % 2) * 8
        points.append((x, y))
    if len(points) >= 2:
        pygame.draw.lines(screen, (86, 150, 184), False, points, 8)
        pygame.draw.lines(screen, (204, 232, 232), False, points, 2)


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


def _draw_memory_ribbons(
    screen: pygame.Surface,
    x: int,
    y: int,
    accent: tuple[int, int, int],
):
    if x < -120 or x > SCREEN_WIDTH + 80:
        return

    for offset, color in enumerate(((236, 232, 210), (248, 218, 92), accent)):
        ribbon_x = x + offset * 24
        pygame.draw.line(screen, color, (ribbon_x, y), (ribbon_x + 14, y + 28), 4)
        pygame.draw.line(screen, color, (ribbon_x + 14, y + 28), (ribbon_x + 30, y), 4)


def _draw_civic_lights(screen: pygame.Surface, x: int, y: int):
    if x < -160 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.line(screen, (78, 82, 86), (x, y + 90), (x + 132, y + 90), 3)
    for offset in (0, 44, 88, 132):
        pole_x = x + offset
        pygame.draw.rect(screen, (78, 82, 86), (pole_x - 2, y + 24, 4, 68))
        pygame.draw.circle(screen, (248, 238, 190), (pole_x, y + 18), 10)
        pygame.draw.circle(screen, (226, 168, 74), (pole_x, y + 18), 10, 2)


def _draw_modern_building(screen: pygame.Surface, x: int, y: int):
    if x < -90 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (126, 142, 154), (x, y, 72, 118))
    for row in range(4):
        for column in range(2):
            pygame.draw.rect(screen, (198, 226, 232), (x + 14 + column * 28, y + 18 + row * 24, 14, 14))


def _draw_school_front(screen: pygame.Surface, x: int, y: int):
    if x < -180 or x > SCREEN_WIDTH + 90:
        return

    pygame.draw.rect(screen, (224, 198, 128), (x, y + 48, 150, 86), border_radius=3)
    pygame.draw.polygon(screen, (112, 86, 62), [(x - 10, y + 48), (x + 75, y), (x + 160, y + 48)])
    pygame.draw.rect(screen, (92, 122, 150), (x + 58, y + 86, 34, 48))
    for offset in (18, 106):
        pygame.draw.rect(screen, (196, 228, 232), (x + offset, y + 70, 26, 24))
        pygame.draw.rect(screen, (92, 122, 150), (x + offset, y + 70, 26, 24), 2)
    pygame.draw.rect(screen, (248, 238, 190), (x + 46, y + 38, 58, 20), border_radius=4)
    pygame.draw.rect(screen, (112, 86, 62), (x + 46, y + 38, 58, 20), 2, border_radius=4)


def _draw_solar_panels(screen: pygame.Surface, x: int, y: int):
    if x < -160 or x > SCREEN_WIDTH + 80:
        return

    for offset in (0, 54, 108):
        panel = pygame.Rect(x + offset, y, 42, 24)
        pygame.draw.polygon(
            screen,
            (52, 92, 122),
            [
                panel.topleft,
                (panel.right, panel.y + 4),
                (panel.right - 6, panel.bottom),
                (panel.x - 6, panel.bottom - 4),
            ],
        )
        pygame.draw.line(screen, (190, 224, 232), (panel.x + 8, panel.y + 2), (panel.x + 2, panel.bottom - 4), 1)
        pygame.draw.line(screen, (190, 224, 232), (panel.x + 22, panel.y + 3), (panel.x + 16, panel.bottom - 3), 1)
        pygame.draw.line(screen, (82, 74, 62), (panel.centerx, panel.bottom - 2), (panel.centerx, y + 54), 3)
    pygame.draw.line(screen, (82, 74, 62), (x - 12, y + 54), (x + 154, y + 54), 3)



def _draw_birds(screen: pygame.Surface, camera_x: int, positions: list[tuple[int, int]]):
    for world_x, y in positions:
        x = world_x - int(camera_x * 0.18)
        if x < -40 or x > SCREEN_WIDTH + 40:
            continue
        pygame.draw.arc(screen, (64, 90, 112), (x - 16, y - 6, 18, 12), 0.1, 2.9, 2)
        pygame.draw.arc(screen, (64, 90, 112), (x, y - 6, 18, 12), 0.2, 3.0, 2)


def _draw_coastal_marker(screen: pygame.Surface, x: int, y: int):
    if x < -80 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (166, 132, 86), (x, y, 20, 48))
    pygame.draw.polygon(screen, (134, 102, 70), [(x - 8, y), (x + 10, y - 20), (x + 28, y)])
    pygame.draw.rect(screen, (92, 68, 44), (x - 10, y + 42, 40, 8))


def _draw_beach_grass(screen: pygame.Surface, x: int, y: int):
    if x < -40 or x > SCREEN_WIDTH + 40:
        return

    pygame.draw.line(screen, (70, 132, 72), (x, y + 10), (x + 10, y - 14), 3)
    pygame.draw.line(screen, (88, 150, 78), (x + 8, y + 10), (x + 24, y - 8), 3)
    pygame.draw.line(screen, (66, 118, 68), (x + 18, y + 10), (x + 28, y - 18), 3)
    pygame.draw.ellipse(screen, (214, 190, 118), (x - 6, y + 8, 44, 12))


def _draw_shell(screen: pygame.Surface, x: int, y: int):
    if x < -40 or x > SCREEN_WIDTH + 40:
        return

    shell_color = (248, 226, 176)
    outline = (154, 118, 82)
    pygame.draw.arc(screen, shell_color, (x, y, 24, 16), 0, 3.14, 8)
    pygame.draw.arc(screen, outline, (x, y, 24, 16), 0, 3.14, 2)
    for offset in (5, 10, 15):
        pygame.draw.line(screen, outline, (x + 12, y + 4), (x + offset, y + 14), 1)


def _draw_care_sign(screen: pygame.Surface, x: int, y: int):
    if x < -80 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (92, 70, 46), (x + 22, y + 26, 5, 48))
    pygame.draw.rect(screen, (244, 226, 150), (x, y, 50, 30), border_radius=4)
    pygame.draw.rect(screen, (92, 70, 46), (x, y, 50, 30), 2, border_radius=4)
    pygame.draw.line(screen, (92, 70, 46), (x + 13, y + 21), (x + 25, y + 8), 3)
    pygame.draw.line(screen, (92, 70, 46), (x + 25, y + 8), (x + 37, y + 21), 3)


def _draw_cane_bundle(screen: pygame.Surface, x: int, y: int):
    if x < -90 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (126, 96, 54), (x - 8, y + 24, 86, 12), border_radius=4)
    for offset in range(0, 72, 12):
        pygame.draw.line(screen, (68, 132, 72), (x + offset, y + 30), (x + offset + 22, y), 5)
        pygame.draw.line(screen, (108, 164, 82), (x + offset + 5, y + 30), (x + offset + 24, y + 4), 3)


def _draw_river_path(screen: pygame.Surface, camera_x: int, level_width: int):
    points = []
    for world_x in range(-120, level_width + 220, 180):
        x = world_x - int(camera_x * 0.22)
        y = 404 + ((world_x // 180) % 2) * 22
        points.append((x, y))
    if len(points) >= 2:
        pygame.draw.lines(screen, (70, 146, 180), False, points, 14)
        pygame.draw.lines(screen, (126, 198, 214), False, points, 5)


def _draw_mine_tracks(screen: pygame.Surface, camera_x: int, level_width: int):
    rail_y = 436
    for world_x in range(-80, level_width, 120):
        x = world_x - int(camera_x * 0.44)
        pygame.draw.line(screen, (84, 68, 50), (x, rail_y + 12), (x + 72, rail_y - 8), 3)
    pygame.draw.line(screen, (72, 62, 54), (-20, rail_y), (SCREEN_WIDTH + 40, rail_y), 3)
    pygame.draw.line(screen, (72, 62, 54), (-20, rail_y + 18), (SCREEN_WIDTH + 40, rail_y + 18), 3)


def _draw_mine_cart(screen: pygame.Surface, x: int, y: int):
    if x < -90 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.polygon(screen, (94, 82, 76), [(x, y + 34), (x + 74, y + 34), (x + 62, y + 62), (x + 12, y + 62)])
    pygame.draw.rect(screen, (58, 54, 52), (x + 12, y + 26, 48, 14))
    pygame.draw.circle(screen, (48, 44, 42), (x + 18, y + 66), 8)
    pygame.draw.circle(screen, (48, 44, 42), (x + 58, y + 66), 8)


def _draw_church(screen: pygame.Surface, x: int, y: int):
    if x < -150 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (226, 218, 184), (x, y + 42, 118, 92))
    pygame.draw.polygon(screen, (122, 82, 68), [(x - 8, y + 42), (x + 59, y + 6), (x + 126, y + 42)])
    pygame.draw.rect(screen, (216, 204, 168), (x + 42, y, 34, 52))
    pygame.draw.polygon(screen, (122, 82, 68), [(x + 36, y), (x + 59, y - 24), (x + 82, y)])
    pygame.draw.rect(screen, (72, 64, 58), (x + 46, y + 84, 26, 50))
    pygame.draw.circle(screen, (98, 132, 152), (x + 59, y + 46), 10)


def _draw_garden_lamp(screen: pygame.Surface, x: int, y: int):
    if x < -80 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (66, 62, 58), (x + 16, y, 6, 66))
    pygame.draw.circle(screen, (248, 220, 116), (x + 19, y - 6), 12)
    pygame.draw.circle(screen, (66, 62, 58), (x + 19, y - 6), 12, 2)
    pygame.draw.circle(screen, (72, 132, 78), (x - 10, y + 62), 16)
    pygame.draw.circle(screen, (82, 148, 86), (x + 44, y + 62), 18)


def _draw_radio_tower(screen: pygame.Surface, x: int, y: int):
    if x < -100 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.line(screen, (74, 78, 82), (x, y + 96), (x + 36, y), 4)
    pygame.draw.line(screen, (74, 78, 82), (x + 72, y + 96), (x + 36, y), 4)
    pygame.draw.line(screen, (74, 78, 82), (x + 14, y + 58), (x + 58, y + 58), 3)
    pygame.draw.arc(screen, (74, 78, 82), (x + 12, y - 16, 48, 36), 0.2, 2.9, 2)
    pygame.draw.arc(screen, (74, 78, 82), (x, y - 30, 72, 54), 0.2, 2.9, 2)


def _draw_civic_posters(screen: pygame.Surface, x: int, y: int):
    if x < -120 or x > SCREEN_WIDTH + 80:
        return

    colors = [(238, 222, 166), (206, 226, 204), (204, 222, 236)]
    for index, color in enumerate(colors):
        poster = pygame.Rect(x + index * 38, y + (index % 2) * 10, 30, 42)
        pygame.draw.rect(screen, color, poster)
        pygame.draw.rect(screen, (92, 82, 70), poster, 2)
        pygame.draw.line(screen, (92, 82, 70), poster.midtop, (poster.centerx, poster.bottom + 22), 2)


def _draw_bandstand(screen: pygame.Surface, x: int, y: int):
    if x < -150 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.ellipse(screen, (160, 150, 126), (x, y + 62, 136, 28))
    pygame.draw.polygon(screen, (104, 92, 78), [(x + 4, y + 36), (x + 68, y), (x + 132, y + 36)])
    for column_x in (x + 24, x + 62, x + 100):
        pygame.draw.rect(screen, (226, 218, 184), (column_x, y + 36, 10, 46))


def _draw_coffee_sacks(screen: pygame.Surface, x: int, y: int):
    if x < -120 or x > SCREEN_WIDTH + 80:
        return

    for index in range(3):
        sack = pygame.Rect(x + index * 34, y + (index % 2) * 8, 34, 42)
        pygame.draw.ellipse(screen, (156, 118, 72), sack)
        pygame.draw.arc(screen, (94, 72, 50), sack, 0.2, 3.0, 2)


def _draw_constitution_book(screen: pygame.Surface, x: int, y: int):
    if x < -110 or x > SCREEN_WIDTH + 80:
        return

    pygame.draw.rect(screen, (236, 232, 210), (x, y + 16, 84, 58), border_radius=4)
    pygame.draw.line(screen, (82, 112, 160), (x + 42, y + 18), (x + 42, y + 72), 3)
    pygame.draw.rect(screen, (82, 150, 214), (x + 12, y + 30, 20, 8))
    pygame.draw.rect(screen, (82, 150, 214), (x + 52, y + 30, 20, 8))
    pygame.draw.rect(screen, (76, 154, 120), (x + 18, y, 48, 22), border_radius=4)


def _draw_memory_candles(screen: pygame.Surface, x: int, y: int):
    if x < -100 or x > SCREEN_WIDTH + 80:
        return

    for offset in (0, 28, 56):
        pygame.draw.rect(screen, (238, 232, 210), (x + offset, y + 18, 14, 34), border_radius=3)
        pygame.draw.polygon(screen, (238, 196, 82), [(x + offset + 7, y + 4), (x + offset + 2, y + 18), (x + offset + 12, y + 18)])


def _draw_connection_nodes(screen: pygame.Surface, camera_x: int, level_width: int):
    points = []
    for world_x in range(220, level_width, 360):
        x = world_x - int(camera_x * 0.3)
        if -40 <= x <= SCREEN_WIDTH + 40:
            y = 166 + ((world_x // 360) % 3) * 28
            points.append((x, y))
            pygame.draw.circle(screen, (82, 150, 214), (x, y), 6)
            pygame.draw.circle(screen, (248, 238, 190), (x, y), 3)
    for first, second in zip(points, points[1:]):
        pygame.draw.line(screen, (82, 150, 214), first, second, 2)
