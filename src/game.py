import asyncio
from math import cos, pi, sin
from random import Random

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
    PLAYER_DRAW_SIZE,
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
STATE_HELP = "help"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 44)
        self.medium_font = pygame.font.Font(None, 38)
        self.sounds = SoundManager()
        self.menu_image = self._load_menu_image()
        self.progress_store = ProgressStore(get_level_count())
        self.saved_progress = self.progress_store.load()
        self.temporary_session = False
        self.random = Random(2018)
        self.touch_ui_enabled = False
        self.touch_control_by_pointer = {}
        self.active_touch_controls = set()
        self.touch_jump_pressed = False
        self.pointer_starts = {}

        self.selected_level_index = 0
        self.level_select_scroll = 0
        self.collection_scroll = 0
        self.previous_state = STATE_MENU
        self.animation_time = 0
        self.effects = []
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
            elif event.type == pygame.FINGERDOWN:
                self._handle_pointer_down(
                    self._finger_event_position(event),
                    ("finger", event.finger_id),
                    is_touch=True,
                )
            elif event.type == pygame.FINGERMOTION:
                self._handle_pointer_motion(
                    self._finger_event_position(event),
                    ("finger", event.finger_id),
                    is_touch=True,
                )
            elif event.type == pygame.FINGERUP:
                self._handle_pointer_up(
                    self._finger_event_position(event),
                    ("finger", event.finger_id),
                    is_touch=True,
                )
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not getattr(event, "touch", False):
                    self._handle_pointer_down(event.pos, ("mouse", 0), is_touch=False)
            elif event.type == pygame.MOUSEMOTION:
                if not getattr(event, "touch", False) and ("mouse", 0) in self.pointer_starts:
                    self._handle_pointer_motion(event.pos, ("mouse", 0), is_touch=False)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not getattr(event, "touch", False):
                    self._handle_pointer_up(event.pos, ("mouse", 0), is_touch=False)

    def _finger_event_position(self, event: pygame.event.Event) -> tuple[int, int]:
        return (
            int(max(0, min(1, event.x)) * SCREEN_WIDTH),
            int(max(0, min(1, event.y)) * SCREEN_HEIGHT),
        )

    def _handle_pointer_down(
        self,
        position: tuple[int, int],
        pointer_id,
        is_touch: bool = True,
    ):
        self.touch_ui_enabled = True
        self.pointer_starts[pointer_id] = {
            "position": position,
            "last_position": position,
            "state": self.state,
            "drag": 0,
            "scroll_remainder": 0,
        }

        if self.state == STATE_PLAYING:
            action = self._gameplay_touch_action_at(position)
            if action in ("left", "right", "jump"):
                self._set_touch_control(pointer_id, action)
            elif action == "pause":
                self._clear_touch_controls()
                self.state = STATE_PAUSED
            elif action == "collection":
                self._clear_touch_controls()
                self._toggle_collection()

    def _handle_pointer_motion(
        self,
        position: tuple[int, int],
        pointer_id,
        is_touch: bool = True,
    ):
        if pointer_id in self.touch_control_by_pointer:
            action = self._gameplay_touch_action_at(position)
            if action in ("left", "right", "jump"):
                self._set_touch_control(pointer_id, action)
            else:
                self._remove_touch_control(pointer_id)

        start = self.pointer_starts.get(pointer_id)
        if not start:
            return

        last_x, last_y = start["last_position"]
        start["last_position"] = position
        start["drag"] += abs(position[0] - last_x) + abs(position[1] - last_y)

        if start["state"] == STATE_COLLECTION and self.state == STATE_COLLECTION:
            self._scroll_collection_from_drag(start, position[1] - last_y)
        elif start["state"] == STATE_LEVEL_SELECT and self.state == STATE_LEVEL_SELECT:
            self._scroll_level_select_from_drag(start, position[1] - last_y)

    def _handle_pointer_up(
        self,
        position: tuple[int, int],
        pointer_id,
        is_touch: bool = True,
    ):
        was_control = pointer_id in self.touch_control_by_pointer
        self._remove_touch_control(pointer_id)

        start = self.pointer_starts.pop(pointer_id, None)
        if was_control or not start:
            return
        if start["drag"] > 24:
            return
        if start["state"] != self.state:
            return

        self._handle_tap(position, start["state"])

    def _set_touch_control(self, pointer_id, action: str):
        previous_action = self.touch_control_by_pointer.get(pointer_id)
        self.touch_control_by_pointer[pointer_id] = action
        if action == "jump" and previous_action != "jump":
            self.touch_jump_pressed = True
        self._refresh_active_touch_controls()

    def _remove_touch_control(self, pointer_id):
        if pointer_id in self.touch_control_by_pointer:
            del self.touch_control_by_pointer[pointer_id]
            self._refresh_active_touch_controls()

    def _clear_touch_controls(self):
        self.touch_control_by_pointer.clear()
        self.active_touch_controls.clear()
        self.touch_jump_pressed = False

    def _refresh_active_touch_controls(self):
        self.active_touch_controls = set(self.touch_control_by_pointer.values())

    def _touch_direction(self) -> int:
        moving_left = "left" in self.active_touch_controls
        moving_right = "right" in self.active_touch_controls
        if moving_left and not moving_right:
            return -1
        if moving_right and not moving_left:
            return 1
        return 0

    def _handle_tap(self, position: tuple[int, int], state: str):
        if state == STATE_MENU:
            self._handle_menu_tap(position)
        elif state == STATE_LEVEL_SELECT:
            self._handle_level_select_tap(position)
        elif state == STATE_INTRO:
            if self._intro_box_rect().collidepoint(position):
                self.state = STATE_PLAYING
        elif state == STATE_PAUSED:
            self._handle_pause_tap(position)
        elif state == STATE_COMPLETED:
            if self._completion_box_rect().collidepoint(position):
                self._go_to_next_level()
        elif state == STATE_FINAL:
            if self._final_box_rect().collidepoint(position):
                self.state = STATE_MENU
        elif state == STATE_COLLECTION:
            if self._collection_back_button_rect().collidepoint(position):
                self.state = self.previous_state
        elif state == STATE_HELP:
            if self._help_box_rect().collidepoint(position):
                self.state = self.previous_state

    def _handle_menu_tap(self, position: tuple[int, int]):
        action = self._menu_touch_action_at(position)
        if action == "continue":
            self._handle_menu_keydown(pygame.K_RETURN)
        elif action == "new":
            self._handle_menu_keydown(pygame.K_n)
        elif action == "timeline":
            self._handle_menu_keydown(pygame.K_s)
        elif action == "collection":
            self._toggle_collection()
        elif action == "help":
            self._toggle_help()
        elif action == "exit":
            self.running = False

    def _handle_level_select_tap(self, position: tuple[int, int]):
        scroll_action = self._level_select_scroll_action_at(position)
        if scroll_action == "up":
            self._handle_level_select_keydown(pygame.K_UP)
            return
        if scroll_action == "down":
            self._handle_level_select_keydown(pygame.K_DOWN)
            return

        selected_index = self._level_select_index_at(position)
        if selected_index is None:
            return

        self.selected_level_index = selected_index
        if selected_index <= self.highest_unlocked_level:
            self.sounds.play("menu")
            self._load_level(selected_index, STATE_INTRO)
        else:
            self.feedback_message = "Essa fase ainda esta bloqueada. Conclua as anteriores primeiro."
            self.feedback_message_timer = 2.5
            self.sounds.play("blocked")

    def _handle_pause_tap(self, position: tuple[int, int]):
        action = self._pause_touch_action_at(position)
        if action == "resume":
            self.state = STATE_PLAYING
        elif action == "restart":
            self._restart_level()
        elif action == "menu":
            self.state = STATE_MENU
        elif self._pause_box_rect().collidepoint(position):
            self.state = STATE_PLAYING

    def _scroll_collection_from_drag(self, start: dict, delta_y: int):
        max_scroll = max(0, len(self._collection_rows()) - 8)
        self._scroll_from_drag(start, delta_y, max_scroll, "collection_scroll")

    def _scroll_level_select_from_drag(self, start: dict, delta_y: int):
        max_scroll = max(0, get_level_count() - 7)
        self._scroll_from_drag(start, delta_y, max_scroll, "level_select_scroll")
        self.selected_level_index = max(
            self.level_select_scroll,
            min(self.selected_level_index, self.level_select_scroll + 6),
        )

    def _scroll_from_drag(
        self,
        start: dict,
        delta_y: int,
        max_scroll: int,
        attribute_name: str,
    ):
        start["scroll_remainder"] += delta_y
        while start["scroll_remainder"] <= -34:
            setattr(self, attribute_name, min(max_scroll, getattr(self, attribute_name) + 1))
            start["scroll_remainder"] += 34
        while start["scroll_remainder"] >= 34:
            setattr(self, attribute_name, max(0, getattr(self, attribute_name) - 1))
            start["scroll_remainder"] -= 34

    def _handle_keydown(self, key: int):
        if key == pygame.K_ESCAPE:
            self.running = False
            return

        if key == pygame.K_c:
            self._toggle_collection()
            return

        if key == pygame.K_h and self.state != STATE_COLLECTION:
            self._toggle_help()
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
        elif self.state == STATE_HELP:
            self._handle_help_keydown(key)

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

    def _handle_help_keydown(self, key: int):
        if key in (pygame.K_h, pygame.K_m, pygame.K_RETURN):
            self.state = self.previous_state

    def _update(self, dt: float):
        self.animation_time += dt
        self._update_effects(dt)

        if self.state != STATE_PLAYING:
            self._update_feedback_message(dt)
            return

        keys = pygame.key.get_pressed()
        touch_jump_pressed = self.touch_jump_pressed
        self.touch_jump_pressed = False
        self.player.handle_input(
            keys,
            dt,
            touch_direction=self._touch_direction(),
            touch_jump_held="jump" in self.active_touch_controls,
            touch_jump_pressed=touch_jump_pressed,
        )
        if self.player.jump_started:
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

        if self.player.rect.colliderect(self.level.goal):
            if self._all_fragments_collected():
                self._complete_level()
            else:
                self._show_goal_feedback()

    def _collect_fragments(self):
        remaining_fragments = []
        collected_any = False

        for fragment in self.fragments:
            if self.player.rect.colliderect(fragment.rect):
                collected_any = True
                self.fragment_message = f"Voce sabia? {fragment.info}"
                self.fragment_message_timer = 4
                self._spawn_effect_burst(
                    fragment.rect.center,
                    FRAGMENT_COLOR,
                    count=14,
                    radius=4,
                )
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
            self._spawn_effect_burst(
                checkpoint.midtop,
                CHECKPOINT_COLOR,
                count=16,
                radius=4,
            )
            self.sounds.play("checkpoint")

    def _all_fragments_collected(self) -> bool:
        return len(self.fragments) == 0

    def _show_goal_feedback(self):
        if self.feedback_message_timer > 0:
            return

        remaining = len(self.fragments)
        plural = "s" if remaining != 1 else ""
        self.feedback_message = f"Falta coletar {remaining} fragmento{plural} antes de atravessar o portal."
        self.feedback_message_timer = 2.4
        self.sounds.play("blocked")

    def _spawn_effect_burst(
        self,
        position: tuple[int, int],
        color: tuple[int, int, int],
        count: int,
        radius: int,
    ):
        x, y = position
        for index in range(count):
            angle = (pi * 2 * index / count) + self.random.uniform(-0.18, 0.18)
            speed = self.random.uniform(48, 128)
            self.effects.append(
                {
                    "x": float(x),
                    "y": float(y),
                    "vx": cos(angle) * speed,
                    "vy": sin(angle) * speed - self.random.uniform(20, 80),
                    "age": 0.0,
                    "duration": self.random.uniform(0.42, 0.72),
                    "color": color,
                    "radius": radius,
                }
            )

        if len(self.effects) > 120:
            self.effects = self.effects[-120:]

    def _update_effects(self, dt: float):
        active_effects = []
        for effect in self.effects:
            effect["age"] += dt
            if effect["age"] >= effect["duration"]:
                continue

            effect["x"] += effect["vx"] * dt
            effect["y"] += effect["vy"] * dt
            effect["vy"] += 190 * dt
            active_effects.append(effect)

        self.effects = active_effects

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
        self.effects = []
        self.camera_x = 0
        self._clear_touch_controls()
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
        self._spawn_effect_burst(
            self.level.goal.center,
            GOAL_COLOR,
            count=28,
            radius=5,
        )
        self.sounds.play("complete")

    def _toggle_collection(self):
        if self.state == STATE_COLLECTION:
            self.state = self.previous_state
            return

        self.previous_state = self.state
        self.collection_scroll = 0
        self.state = STATE_COLLECTION

    def _toggle_help(self):
        if self.state == STATE_HELP:
            self.state = self.previous_state
            return

        self.previous_state = self.state
        self.state = STATE_HELP

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

    def _centered_rect(self, width: int, height: int) -> pygame.Rect:
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        return rect

    def _menu_panel_rect(self) -> pygame.Rect:
        return pygame.Rect(548, 302, 382, 190)

    def _menu_touch_actions(self) -> list[tuple[str, pygame.Rect]]:
        panel = self._menu_panel_rect()
        return [
            ("continue", pygame.Rect(panel.x + 12, panel.y + 8, panel.width - 24, 28)),
            ("new", pygame.Rect(panel.x + 12, panel.y + 36, panel.width - 24, 28)),
            ("timeline", pygame.Rect(panel.x + 12, panel.y + 64, panel.width - 24, 28)),
            ("collection", pygame.Rect(panel.x + 12, panel.y + 92, 176, 28)),
            ("help", pygame.Rect(panel.x + 194, panel.y + 92, 176, 28)),
            ("exit", pygame.Rect(panel.x + 12, panel.y + 120, panel.width - 24, 28)),
        ]

    def _menu_touch_action_at(self, position: tuple[int, int]) -> str | None:
        for action, rect in self._menu_touch_actions():
            if rect.collidepoint(position):
                return action
        return None

    def _touch_control_rects(self) -> dict[str, pygame.Rect]:
        return {
            "left": pygame.Rect(24, SCREEN_HEIGHT - 112, 86, 82),
            "right": pygame.Rect(122, SCREEN_HEIGHT - 112, 86, 82),
            "jump": pygame.Rect(SCREEN_WIDTH - 136, SCREEN_HEIGHT - 124, 108, 96),
            "pause": pygame.Rect(SCREEN_WIDTH - 134, 62, 50, 42),
            "collection": pygame.Rect(SCREEN_WIDTH - 74, 62, 50, 42),
        }

    def _gameplay_touch_action_at(self, position: tuple[int, int]) -> str | None:
        for action, rect in self._touch_control_rects().items():
            if rect.collidepoint(position):
                return action
        return None

    def _level_select_box_rect(self) -> pygame.Rect:
        return self._centered_rect(860, 440)

    def _level_select_row_rects(self) -> list[tuple[int, pygame.Rect]]:
        box = self._level_select_box_rect()
        first_index = self.level_select_scroll
        last_index = min(get_level_count(), first_index + 7)
        rows = []
        for row_index, index in enumerate(range(first_index, last_index)):
            y = box.y + 82 + row_index * 43
            rows.append((index, pygame.Rect(box.x + 84, y - 7, box.width - 124, 35)))
        return rows

    def _level_select_index_at(self, position: tuple[int, int]) -> int | None:
        for index, rect in self._level_select_row_rects():
            if rect.collidepoint(position):
                return index
        return None

    def _level_select_scroll_action_at(self, position: tuple[int, int]) -> str | None:
        box = self._level_select_box_rect()
        if pygame.Rect(box.right - 62, box.y + 58, 56, 56).collidepoint(position):
            return "up"
        if pygame.Rect(box.right - 62, box.bottom - 106, 56, 56).collidepoint(position):
            return "down"
        return None

    def _collection_box_rect(self) -> pygame.Rect:
        return self._centered_rect(860, 440)

    def _collection_back_button_rect(self) -> pygame.Rect:
        box = self._collection_box_rect()
        return pygame.Rect(box.right - 116, box.y + 18, 88, 34)

    def _intro_box_rect(self) -> pygame.Rect:
        return pygame.Rect(70, SCREEN_HEIGHT - 195, SCREEN_WIDTH - 140, 150)

    def _pause_box_rect(self) -> pygame.Rect:
        return self._centered_rect(520, 244)

    def _pause_touch_actions(self) -> list[tuple[str, pygame.Rect]]:
        box = self._pause_box_rect()
        return [
            ("resume", pygame.Rect(box.x + 64, box.y + 82, box.width - 128, 34)),
            ("restart", pygame.Rect(box.x + 64, box.y + 124, box.width - 128, 34)),
            ("menu", pygame.Rect(box.x + 64, box.y + 166, box.width - 128, 34)),
        ]

    def _pause_touch_action_at(self, position: tuple[int, int]) -> str | None:
        for action, rect in self._pause_touch_actions():
            if rect.collidepoint(position):
                return action
        return None

    def _help_box_rect(self) -> pygame.Rect:
        return self._centered_rect(780, 420)

    def _completion_box_rect(self) -> pygame.Rect:
        box = pygame.Rect(0, 0, 820, 208)
        box.center = (SCREEN_WIDTH // 2, 168)
        return box

    def _final_box_rect(self) -> pygame.Rect:
        return self._centered_rect(840, 380)

    def _collection_rows(self) -> list[tuple[str, str]]:
        rows = []
        entries_by_level: dict[str, list[str]] = {}
        for level_title, info in self.collection_entries:
            entries_by_level.setdefault(level_title, []).append(info)

        for index in range(get_level_count()):
            level_title = get_level_plain_title(index)
            entries = entries_by_level.get(level_title, [])

            total = get_level_fragment_count(index)
            rows.append(("header", f"{index + 1:02d}. {get_level_title(index)} ({min(len(entries), total)}/{total})"))
            for info in entries:
                rows.append(("item", info))
            if not entries:
                rows.append(("empty", "Ainda sem fragmentos coletados nesta fase."))

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
        elif self.state == STATE_HELP:
            self._draw_help()
        else:
            self._draw_level()
            self._draw_hazards()
            self._draw_checkpoints()
            self._draw_fragments()
            self._draw_effects()
            self._draw_player()
            self._draw_hud()
            if self.state == STATE_PLAYING and self.touch_ui_enabled:
                self._draw_touch_controls()

        if self.state == STATE_INTRO:
            self._draw_intro()
        elif self.state == STATE_PAUSED:
            self._draw_pause()
        elif self.state == STATE_COMPLETED:
            self._draw_completion_message()

        pygame.display.flip()

    def _draw_level(self):
        for platform in self.level.platforms:
            base_color, top_color, outline_color = self._platform_palette(platform)
            platform_rect = self._to_screen_rect(platform)
            pygame.draw.rect(self.screen, base_color, platform_rect)
            pygame.draw.rect(self.screen, outline_color, platform_rect, 2)
            pygame.draw.rect(
                self.screen,
                top_color,
                (platform_rect.x, platform_rect.y, platform_rect.width, min(8, platform_rect.height)),
            )
            if platform.width < self.level.width:
                for marker_x in range(platform_rect.x + 18, platform_rect.right - 12, 34):
                    pygame.draw.circle(self.screen, top_color, (marker_x, platform_rect.y + 4), 3)

        goal_rect = self._to_screen_rect(self.level.goal)
        unlocked = self._all_fragments_collected()
        pulse = 4 + int(sin(self.animation_time * 4) * 3)
        outer_color = GOAL_COLOR if unlocked else (132, 150, 138)
        inner_color = (168, 236, 156) if unlocked else (196, 204, 188)
        outline_color = (36, 92, 52) if unlocked else (84, 94, 82)
        portal_outer = goal_rect.inflate(28 + pulse, 42 + pulse)
        portal_inner = goal_rect.inflate(10, 20)

        pygame.draw.rect(
            self.screen,
            (94, 76, 56),
            (goal_rect.centerx - 33, goal_rect.bottom - 8, 66, 12),
            border_radius=3,
        )
        pygame.draw.ellipse(self.screen, outer_color, portal_outer, 6)
        pygame.draw.ellipse(self.screen, inner_color, portal_inner)
        pygame.draw.ellipse(self.screen, outline_color, portal_inner, 3)
        pygame.draw.rect(self.screen, outline_color, goal_rect.inflate(8, 0), 2, border_radius=4)

        if unlocked:
            for index in range(6):
                angle = self.animation_time * 2.8 + index * (pi / 3)
                sparkle_x = goal_rect.centerx + int(cos(angle) * 36)
                sparkle_y = goal_rect.centery + int(sin(angle) * 30)
                pygame.draw.circle(self.screen, (248, 238, 126), (sparkle_x, sparkle_y), 3)
        else:
            lock_box = pygame.Rect(0, 0, 22, 18)
            lock_box.center = goal_rect.center
            pygame.draw.rect(self.screen, (94, 100, 92), lock_box, border_radius=4)
            pygame.draw.arc(
                self.screen,
                (94, 100, 92),
                (lock_box.x + 4, lock_box.y - 10, 14, 18),
                pi,
                pi * 2,
                3,
            )

    def _platform_palette(
        self,
        platform: pygame.Rect,
    ) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
        if platform.width >= self.level.width:
            return GROUND_COLOR, (116, 160, 86), (62, 86, 54)

        palettes = {
            "coast": ((154, 118, 72), (224, 194, 112), (92, 72, 54)),
            "sugar": ((128, 96, 58), (92, 158, 82), (70, 84, 50)),
            "interior": ((118, 94, 64), (72, 138, 78), (62, 82, 54)),
            "mines": ((116, 104, 92), (172, 154, 112), (72, 70, 66)),
            "colonial_city": ((154, 118, 82), (226, 202, 128), (86, 66, 52)),
            "court": ((160, 122, 88), (226, 202, 128), (86, 66, 52)),
            "independence": ((138, 108, 72), (126, 176, 92), (70, 92, 56)),
            "empire": ((142, 116, 92), (196, 178, 140), (76, 66, 60)),
            "republic": ((130, 124, 104), (206, 196, 156), (74, 74, 66)),
            "rural_republic": ((126, 96, 58), (96, 142, 72), (66, 76, 48)),
            "vargas": ((116, 116, 112), (170, 180, 178), (70, 74, 74)),
            "democracy": ((118, 126, 104), (190, 206, 146), (70, 82, 64)),
            "dictatorship": ((106, 112, 116), (154, 158, 150), (62, 66, 70)),
            "redemocratization": ((112, 124, 104), (134, 184, 128), (60, 86, 66)),
            "contemporary": ((112, 122, 126), (156, 210, 198), (58, 78, 82)),
        }
        return palettes.get(self.level.theme, (PLATFORM_COLOR, (174, 126, 78), (68, 82, 58)))

    def _draw_hazards(self):
        for hazard in self.level.hazards:
            hazard_rect = self._to_screen_rect(hazard)
            warning_top = hazard_rect.y - 24
            warning_color = (246, 190, 86)

            for marker_x in range(hazard_rect.x + 12, hazard_rect.right - 4, 34):
                pygame.draw.polygon(
                    self.screen,
                    warning_color,
                    [
                        (marker_x, warning_top),
                        (marker_x - 10, warning_top + 18),
                        (marker_x + 10, warning_top + 18),
                    ],
                )
                pygame.draw.polygon(
                    self.screen,
                    HAZARD_OUTLINE,
                    [
                        (marker_x, warning_top),
                        (marker_x - 10, warning_top + 18),
                        (marker_x + 10, warning_top + 18),
                    ],
                    2,
                )

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
            color = CHECKPOINT_COLOR if index in self.active_checkpoints else (150, 170, 185)
            wave = int(sin(self.animation_time * 5 + index) * 3)
            flag_points = [
                (checkpoint_rect.centerx, checkpoint_rect.y + 8),
                (checkpoint_rect.centerx + 32, checkpoint_rect.y + 10 + wave),
                (checkpoint_rect.centerx + 26, checkpoint_rect.y + 28 + wave),
                (checkpoint_rect.centerx, checkpoint_rect.y + 26),
            ]

            pygame.draw.rect(self.screen, CHECKPOINT_OUTLINE, pole)
            pygame.draw.circle(self.screen, CHECKPOINT_OUTLINE, pole.midtop, 4)
            pygame.draw.polygon(self.screen, color, flag_points)
            pygame.draw.lines(self.screen, CHECKPOINT_OUTLINE, True, flag_points, 2)
            pygame.draw.rect(
                self.screen,
                (226, 202, 128),
                (checkpoint_rect.centerx - 12, checkpoint_rect.bottom - 7, 24, 7),
                border_radius=3,
            )

            if index in self.active_checkpoints:
                pygame.draw.circle(
                    self.screen,
                    (208, 236, 250),
                    (checkpoint_rect.centerx + 42, checkpoint_rect.y + 18 + wave),
                    4,
                )

    def _draw_fragments(self):
        for fragment in self.fragments:
            fragment_rect = self._to_screen_rect(fragment.rect)
            float_y = int(sin(self.animation_time * 4 + fragment.rect.x * 0.02) * 5)
            fragment_rect.y += float_y
            center = fragment_rect.center
            glow_radius = 18 + int(sin(self.animation_time * 5 + fragment.rect.x) * 3)

            pygame.draw.circle(self.screen, (252, 230, 132), center, glow_radius, 2)
            pygame.draw.ellipse(self.screen, FRAGMENT_COLOR, fragment_rect)
            pygame.draw.ellipse(self.screen, FRAGMENT_OUTLINE, fragment_rect, 2)
            pygame.draw.line(
                self.screen,
                (255, 248, 190),
                (center[0], fragment_rect.y + 4),
                (center[0], fragment_rect.bottom - 4),
                2,
            )
            pygame.draw.line(
                self.screen,
                (255, 248, 190),
                (fragment_rect.x + 4, center[1]),
                (fragment_rect.right - 4, center[1]),
                2,
            )

    def _draw_effects(self):
        for effect in self.effects:
            progress = effect["age"] / effect["duration"]
            radius = max(1, int(effect["radius"] * (1 - progress)))
            x = int(effect["x"] - self.camera_x)
            y = int(effect["y"])
            pygame.draw.circle(self.screen, effect["color"], (x, y), radius)

    def _draw_player(self):
        self.player.draw(self.screen, self.camera_x)

    def _to_screen_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-self.camera_x, 0)

    def _draw_hud(self):
        title = f"{self.level.year} - {self.level.title}"
        level_progress = f"Fase {self.level_index + 1}/{get_level_count()}"
        collected = self.total_fragments - len(self.fragments)
        fragments_text = f"Fragmentos historicos: {collected}/{self.total_fragments}"

        title_box = pygame.Rect(16, 14, 690, 100)
        progress_box = pygame.Rect(SCREEN_WIDTH - 140, 18, 116, 34)
        title_surface = self._render_fitting_text(
            title,
            TEXT_COLOR,
            title_box.width - 32,
            [self.big_font, self.medium_font],
        )
        progress_surface = self.font.render(level_progress, True, TEXT_COLOR)
        mission_surface = self.font.render(self.level.mission, True, TEXT_COLOR)
        fragments_surface = self.font.render(fragments_text, True, TEXT_COLOR)

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
        elif self._all_fragments_collected():
            self._draw_feedback_message("Portal liberado! Agora encontre o marco final.")

        if self.level_index == 0 and self.state == STATE_PLAYING and not self.touch_ui_enabled:
            self._draw_tutorial_hints()

    def _draw_menu(self):
        self._draw_menu_scene()

        panel = self._menu_panel_rect()
        panel_surface = pygame.Surface(panel.size, pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            (248, 238, 190, 224),
            panel_surface.get_rect(),
            border_radius=8,
        )
        self.screen.blit(panel_surface, panel)
        pygame.draw.rect(self.screen, TEXT_COLOR, panel, 2, border_radius=8)
        for _, row in self._menu_touch_actions():
            pygame.draw.rect(self.screen, (248, 238, 190), row, border_radius=5)
            pygame.draw.rect(self.screen, (128, 116, 86), row, 1, border_radius=5)

        start_surface = self.font.render("Enter: continuar", True, TEXT_COLOR)
        progress_text = f"Fases liberadas: {self.highest_unlocked_level + 1}/{get_level_count()}"
        if self.temporary_session:
            progress_text = "Nova jornada nesta sessao"
        progress_surface = self.font.render(progress_text, True, TEXT_COLOR)
        new_journey_surface = self.font.render("N: nova sessao", True, TEXT_COLOR)
        select_surface = self.font.render("S: linha do tempo", True, TEXT_COLOR)
        collection_surface = self.font.render("C: colecao", True, TEXT_COLOR)
        help_surface = self.font.render("H: ajuda", True, TEXT_COLOR)
        exit_surface = self.font.render("Esc: sair", True, TEXT_COLOR)

        self.screen.blit(start_surface, (panel.x + 18, panel.y + 12))
        self.screen.blit(new_journey_surface, (panel.x + 18, panel.y + 40))
        self.screen.blit(select_surface, (panel.x + 18, panel.y + 68))
        self.screen.blit(collection_surface, (panel.x + 18, panel.y + 96))
        self.screen.blit(help_surface, (panel.x + 206, panel.y + 96))
        self.screen.blit(exit_surface, (panel.x + 18, panel.y + 124))
        self.screen.blit(progress_surface, (panel.x + 18, panel.y + 154))

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
        box = self._level_select_box_rect()
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

        for row_index, (index, row) in enumerate(self._level_select_row_rects()):
            y = box.y + 82 + row_index * 43
            is_selected = index == self.selected_level_index
            is_unlocked = index <= self.highest_unlocked_level
            is_completed = index in self.completed_levels
            is_next = is_unlocked and not is_completed and index == self.highest_unlocked_level

            if is_selected:
                pygame.draw.rect(self.screen, (226, 202, 128), row)
                pygame.draw.rect(self.screen, TEXT_COLOR, row, 2)
            elif is_next:
                pygame.draw.rect(self.screen, (236, 226, 184), row)

            dot_color = (82, 150, 214) if is_unlocked else (132, 132, 132)
            if is_completed:
                dot_color = GOAL_COLOR
            pygame.draw.circle(self.screen, dot_color, (line_x, y + 10), 11)
            pygame.draw.circle(self.screen, TEXT_COLOR, (line_x, y + 10), 11, 2)

            if is_completed:
                status = "Concluida"
            elif is_next:
                status = "Proxima"
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

            if is_completed:
                medal_x = row.right - 132
                pygame.draw.polygon(
                    self.screen,
                    (226, 168, 74),
                    [
                        (medal_x, row.centery - 10),
                        (medal_x + 10, row.centery - 2),
                        (medal_x + 6, row.centery + 12),
                        (medal_x - 6, row.centery + 12),
                        (medal_x - 10, row.centery - 2),
                    ],
                )
                pygame.draw.circle(self.screen, (248, 218, 92), (medal_x, row.centery - 5), 10)
                pygame.draw.circle(self.screen, TEXT_COLOR, (medal_x, row.centery - 5), 10, 2)

        if first_index > 0:
            up_rect = pygame.Rect(box.right - 62, box.y + 58, 56, 56)
            pygame.draw.rect(self.screen, (238, 222, 166), up_rect, border_radius=6)
            pygame.draw.rect(self.screen, TEXT_COLOR, up_rect, 2, border_radius=6)
            up_surface = self.font.render("^", True, TEXT_COLOR)
            self.screen.blit(up_surface, up_surface.get_rect(center=up_rect.center))
        if last_index < get_level_count():
            down_rect = pygame.Rect(box.right - 62, box.bottom - 106, 56, 56)
            pygame.draw.rect(self.screen, (238, 222, 166), down_rect, border_radius=6)
            pygame.draw.rect(self.screen, TEXT_COLOR, down_rect, 2, border_radius=6)
            down_surface = self.font.render("v", True, TEXT_COLOR)
            self.screen.blit(down_surface, down_surface.get_rect(center=down_rect.center))

        if self.feedback_message and self.feedback_message_timer > 0:
            feedback_surface = self.font.render(self.feedback_message, True, (116, 70, 42))
            self.screen.blit(
                feedback_surface,
                feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 60)),
            )

        help_surface = self.font.render(
            "Setas ou toque escolhem | Enter inicia | M volta ao menu",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 28)))

    def _draw_fragment_message(self):
        box = self._get_message_box_rect(710, 82)
        text_alpha = self._draw_message_panel(box)

        for index, line in enumerate(self._wrap_text(self.fragment_message, 64)[:3]):
            line_surface = self.font.render(line, True, TEXT_COLOR)
            line_surface.set_alpha(text_alpha)
            self.screen.blit(line_surface, (box.x + 16, box.y + 14 + index * 24))

    def _draw_feedback_message(self, message: str | None = None):
        box = self._get_message_box_rect(710, 44)
        text_alpha = self._draw_message_panel(box)

        message_surface = self.font.render(message or self.feedback_message, True, TEXT_COLOR)
        message_surface.set_alpha(text_alpha)
        self.screen.blit(message_surface, (box.x + 16, box.y + 12))

    def _get_message_box_rect(self, width: int, height: int) -> pygame.Rect:
        return pygame.Rect(24, 126, width, height)

    def _draw_message_panel(self, box: pygame.Rect) -> int:
        overlaps_player = box.colliderect(self._get_player_screen_rect().inflate(20, 14))
        background_alpha = 116 if overlaps_player else 255
        border_alpha = 132 if overlaps_player else 255
        text_alpha = 150 if overlaps_player else 255

        panel = pygame.Surface(box.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (248, 238, 190, background_alpha), panel.get_rect())
        pygame.draw.rect(panel, (*TEXT_COLOR, border_alpha), panel.get_rect(), 2)
        self.screen.blit(panel, box)

        return text_alpha

    def _get_player_screen_rect(self) -> pygame.Rect:
        player_rect = pygame.Rect((0, 0), PLAYER_DRAW_SIZE)
        player_rect.midbottom = (
            self.player.rect.centerx - self.camera_x,
            self.player.rect.bottom,
        )
        return player_rect

    def _draw_tutorial_hints(self):
        hints = [
            ("A/D", "andar", 132),
            ("Espaco", "pular", 150),
            ("Fragmentos", "coletar", 190),
        ]
        x = 24
        y = SCREEN_HEIGHT - 64
        for key_text, label, width in hints:
            box = pygame.Rect(x, y, width, 38)
            pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=6)
            pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=6)
            key_surface = self.font.render(key_text, True, TEXT_COLOR)
            label_surface = self.font.render(label, True, (72, 76, 70))
            label_x = box.x + 12 + key_surface.get_width() + 14
            self.screen.blit(key_surface, (box.x + 10, box.y + 8))
            self.screen.blit(label_surface, (label_x, box.y + 8))
            x += width + 10

    def _draw_touch_controls(self):
        rects = self._touch_control_rects()
        self._draw_virtual_button(rects["left"], "<", "left" in self.active_touch_controls)
        self._draw_virtual_button(rects["right"], ">", "right" in self.active_touch_controls)
        self._draw_virtual_button(rects["jump"], "Pular", "jump" in self.active_touch_controls)
        self._draw_virtual_button(rects["pause"], "P", False, alpha=196)
        self._draw_virtual_button(rects["collection"], "C", False, alpha=196)

    def _draw_virtual_button(
        self,
        rect: pygame.Rect,
        label: str,
        active: bool,
        alpha: int = 176,
    ):
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        fill = (226, 202, 128, 224 if active else alpha)
        border = (*TEXT_COLOR, 238)
        pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=10)
        pygame.draw.rect(surface, border, surface.get_rect(), 3, border_radius=10)
        self.screen.blit(surface, rect)

        label_surface = self.font.render(label, True, TEXT_COLOR)
        self.screen.blit(label_surface, label_surface.get_rect(center=rect.center))

    def _draw_pause(self):
        box = self._pause_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render("Pausado", True, TEXT_COLOR)
        resume_surface = self.font.render("Continuar", True, TEXT_COLOR)
        restart_surface = self.font.render("Reiniciar fase", True, TEXT_COLOR)
        menu_surface = self.font.render("Voltar ao menu", True, TEXT_COLOR)
        collection_surface = self.font.render("C abre a colecao historica", True, TEXT_COLOR)

        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 50)))
        for action, rect in self._pause_touch_actions():
            pygame.draw.rect(self.screen, (226, 202, 128), rect, border_radius=6)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, 2, border_radius=6)
            label = {
                "resume": resume_surface,
                "restart": restart_surface,
                "menu": menu_surface,
            }[action]
            self.screen.blit(label, label.get_rect(center=rect.center))
        self.screen.blit(collection_surface, collection_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 218)))

    def _draw_help(self):
        self._draw_menu_scene()
        box = self._help_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)

        title_surface = self.big_font.render("Ajuda rapida", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 44)))

        rows = [
            ("A/D ou setas", "Mover Mig pelos caminhos."),
            ("Espaco / W", "Pular com um pouco de perdao no tempo."),
            ("Toque < >", "Mover Mig no celular."),
            ("Toque Pular", "Pular usando o botao grande da tela."),
            ("Fragmentos", "Pegue todos para abrir o portal da fase."),
            ("C ou toque C", "Abrir a colecao historica."),
            ("P / R / M", "Pausar, reiniciar ou voltar ao menu."),
        ]
        y = box.y + 80
        for key_text, description in rows:
            key_box = pygame.Rect(box.x + 42, y, 210, 34)
            pygame.draw.rect(self.screen, (226, 202, 128), key_box, border_radius=6)
            pygame.draw.rect(self.screen, TEXT_COLOR, key_box, 2, border_radius=6)
            key_surface = self.font.render(key_text, True, TEXT_COLOR)
            description_surface = self.font.render(description, True, TEXT_COLOR)
            self.screen.blit(key_surface, key_surface.get_rect(center=key_box.center))
            self.screen.blit(description_surface, (box.x + 278, y + 7))
            y += 38

        note_surface = self.font.render(
            "No celular, use o aparelho deitado. Leia e avance no seu ritmo.",
            True,
            (72, 76, 70),
        )
        close_surface = self.font.render("H, Enter, M ou toque aqui volta", True, TEXT_COLOR)
        self.screen.blit(note_surface, note_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 58)))
        self.screen.blit(close_surface, close_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 28)))

    def _draw_collection(self):
        box = self._collection_box_rect()
        pygame.draw.rect(self.screen, (246, 234, 196), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)
        pygame.draw.rect(self.screen, (226, 202, 128), (box.x, box.y, 84, box.height), border_radius=8)
        pygame.draw.line(self.screen, TEXT_COLOR, (box.x + 84, box.y), (box.x + 84, box.bottom), 2)

        title_surface = self.big_font.render("Colecao historica", True, TEXT_COLOR)
        collected_count = len(self.collection_entries)
        total_count = get_total_fragment_count()
        count_surface = self.font.render(
            f"Fragmentos coletados: {collected_count}/{total_count}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2 + 34, box.y + 38)))
        self.screen.blit(count_surface, count_surface.get_rect(center=(SCREEN_WIDTH // 2 + 34, box.y + 70)))

        pygame.draw.circle(self.screen, GOAL_COLOR, (box.x + 42, box.y + 54), 18)
        pygame.draw.circle(self.screen, TEXT_COLOR, (box.x + 42, box.y + 54), 18, 2)
        medal_surface = self.font.render(str(collected_count), True, TEXT_COLOR)
        self.screen.blit(medal_surface, medal_surface.get_rect(center=(box.x + 42, box.y + 54)))

        back_rect = self._collection_back_button_rect()
        pygame.draw.rect(self.screen, (226, 202, 128), back_rect, border_radius=6)
        pygame.draw.rect(self.screen, TEXT_COLOR, back_rect, 2, border_radius=6)
        back_surface = self.font.render("Voltar", True, TEXT_COLOR)
        self.screen.blit(back_surface, back_surface.get_rect(center=back_rect.center))

        rows = self._collection_rows()
        visible_rows = rows[self.collection_scroll : self.collection_scroll + 8]
        y = box.y + 96
        for row_type, text in visible_rows:
            if row_type == "header":
                header_box = pygame.Rect(box.x + 108, y - 4, box.width - 138, 30)
                pygame.draw.rect(self.screen, (238, 222, 166), header_box, border_radius=5)
                surface = self.font.render(text, True, TEXT_COLOR)
                pygame.draw.circle(self.screen, GOAL_COLOR, (box.x + 124, y + 11), 7)
                self.screen.blit(surface, (box.x + 142, y))
                y += 34
            elif row_type == "empty":
                surface = self.font.render(text, True, (106, 102, 88))
                self.screen.blit(surface, (box.x + 142, y))
                y += 28
            else:
                for line in self._wrap_text(text, 76)[:2]:
                    surface = self.font.render(line, True, (64, 68, 72))
                    self.screen.blit(surface, (box.x + 142, y))
                    y += 22
                y += 4

        help_surface = self.font.render(
            "Setas ou arraste rolam | C, Enter, M ou Voltar fecha",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 28)))

    def _draw_intro(self):
        box = self._intro_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        speaker_surface = self.font.render("Mig", True, TEXT_COLOR)
        self.screen.blit(speaker_surface, (box.x + 22, box.y + 18))

        for index, line in enumerate(self._wrap_text(self.level.intro_text, 68)):
            line_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(line_surface, (box.x + 22, box.y + 54 + index * 26))

        continue_surface = self.font.render("Pressione Enter ou toque aqui para iniciar.", True, TEXT_COLOR)
        self.screen.blit(
            continue_surface,
            continue_surface.get_rect(bottomright=(box.right - 22, box.bottom - 16)),
        )

    def _draw_completion_message(self):
        title = "Fase concluida!"
        subtitle = "Medalha recebida: todos os fragmentos da fase foram encontrados."
        if self.level_index + 1 >= get_level_count():
            restart = "Enter abre o final | toque continua | R reinicia | C colecao."
        else:
            restart = "Enter avanca | toque continua | R reinicia | C colecao."

        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        subtitle_surface = self.font.render(subtitle, True, TEXT_COLOR)
        restart_surface = self.font.render(restart, True, TEXT_COLOR)

        box = self._completion_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)
        pygame.draw.circle(self.screen, (248, 218, 92), (box.x + 42, box.y + 42), 20)
        pygame.draw.circle(self.screen, TEXT_COLOR, (box.x + 42, box.y + 42), 20, 2)
        pygame.draw.polygon(
            self.screen,
            (226, 168, 74),
            [(box.x + 32, box.y + 58), (box.x + 42, box.y + 78), (box.x + 52, box.y + 58)],
        )

        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 42)))
        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 78)),
        )
        for index, line in enumerate(self._wrap_text(self.level.historical_note, 78)[:2]):
            note_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(note_surface, note_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 108 + index * 24)))
        question_surface = self.font.render(self._completion_question(), True, (72, 76, 70))
        self.screen.blit(
            question_surface,
            question_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 160)),
        )
        self.screen.blit(
            restart_surface,
            restart_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 188)),
        )

    def _completion_question(self) -> str:
        questions = [
            "Pergunta para pensar: quem ja vivia nesse territorio?",
            "Pergunta para pensar: o que mudou nesse periodo?",
            "Pergunta para pensar: por que estudar isso com respeito?",
            "Pergunta para pensar: o que podemos aprender com esse momento?",
        ]
        return questions[self.level_index % len(questions)]

    def _draw_final(self):
        box = self._final_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)

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

        medal_y = box.y + 218
        start_x = SCREEN_WIDTH // 2 - 190
        for index in range(5):
            x = start_x + index * 95
            pygame.draw.circle(self.screen, (248, 218, 92), (x, medal_y), 19)
            pygame.draw.circle(self.screen, TEXT_COLOR, (x, medal_y), 19, 2)
            pygame.draw.polygon(
                self.screen,
                (226, 168, 74),
                [(x - 9, medal_y + 16), (x, medal_y + 34), (x + 9, medal_y + 16)],
            )

        completed_surface = self.font.render(
            f"Fases concluidas: {len(self.completed_levels)}/{get_level_count()}",
            True,
            TEXT_COLOR,
        )
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
            "Enter, M ou toque volta ao menu | C abre colecao | R revisita a ultima fase",
            True,
            TEXT_COLOR,
        )

        self.screen.blit(completed_surface, completed_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 266)))
        self.screen.blit(collected_surface, collected_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 296)))
        self.screen.blit(credits_surface, credits_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 330)))
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 360)))

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

    def _render_fitting_text(
        self,
        text: str,
        color: tuple[int, int, int],
        max_width: int,
        fonts: list[pygame.font.Font],
    ) -> pygame.Surface:
        for font in fonts:
            surface = font.render(text, True, color)
            if surface.get_width() <= max_width:
                return surface

        return fonts[-1].render(text, True, color)
