import asyncio

import pygame

from src.backgrounds import draw_background
from src.levels import (
    create_level,
    get_level_count,
    get_level_fragment_count,
    get_level_plain_title,
    get_level_title,
    get_total_fragment_count,
)
from src.player import Player
from src.progress import ProgressStore
from src.sounds import SoundManager
from src.settings import (
    FPS,
    CHECKPOINT_COLOR,
    CHECKPOINT_OUTLINE,
    FRAGMENT_COLOR,
    FRAGMENT_OUTLINE,
    GOAL_COLOR,
    GROUND_COLOR,
    HAZARD_COLOR,
    HAZARD_OUTLINE,
    PLATFORM_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TEXT_COLOR,
    TITLE,
)


STATE_MENU = "menu"
STATE_LEVEL_SELECT = "level_select"
STATE_INTRO = "intro"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_COMPLETED = "completed"
STATE_COLLECTION = "collection"
STATE_FINAL = "final"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 44)
        self.sounds = SoundManager()
        self.menu_image = self._load_menu_image()
        self.progress_store = ProgressStore(get_level_count())
        self.saved_progress = self.progress_store.load()
        self.temporary_session = False

        self.selected_level_index = 0
        self.level_select_scroll = 0
        self.collection_scroll = 0
        self.previous_state = STATE_MENU
        self.running = True
        self._apply_progress(self.saved_progress)
        self._load_level(0, STATE_MENU)

    async def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self._handle_events()
            self._update(dt)
            self._draw()

            await asyncio.sleep(0)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key: int):
        if key == pygame.K_ESCAPE:
            self.running = False
            return

        if key == pygame.K_c:
            self._toggle_collection()
            return

        if self.state == STATE_MENU:
            self._handle_menu_keydown(key)
        elif self.state == STATE_LEVEL_SELECT:
            self._handle_level_select_keydown(key)
        elif self.state == STATE_INTRO:
            if key == pygame.K_RETURN:
                self.state = STATE_PLAYING
            elif key == pygame.K_m:
                self.state = STATE_MENU
        elif self.state == STATE_PLAYING:
            if key == pygame.K_p:
                self.state = STATE_PAUSED
            elif key == pygame.K_r:
                self._restart_level()
            elif key == pygame.K_m:
                self.state = STATE_MENU
        elif self.state == STATE_PAUSED:
            self._handle_pause_keydown(key)
        elif self.state == STATE_COMPLETED:
            self._handle_completed_keydown(key)
        elif self.state == STATE_FINAL:
            self._handle_final_keydown(key)
        elif self.state == STATE_COLLECTION:
            self._handle_collection_keydown(key)

    def _handle_menu_keydown(self, key: int):
        if key == pygame.K_RETURN:
            self.sounds.play("menu")
            self._load_level(self.highest_unlocked_level, STATE_INTRO)
        elif key == pygame.K_n:
            self.sounds.play("menu")
            self._start_temporary_new_journey()
        elif key == pygame.K_s:
            self.sounds.play("select")
            self.state = STATE_LEVEL_SELECT
            self.selected_level_index = min(self.level_index, self.highest_unlocked_level)
            self._sync_level_select_scroll()

    def _handle_level_select_keydown(self, key: int):
        if key in (pygame.K_UP, pygame.K_w):
            self.selected_level_index = max(0, self.selected_level_index - 1)
            self._sync_level_select_scroll()
            self.sounds.play("select")
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected_level_index = min(get_level_count() - 1, self.selected_level_index + 1)
            self._sync_level_select_scroll()
            self.sounds.play("select")
        elif key == pygame.K_RETURN:
            if self.selected_level_index <= self.highest_unlocked_level:
                self.sounds.play("menu")
                self._load_level(self.selected_level_index, STATE_INTRO)
            else:
                self.feedback_message = "Essa fase ainda esta bloqueada. Conclua as anteriores primeiro."
                self.feedback_message_timer = 2.5
                self.sounds.play("blocked")
        elif key == pygame.K_m:
            self.state = STATE_MENU

    def _handle_pause_keydown(self, key: int):
        if key in (pygame.K_p, pygame.K_RETURN):
            self.state = STATE_PLAYING
        elif key == pygame.K_r:
            self._restart_level()
        elif key == pygame.K_m:
            self.state = STATE_MENU

    def _handle_completed_keydown(self, key: int):
        if key == pygame.K_RETURN:
            self._go_to_next_level()
        elif key == pygame.K_r:
            self._restart_level()
        elif key == pygame.K_m:
            self.state = STATE_MENU

    def _handle_final_keydown(self, key: int):
        if key in (pygame.K_RETURN, pygame.K_m):
            self.state = STATE_MENU
        elif key == pygame.K_r:
            self._restart_level()

    def _handle_collection_keydown(self, key: int):
        max_scroll = max(0, len(self._collection_rows()) - 8)
        if key in (pygame.K_UP, pygame.K_w):
            self.collection_scroll = max(0, self.collection_scroll - 1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.collection_scroll = min(max_scroll, self.collection_scroll + 1)
        elif key in (pygame.K_c, pygame.K_m, pygame.K_RETURN):
            self.state = self.previous_state

    def _update(self, dt: float):
        if self.state != STATE_PLAYING:
            self._update_feedback_message(dt)
            return

        keys = pygame.key.get_pressed()
        was_on_ground = self.player.on_ground
        self.player.handle_input(keys)
        if was_on_ground and self.player.velocity.y < 0:
            self.sounds.play("jump")
        self.player.update(dt, self.level.platforms, self.level.width)
        self._update_camera()
        self._update_fragment_message(dt)
        self._update_feedback_message(dt)
        self._collect_fragments()
        self._update_checkpoints()

        if self._should_restart_attempt():
            self._reset_attempt("Mig voltou ao ponto de retorno para tentar com mais cuidado.")
            return

        if self.player.rect.colliderect(self.level.goal) and self._all_fragments_collected():
            self._complete_level()

    def _collect_fragments(self):
        remaining_fragments = []
        collected_any = False

        for fragment in self.fragments:
            if self.player.rect.colliderect(fragment.rect):
                collected_any = True
                self.fragment_message = fragment.info
                self.fragment_message_timer = 4
                self._add_collection_entry(fragment.info)
            else:
                remaining_fragments.append(fragment)

        self.fragments = remaining_fragments
        if collected_any:
            self.sounds.play("collect")

    def _add_collection_entry(self, info: str):
        entry = (self.level.title, info)
        if entry in self.collection_entry_set:
            return

        self.collection_entry_set.add(entry)
        self.collection_entries.append(entry)
        self._save_progress()

    def _update_fragment_message(self, dt: float):
        if self.fragment_message_timer <= 0:
            return

        self.fragment_message_timer -= dt
        if self.fragment_message_timer <= 0:
            self.fragment_message = ""

    def _update_feedback_message(self, dt: float):
        if self.feedback_message_timer <= 0:
            return

        self.feedback_message_timer -= dt
        if self.feedback_message_timer <= 0:
            self.feedback_message = ""

    def _should_restart_attempt(self) -> bool:
        touched_hazard = any(
            self.player.rect.colliderect(hazard) for hazard in self.level.hazards
        )
        fell_below_level = self.player.rect.top > SCREEN_HEIGHT + 120
        return touched_hazard or fell_below_level

    def _update_checkpoints(self):
        for index, checkpoint in enumerate(self.level.checkpoints):
            if index in self.active_checkpoints:
                continue
            if not self.player.rect.colliderect(checkpoint):
                continue

            self.active_checkpoints.add(index)
            self.respawn_position = (
                checkpoint.centerx - self.player.rect.width // 2,
                checkpoint.bottom - self.player.rect.height,
            )
            self.feedback_message = "Ponto de retorno ativado."
            self.feedback_message_timer = 2.5
            self.sounds.play("checkpoint")

    def _all_fragments_collected(self) -> bool:
        return len(self.fragments) == 0

    def _update_camera(self):
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        max_camera_x = max(0, self.level.width - SCREEN_WIDTH)
        self.camera_x = max(0, min(target_x, max_camera_x))

    def _load_level(self, index: int, state: str):
        self.level_index = index
        self.level = create_level(self.level_index)
        self.player = Player(self.level.start_position)
        self.fragments = list(self.level.fragments)
        self.total_fragments = len(self.fragments)
        self.respawn_position = self.level.start_position
        self.active_checkpoints = set()
        self.fragment_message = ""
        self.fragment_message_timer = 0
        self.feedback_message = ""
        self.feedback_message_timer = 0
        self.camera_x = 0
        self.state = state

    def _load_menu_image(self) -> pygame.Surface | None:
        try:
            image = pygame.image.load("abertura.png").convert()
        except (FileNotFoundError, pygame.error):
            return None

        return pygame.transform.smoothscale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def _restart_level(self, feedback_message: str = ""):
        self._load_level(self.level_index, STATE_PLAYING)
        self.feedback_message = feedback_message
        self.feedback_message_timer = 2.5 if feedback_message else 0

    def _reset_attempt(self, feedback_message: str):
        self.player = Player(self.respawn_position)
        self.fragment_message = ""
        self.fragment_message_timer = 0
        self.feedback_message = feedback_message
        self.feedback_message_timer = 2.5
        self.sounds.play("reset")
        self._update_camera()

    def _go_to_next_level(self):
        next_index = self.level_index + 1
        if next_index >= get_level_count():
            self.state = STATE_FINAL
            self.sounds.play("final")
            return

        self._load_level(next_index, STATE_INTRO)

    def _complete_level(self):
        self.state = STATE_COMPLETED
        self.completed_levels.add(self.level_index)
        self.highest_unlocked_level = min(
            get_level_count() - 1,
            max(self.highest_unlocked_level, self.level_index + 1),
        )
        self._save_progress()
        self.sounds.play("complete")

    def _toggle_collection(self):
        if self.state == STATE_COLLECTION:
            self.state = self.previous_state
            return

        self.previous_state = self.state
        self.collection_scroll = 0
        self.state = STATE_COLLECTION

    def _save_progress(self):
        if self.temporary_session:
            return

        self.progress_store.save(
            self.highest_unlocked_level,
            self.collection_entries,
            self.completed_levels,
        )

    def _apply_progress(self, progress: dict):
        self.highest_unlocked_level = progress["highest_unlocked_level"]
        self.completed_levels = set(progress["completed_levels"])
        self.collection_entries = list(progress["collection_entries"])
        self.collection_entry_set = set(self.collection_entries)

    def _start_temporary_new_journey(self):
        self.temporary_session = True
        self._apply_progress(
            {
                "highest_unlocked_level": 0,
                "completed_levels": set(),
                "collection_entries": [],
            }
        )
        self.selected_level_index = 0
        self.level_select_scroll = 0
        self.collection_scroll = 0
        self._load_level(0, STATE_INTRO)

    def _sync_level_select_scroll(self):
        visible_rows = 7
        if self.selected_level_index < self.level_select_scroll:
            self.level_select_scroll = self.selected_level_index
        elif self.selected_level_index >= self.level_select_scroll + visible_rows:
            self.level_select_scroll = self.selected_level_index - visible_rows + 1

    def _collection_rows(self) -> list[tuple[str, str]]:
        rows = []
        entries_by_level: dict[str, list[str]] = {}
        for level_title, info in self.collection_entries:
            entries_by_level.setdefault(level_title, []).append(info)

        for index in range(get_level_count()):
            level_title = get_level_plain_title(index)
            entries = entries_by_level.get(level_title, [])
            if not entries:
                continue

            total = get_level_fragment_count(index)
            rows.append(("header", f"{get_level_title(index)} ({len(entries)}/{total})"))
            for info in entries:
                rows.append(("item", info))

        return rows

    def _draw(self):
        draw_background(self.screen, self.level.theme, self.camera_x, self.level.width)

        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_LEVEL_SELECT:
            self._draw_level_select()
        elif self.state == STATE_COLLECTION:
            self._draw_collection()
        elif self.state == STATE_FINAL:
            self._draw_final()
        else:
            self._draw_level()
            self._draw_hazards()
            self._draw_checkpoints()
            self._draw_fragments()
            self._draw_player()
            self._draw_hud()

        if self.state == STATE_INTRO:
            self._draw_intro()
        elif self.state == STATE_PAUSED:
            self._draw_pause()
        elif self.state == STATE_COMPLETED:
            self._draw_completion_message()

        pygame.display.flip()

    def _draw_level(self):
        for platform in self.level.platforms:
            color = GROUND_COLOR if platform.width >= self.level.width else PLATFORM_COLOR
            platform_rect = self._to_screen_rect(platform)
            pygame.draw.rect(self.screen, color, platform_rect)
            pygame.draw.rect(self.screen, (68, 82, 58), platform_rect, 2)
            if platform.width < self.level.width:
                pygame.draw.rect(
                    self.screen,
                    (174, 126, 78),
                    (platform_rect.x + 4, platform_rect.y + 4, platform_rect.width - 8, 5),
                )

        goal_rect = self._to_screen_rect(self.level.goal)
        goal_color = GOAL_COLOR if self._all_fragments_collected() else (130, 150, 135)
        pygame.draw.rect(self.screen, (64, 72, 58), (goal_rect.centerx - 3, goal_rect.y - 34, 6, 94))
        pygame.draw.rect(self.screen, goal_color, goal_rect)
        pygame.draw.polygon(
            self.screen,
            goal_color,
            [
                (goal_rect.centerx, goal_rect.y - 38),
                (goal_rect.centerx + 54, goal_rect.y - 20),
                (goal_rect.centerx, goal_rect.y - 2),
            ],
        )
        pygame.draw.rect(self.screen, (36, 92, 52), goal_rect, 3)

    def _draw_hazards(self):
        for hazard in self.level.hazards:
            hazard_rect = self._to_screen_rect(hazard)
            pygame.draw.rect(self.screen, HAZARD_COLOR, hazard_rect)
            pygame.draw.rect(self.screen, HAZARD_OUTLINE, hazard_rect, 2)

            stripe_x = hazard_rect.x + 8
            while stripe_x < hazard_rect.right:
                pygame.draw.line(
                    self.screen,
                    HAZARD_OUTLINE,
                    (stripe_x, hazard_rect.bottom - 2),
                    (stripe_x + 12, hazard_rect.y + 2),
                    2,
                )
                stripe_x += 22

    def _draw_checkpoints(self):
        for index, checkpoint in enumerate(self.level.checkpoints):
            checkpoint_rect = self._to_screen_rect(checkpoint)
            pole = pygame.Rect(
                checkpoint_rect.centerx - 2,
                checkpoint_rect.y + 8,
                4,
                checkpoint_rect.height - 8,
            )
            flag = pygame.Rect(checkpoint_rect.centerx, checkpoint_rect.y + 8, 28, 20)
            color = CHECKPOINT_COLOR if index in self.active_checkpoints else (150, 170, 185)

            pygame.draw.rect(self.screen, CHECKPOINT_OUTLINE, pole)
            pygame.draw.rect(self.screen, color, flag)
            pygame.draw.rect(self.screen, CHECKPOINT_OUTLINE, flag, 2)

    def _draw_fragments(self):
        for fragment in self.fragments:
            fragment_rect = self._to_screen_rect(fragment.rect)
            pygame.draw.ellipse(self.screen, FRAGMENT_COLOR, fragment_rect)
            pygame.draw.ellipse(self.screen, FRAGMENT_OUTLINE, fragment_rect, 2)

    def _draw_player(self):
        self.player.draw(self.screen, self.camera_x)

    def _to_screen_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-self.camera_x, 0)

    def _draw_hud(self):
        title = f"{self.level.year} - {self.level.title}"
        level_progress = f"Fase {self.level_index + 1}/{get_level_count()}"
        collected = self.total_fragments - len(self.fragments)
        fragments_text = f"Fragmentos historicos: {collected}/{self.total_fragments}"
        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        progress_surface = self.font.render(level_progress, True, TEXT_COLOR)
        mission_surface = self.font.render(self.level.mission, True, TEXT_COLOR)
        fragments_surface = self.font.render(fragments_text, True, TEXT_COLOR)

        title_box = pygame.Rect(16, 14, 690, 100)
        progress_box = pygame.Rect(SCREEN_WIDTH - 140, 18, 116, 34)
        pygame.draw.rect(self.screen, (248, 238, 190), title_box)
        pygame.draw.rect(self.screen, TEXT_COLOR, title_box, 2)
        pygame.draw.rect(self.screen, (248, 238, 190), progress_box)
        pygame.draw.rect(self.screen, TEXT_COLOR, progress_box, 2)

        self.screen.blit(title_surface, (32, 24))
        self.screen.blit(
            progress_surface,
            progress_surface.get_rect(center=progress_box.center),
        )
        self.screen.blit(mission_surface, (32, 66))
        self.screen.blit(fragments_surface, (32, 92))

        if self.fragment_message:
            self._draw_fragment_message()
        elif self.feedback_message:
            self._draw_feedback_message()

    def _draw_menu(self):
        self._draw_menu_scene()

        panel = pygame.Rect(560, 350, 360, 150)
        panel_surface = pygame.Surface(panel.size, pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            (248, 238, 190, 224),
            panel_surface.get_rect(),
            border_radius=8,
        )
        self.screen.blit(panel_surface, panel)
        pygame.draw.rect(self.screen, TEXT_COLOR, panel, 2, border_radius=8)

        start_surface = self.font.render("Enter: continuar", True, TEXT_COLOR)
        progress_text = f"Fases liberadas: {self.highest_unlocked_level + 1}/{get_level_count()}"
        if self.temporary_session:
            progress_text = "Nova jornada nesta sessao"
        progress_surface = self.font.render(progress_text, True, TEXT_COLOR)
        new_journey_surface = self.font.render("N: nova sessao", True, TEXT_COLOR)
        select_surface = self.font.render("S: linha do tempo", True, TEXT_COLOR)
        collection_surface = self.font.render("C: colecao", True, TEXT_COLOR)
        exit_surface = self.font.render("Esc: sair", True, TEXT_COLOR)

        self.screen.blit(start_surface, (panel.x + 18, panel.y + 14))
        self.screen.blit(new_journey_surface, (panel.x + 18, panel.y + 42))
        self.screen.blit(select_surface, (panel.x + 18, panel.y + 70))
        self.screen.blit(collection_surface, (panel.x + 18, panel.y + 98))
        self.screen.blit(exit_surface, (panel.x + 206, panel.y + 98))
        self.screen.blit(progress_surface, (panel.x + 18, panel.y + 122))

    def _draw_menu_scene(self):
        if self.menu_image:
            self.screen.blit(self.menu_image, (0, 0))
            return

        pygame.draw.rect(self.screen, (74, 154, 194), (0, 348, SCREEN_WIDTH, 82))
        pygame.draw.rect(self.screen, (232, 207, 132), (0, 430, SCREEN_WIDTH, 110))

        self._draw_menu_cloud(95, 88)
        self._draw_menu_cloud(390, 62)
        pygame.draw.circle(self.screen, (248, 220, 116), (812, 88), 38)

        self._draw_menu_history_path()

    def _draw_menu_cloud(self, x: int, y: int):
        pygame.draw.circle(self.screen, (242, 248, 250), (x, y), 22)
        pygame.draw.circle(self.screen, (242, 248, 250), (x + 28, y - 12), 28)
        pygame.draw.circle(self.screen, (242, 248, 250), (x + 62, y), 22)
        pygame.draw.rect(self.screen, (242, 248, 250), (x, y, 62, 22))

    def _draw_menu_history_path(self):
        points = [(58, 468), (154, 440), (258, 462), (364, 436), (424, 448)]
        pygame.draw.lines(self.screen, (96, 82, 64), False, points, 5)

        nodes = [
            ((58, 468), "1500", "ship"),
            ((154, 440), "acucar", "cane"),
            ((258, 462), "ouro", "mine"),
            ((364, 436), "hoje", "city"),
        ]
        for position, label, icon in nodes:
            pygame.draw.circle(self.screen, (248, 238, 190), position, 23)
            pygame.draw.circle(self.screen, TEXT_COLOR, position, 23, 2)
            self._draw_menu_history_icon(position, icon)
            label_surface = self.font.render(label, True, TEXT_COLOR)
            self.screen.blit(label_surface, label_surface.get_rect(center=(position[0], position[1] + 36)))

    def _draw_menu_history_icon(self, center: tuple[int, int], icon: str):
        x, y = center
        if icon == "ship":
            pygame.draw.polygon(self.screen, (100, 71, 48), [(x - 14, y + 8), (x + 16, y + 8), (x + 9, y + 16), (x - 8, y + 16)])
            pygame.draw.line(self.screen, (74, 52, 38), (x, y + 8), (x, y - 14), 3)
            pygame.draw.polygon(self.screen, (242, 238, 210), [(x + 3, y - 12), (x + 3, y + 4), (x + 16, y + 2)])
        elif icon == "cane":
            pygame.draw.line(self.screen, (64, 132, 70), (x - 5, y + 15), (x + 5, y - 15), 4)
            pygame.draw.line(self.screen, (92, 158, 82), (x + 4, y + 12), (x + 14, y - 12), 4)
        elif icon == "mine":
            pygame.draw.polygon(self.screen, (142, 122, 88), [(x - 17, y + 16), (x, y - 15), (x + 17, y + 16)])
            pygame.draw.rect(self.screen, (64, 58, 56), (x - 7, y + 2, 14, 14))
        else:
            pygame.draw.rect(self.screen, (126, 142, 154), (x - 14, y - 15, 28, 31))
            pygame.draw.rect(self.screen, (198, 226, 232), (x - 8, y - 9, 6, 6))
            pygame.draw.rect(self.screen, (198, 226, 232), (x + 4, y - 9, 6, 6))
            pygame.draw.rect(self.screen, (198, 226, 232), (x - 8, y + 3, 6, 6))
            pygame.draw.rect(self.screen, (198, 226, 232), (x + 4, y + 3, 6, 6))

    def _draw_menu_option(
        self,
        x: int,
        y: int,
        key_text: str,
        label_surface: pygame.Surface,
    ):
        key_box = pygame.Rect(x, y, 72, 32)
        pygame.draw.rect(self.screen, (226, 202, 128), key_box, border_radius=6)
        pygame.draw.rect(self.screen, TEXT_COLOR, key_box, 2, border_radius=6)
        key_surface = self.font.render(key_text, True, TEXT_COLOR)
        self.screen.blit(key_surface, key_surface.get_rect(center=key_box.center))
        self.screen.blit(label_surface, (x + 88, y + 6))

    def _draw_level_select(self):
        box = pygame.Rect(0, 0, 860, 440)
        box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render("Linha do tempo", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 46)))

        visible_rows = 7
        first_index = self.level_select_scroll
        last_index = min(get_level_count(), first_index + visible_rows)
        line_x = box.x + 58
        pygame.draw.line(
            self.screen,
            (128, 116, 86),
            (line_x, box.y + 92),
            (line_x, box.y + 92 + (visible_rows - 1) * 43),
            4,
        )

        for row_index, index in enumerate(range(first_index, last_index)):
            y = box.y + 82 + row_index * 43
            is_selected = index == self.selected_level_index
            is_unlocked = index <= self.highest_unlocked_level
            is_completed = index in self.completed_levels
            row = pygame.Rect(box.x + 84, y - 7, box.width - 124, 35)

            if is_selected:
                pygame.draw.rect(self.screen, (226, 202, 128), row)
                pygame.draw.rect(self.screen, TEXT_COLOR, row, 2)

            dot_color = (82, 150, 214) if is_unlocked else (132, 132, 132)
            if is_completed:
                dot_color = GOAL_COLOR
            pygame.draw.circle(self.screen, dot_color, (line_x, y + 10), 11)
            pygame.draw.circle(self.screen, TEXT_COLOR, (line_x, y + 10), 11, 2)

            if is_completed:
                status = "Concluida"
            elif is_unlocked:
                status = "Liberada"
            else:
                status = "Bloqueada"
            text = f"{index + 1:02d}. {get_level_title(index)}"
            color = TEXT_COLOR if is_unlocked else (112, 112, 112)
            surface = self.font.render(text, True, color)
            status_surface = self.font.render(status, True, color)
            self.screen.blit(surface, (row.x + 14, row.y + 7))
            self.screen.blit(
                status_surface,
                status_surface.get_rect(midright=(row.right - 12, row.centery)),
            )

        if first_index > 0:
            up_surface = self.font.render("^", True, TEXT_COLOR)
            self.screen.blit(up_surface, up_surface.get_rect(center=(box.right - 34, box.y + 82)))
        if last_index < get_level_count():
            down_surface = self.font.render("v", True, TEXT_COLOR)
            self.screen.blit(down_surface, down_surface.get_rect(center=(box.right - 34, box.bottom - 78)))

        if self.feedback_message and self.feedback_message_timer > 0:
            feedback_surface = self.font.render(self.feedback_message, True, (116, 70, 42))
            self.screen.blit(
                feedback_surface,
                feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 60)),
            )

        help_surface = self.font.render(
            "Setas escolhem | Enter inicia | M volta ao menu",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 28)))

    def _draw_fragment_message(self):
        box = pygame.Rect(24, 126, 710, 68)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        for index, line in enumerate(self._wrap_text(self.fragment_message, 64)):
            line_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(line_surface, (box.x + 16, box.y + 14 + index * 24))

    def _draw_feedback_message(self):
        box = pygame.Rect(24, 126, 710, 44)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        message_surface = self.font.render(self.feedback_message, True, TEXT_COLOR)
        self.screen.blit(message_surface, (box.x + 16, box.y + 12))

    def _draw_pause(self):
        box = pygame.Rect(0, 0, 520, 220)
        box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render("Pausado", True, TEXT_COLOR)
        resume_surface = self.font.render("P ou Enter continua", True, TEXT_COLOR)
        restart_surface = self.font.render("R reinicia | M volta ao menu", True, TEXT_COLOR)
        collection_surface = self.font.render("C abre a colecao historica", True, TEXT_COLOR)

        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 50)))
        self.screen.blit(resume_surface, resume_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 100)))
        self.screen.blit(restart_surface, restart_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 138)))
        self.screen.blit(collection_surface, collection_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 176)))

    def _draw_collection(self):
        box = pygame.Rect(0, 0, 860, 440)
        box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render("Colecao historica", True, TEXT_COLOR)
        collected_count = len(self.collection_entries)
        total_count = get_total_fragment_count()
        count_surface = self.font.render(
            f"Fragmentos coletados: {collected_count}/{total_count}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 38)))
        self.screen.blit(count_surface, count_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 70)))

        if not self.collection_entries:
            empty_surface = self.font.render(
                "Colete fragmentos durante as fases para preencher esta tela.",
                True,
                TEXT_COLOR,
            )
            self.screen.blit(empty_surface, empty_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        else:
            rows = self._collection_rows()
            visible_rows = rows[self.collection_scroll : self.collection_scroll + 8]
            y = box.y + 96
            for row_type, text in visible_rows:
                if row_type == "header":
                    surface = self.font.render(text, True, TEXT_COLOR)
                    pygame.draw.circle(self.screen, GOAL_COLOR, (box.x + 34, y + 12), 7)
                    self.screen.blit(surface, (box.x + 52, y))
                    y += 30
                else:
                    for line in self._wrap_text(text, 82)[:2]:
                        surface = self.font.render(line, True, (64, 68, 72))
                        self.screen.blit(surface, (box.x + 72, y))
                        y += 22
                    y += 4

        help_surface = self.font.render(
            "Setas rolam | C, Enter ou M volta",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 28)))

    def _draw_intro(self):
        box = pygame.Rect(70, SCREEN_HEIGHT - 195, SCREEN_WIDTH - 140, 150)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        speaker_surface = self.font.render("Mig", True, TEXT_COLOR)
        self.screen.blit(speaker_surface, (box.x + 22, box.y + 18))

        for index, line in enumerate(self._wrap_text(self.level.intro_text, 68)):
            line_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(line_surface, (box.x + 22, box.y + 54 + index * 26))

        continue_surface = self.font.render("Pressione Enter para iniciar.", True, TEXT_COLOR)
        self.screen.blit(
            continue_surface,
            continue_surface.get_rect(bottomright=(box.right - 22, box.bottom - 16)),
        )

    def _draw_completion_message(self):
        title = "Fase concluida!"
        subtitle = "Mig encontrou um ponto seguro de observacao."
        if self.level_index + 1 >= get_level_count():
            restart = "Enter abre o final | R reinicia | C abre colecao."
        else:
            restart = "Enter avanca | R reinicia | C abre colecao."

        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        subtitle_surface = self.font.render(subtitle, True, TEXT_COLOR)
        restart_surface = self.font.render(restart, True, TEXT_COLOR)

        box = pygame.Rect(0, 0, 800, 170)
        box.center = (SCREEN_WIDTH // 2, 155)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, 105)))
        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 142)),
        )
        for index, line in enumerate(self._wrap_text(self.level.historical_note, 78)[:2]):
            note_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(note_surface, note_surface.get_rect(center=(SCREEN_WIDTH // 2, 172 + index * 24)))
        self.screen.blit(
            restart_surface,
            restart_surface.get_rect(center=(SCREEN_WIDTH // 2, 222)),
        )

    def _draw_final(self):
        box = pygame.Rect(0, 0, 820, 350)
        box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render("Jornada concluida!", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 52)))

        lines = [
            "Mig viajou de 1500 ate o Brasil contemporaneo.",
            "A historia do Brasil continua sendo estudada, contada e vivida.",
            "Cada fragmento lembra que aprender historia pede curiosidade e respeito.",
        ]
        for index, line in enumerate(lines):
            surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 110 + index * 34)))

        collected_surface = self.font.render(
            f"Colecao: {len(self.collection_entries)}/{get_total_fragment_count()} fragmentos",
            True,
            TEXT_COLOR,
        )
        credits_surface = self.font.render(
            "Creditos: jogo educativo criado com Python, Pygame-CE e carinho pelo aprendizado.",
            True,
            TEXT_COLOR,
        )
        help_surface = self.font.render(
            "Enter ou M volta ao menu | C abre colecao | R revisita a ultima fase",
            True,
            TEXT_COLOR,
        )

        self.screen.blit(collected_surface, collected_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 226)))
        self.screen.blit(credits_surface, credits_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 268)))
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 314)))

    def _wrap_text(self, text: str, max_chars: int) -> list[str]:
        lines = []
        current_line = ""

        for word in text.split():
            test_line = f"{current_line} {word}".strip()
            if len(test_line) <= max_chars:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
