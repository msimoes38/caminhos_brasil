import asyncio
import unicodedata
from math import cos, pi, sin
from random import Random

import pygame

from src.backgrounds import draw_background
from src.levels import (
    create_level,
    get_active_pill_count,
    get_history_blocks,
    get_level_count,
    get_level_fragment_count,
    get_level_pill_bank,
    get_level_pill_count,
    get_level_pill_infos,
    get_level_plain_title,
    get_level_title,
    get_side_mission_summary,
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
STATE_QUIZ = "quiz"
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
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 44)
        self.medium_font = pygame.font.Font(None, 38)
        self.sounds = SoundManager()
        self.menu_image = self._load_menu_image()
        self.progress_store = ProgressStore(get_level_count())
        self.saved_progress = self.progress_store.load()
        self.temporary_session = False
        self.random = Random()
        self.session_random = Random()
        self.session_pill_choices: dict[int, tuple[int, ...]] = {}
        self.session_quiz_choices: dict[int, int] = {}
        self.keyboard_input_seen = False
        self.touch_ui_enabled = self._detect_touch_context()
        self.touch_control_by_pointer = {}
        self.active_touch_controls = set()
        self.touch_jump_pressed = False
        self.pointer_starts = {}
        self.level_play_time = 0
        self.tutorial_actions = self._new_tutorial_actions()
        self.side_missions_completed: set[int] = set()
        self.side_mission_completed = False
        self.micro_events_seen: set[int] = set()
        self.session_discovery_count = 0
        self.recent_collection_entry = None
        self.selected_quiz_option = 0
        self.quiz_feedback = ""
        self.quiz_feedback_timer = 0
        self.quiz_answered_correctly = False
        self.recent_history_block_seal = None
        self.recent_phase_album_completed: str | None = None

        self.selected_level_index = 0
        self.level_select_scroll = 0
        self.collection_scroll = 0
        self.previous_state = STATE_MENU
        self.animation_time = 0
        self.effects = []
        self.running = True
        self.web_loading_overlay_hidden = False
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

    def _new_tutorial_actions(self) -> dict[str, bool]:
        return {
            "move": False,
            "jump": False,
            "collect": False,
            "side": False,
            "portal": False,
        }

    def _detect_touch_context(self) -> bool:
        try:
            import platform

            window = getattr(platform, "window", None)
            if window is None:
                return False

            web_touch_context = self._web_touch_context_flag(window)
            if web_touch_context is not None:
                return web_touch_context

            navigator = getattr(window, "navigator", None) if window else None
            max_touch_points = self._safe_int(
                getattr(navigator, "maxTouchPoints", 0) if navigator else 0
            )
            ms_max_touch_points = self._safe_int(
                getattr(navigator, "msMaxTouchPoints", 0) if navigator else 0
            )
            if max(max_touch_points, ms_max_touch_points) > 0:
                return True

            media_queries = (
                "(pointer: coarse)",
                "(any-pointer: coarse)",
                "(hover: none)",
            )
            if any(self._match_media(window, query) for query in media_queries):
                return True

            if self._window_supports_touch(window):
                return True

            user_agent = str(getattr(navigator, "userAgent", "") if navigator else "").lower()
            mobile_tokens = ("android", "iphone", "ipad", "ipod", "mobile", "tablet")
            return any(token in user_agent for token in mobile_tokens)
        except Exception:
            return False

    def _web_touch_context_flag(self, window) -> bool | None:
        try:
            value = getattr(window, "caminhosTouchContext", None)
        except Exception:
            return None

        if value is None:
            return None
        if isinstance(value, bool):
            return value

        text = str(value).strip().lower()
        if text in ("true", "1", "yes"):
            return True
        if text in ("false", "0", "no", "none", "null", "undefined", ""):
            return False
        return None

    def _safe_int(self, value) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    def _match_media(self, window, query: str) -> bool:
        try:
            match_media = getattr(window, "matchMedia", None)
            if match_media is None:
                return False
            result = match_media(query)
            return bool(getattr(result, "matches", False))
        except Exception:
            return False

    def _window_supports_touch(self, window) -> bool:
        try:
            if "ontouchstart" in window:
                return True
        except Exception:
            pass

        try:
            return getattr(window, "ontouchstart", None) is not None
        except Exception:
            return False

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keyboard_input_seen = True
                if event.key in (
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_SPACE,
                    pygame.K_UP,
                    pygame.K_w,
                ):
                    self.touch_ui_enabled = False
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
        if is_touch:
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
        elif state == STATE_QUIZ:
            self._handle_quiz_tap(position)
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
        elif action == "fullscreen":
            self._request_fullscreen()
        elif action == "exit":
            self.running = False

    def _request_fullscreen(self):
        self.touch_ui_enabled = True
        attempted = False

        try:
            import platform

            window = getattr(platform, "window", None)
            helper = getattr(window, "caminhosRequestFullscreen", None) if window else None
            if helper is not None:
                helper()
                attempted = True
            else:
                document = getattr(platform, "document", None)
                element = getattr(document, "documentElement", None) if document else None
                if element is None and document is not None:
                    element = getattr(document, "body", None)
                if element is not None:
                    for method_name in (
                        "requestFullscreen",
                        "webkitRequestFullscreen",
                        "msRequestFullscreen",
                    ):
                        method = getattr(element, method_name, None)
                        if method is not None:
                            method()
                            attempted = True
                            break

                screen = getattr(window, "screen", None) if window else None
                orientation = getattr(screen, "orientation", None) if screen else None
                lock_orientation = getattr(orientation, "lock", None) if orientation else None
                if lock_orientation is not None:
                    lock_orientation("landscape")
        except Exception:
            attempted = False

        if attempted:
            self.feedback_message = "Tentando tela cheia. Use o celular deitado."
        else:
            self.feedback_message = "Se a barra continuar aparecendo, use Adicionar à tela inicial."
        self.feedback_message_timer = 4.5

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
            self.feedback_message = "Essa fase ainda está bloqueada. Conclua as anteriores primeiro."
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
        elif action == "collection":
            self._toggle_collection()
        elif self._pause_box_rect().collidepoint(position):
            self.state = STATE_PLAYING

    def _handle_quiz_tap(self, position: tuple[int, int]):
        option_index = self._quiz_option_at(position)
        if option_index is None:
            return

        self._submit_quiz_answer(option_index)

    def _scroll_collection_from_drag(self, start: dict, delta_y: int):
        max_scroll = max(0, len(self._collection_rows()) - self._collection_visible_rows())
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
            self._return_to_start_screen()
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
        elif self.state == STATE_QUIZ:
            self._handle_quiz_keydown(key)
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
                self.feedback_message = "Essa fase ainda está bloqueada. Conclua as anteriores primeiro."
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
        elif key == pygame.K_c:
            self._toggle_collection()

    def _handle_quiz_keydown(self, key: int):
        option_count = len(self.level.quiz.options) if self.level.quiz else 0
        if option_count == 0:
            self._complete_level()
            return

        if key in (pygame.K_UP, pygame.K_w):
            self.selected_quiz_option = max(0, self.selected_quiz_option - 1)
            self.quiz_feedback = ""
            self.sounds.play("select")
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected_quiz_option = min(option_count - 1, self.selected_quiz_option + 1)
            self.quiz_feedback = ""
            self.sounds.play("select")
        elif key == pygame.K_RETURN:
            self._submit_quiz_answer(self.selected_quiz_option)
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
        max_scroll = max(0, len(self._collection_rows()) - self._collection_visible_rows())
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
        self._update_quiz_feedback(dt)
        self._refresh_late_touch_context()

        if self.state != STATE_PLAYING:
            self._update_feedback_message(dt)
            return

        keys = pygame.key.get_pressed()
        touch_jump_pressed = self.touch_jump_pressed
        self.touch_jump_pressed = False
        moved_this_frame = (
            self._touch_direction() != 0
            or keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
            or keys[pygame.K_a]
            or keys[pygame.K_d]
        )
        if moved_this_frame:
            self.tutorial_actions["move"] = True
        self.level_play_time += dt
        self.player.handle_input(
            keys,
            dt,
            touch_direction=self._touch_direction(),
            touch_jump_held="jump" in self.active_touch_controls,
            touch_jump_pressed=touch_jump_pressed,
        )
        if self.player.jump_started:
            self.tutorial_actions["jump"] = True
            self.sounds.play("jump")
        self.player.update(dt, self.level.platforms, self.level.width)
        self._update_camera()
        self._update_fragment_message(dt)
        self._update_feedback_message(dt)
        self._collect_fragments()
        self._update_checkpoints()
        self._update_side_mission()
        self._update_micro_event()

        if self._should_restart_attempt():
            self._reset_attempt("Mig voltou ao ponto de retorno para tentar com mais cuidado.")
            return

        if self.player.rect.colliderect(self.level.goal):
            self.tutorial_actions["portal"] = True
            if self._all_fragments_collected():
                self._open_quiz_or_complete()
            else:
                self._show_goal_feedback()

    def _refresh_late_touch_context(self):
        if self.touch_ui_enabled or self.keyboard_input_seen or self.state != STATE_MENU:
            return
        if self._detect_touch_context():
            self.touch_ui_enabled = True

    def _collect_fragments(self):
        remaining_fragments = []
        collected_any = False

        for fragment in self.fragments:
            if self.player.rect.colliderect(fragment.rect):
                collected_any = True
                self.tutorial_actions["collect"] = True
                self.fragment_message = f"Boa descoberta! Você sabia? {fragment.info}"
                self.fragment_message_timer = 4
                self._spawn_effect_burst(
                    fragment.rect.center,
                    FRAGMENT_COLOR,
                    count=18,
                    radius=4,
                )
                self._add_collection_entry(fragment.info)
            else:
                remaining_fragments.append(fragment)

        self.fragments = remaining_fragments
        if collected_any:
            if self._all_fragments_collected() and not self.recent_phase_album_completed:
                self.feedback_message = "Todas as pílulas coletadas! O portal brilhou. Procure o Guardião."
                self.feedback_message_timer = 3.8
            self.sounds.play("collect")

    def _add_collection_entry(self, info: str):
        entry = (self.level.title, info)
        if entry in self.collection_entry_set:
            return

        self.collection_entry_set.add(entry)
        self.collection_entries.append(entry)
        self.recent_collection_entry = entry
        self.session_discovery_count += 1
        phase_entries = [
            saved_entry
            for saved_entry in self.collection_entries
            if saved_entry[0] == self.level.title
        ]
        if len(phase_entries) >= get_level_fragment_count(self.level_index):
            self.recent_phase_album_completed = self.level.title
            self.feedback_message = "Álbum completo da fase! Você encontrou as 10 descobertas."
            self.feedback_message_timer = 4.2
            self._spawn_effect_burst(
                self.player.rect.midtop,
                (255, 219, 112),
                count=28,
                radius=5,
            )
            self.sounds.play("seal")
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

    def _update_side_mission(self):
        if self.side_mission_completed:
            return

        mission = self.level.side_mission
        if not self.player.rect.colliderect(mission.rect):
            return

        self.side_mission_completed = True
        self.side_missions_completed.add(self.level_index)
        self.tutorial_actions["side"] = True
        self.feedback_message = mission.complete_message
        self.feedback_message_timer = 3.6
        self._spawn_effect_burst(
            mission.rect.center,
            (255, 205, 86),
            count=22,
            radius=5,
        )
        self.sounds.play("bonus")

    def _update_micro_event(self):
        if self.level_index in self.micro_events_seen:
            return
        if self.feedback_message_timer > 0 or self.fragment_message_timer > 0:
            return

        trigger_x, message, color = self._micro_event_data()
        if self.player.rect.centerx < trigger_x:
            return

        self.micro_events_seen.add(self.level_index)
        self.feedback_message = message
        self.feedback_message_timer = 3.2
        self._spawn_effect_burst(
            self.player.rect.midtop,
            color,
            count=14,
            radius=4,
        )

    def _micro_event_data(self) -> tuple[int, str, tuple[int, int, int]]:
        messages = (
            ("Uma onda desenhou espuma no caminho.", (126, 198, 214)),
            ("Folhas de cana balançam e mostram o rumo.", (124, 184, 92)),
            ("Um mapa antigo aponta novas trilhas.", (226, 202, 128)),
            ("Uma pedra brilha de leve nas montanhas.", (218, 196, 118)),
            ("Uma carta na praça lembra ideias em movimento.", (226, 202, 128)),
            ("Um livro aberto convida Mig a observar.", (204, 222, 236)),
            ("Um marco verde destaca uma mudança política.", (126, 176, 92)),
            ("Uma luz de jardim ajuda a notar continuidades.", (248, 220, 116)),
            ("Uma memória de liberdade pede respeito.", (238, 232, 210)),
            ("Um sino distante marca novas escolhas.", (226, 168, 74)),
            ("Trilhos e café mostram caminhos do período.", (156, 118, 72)),
            ("Um rádio antigo leva notícias pela cidade.", (170, 180, 178)),
            ("Cartazes lembram diálogo e participação.", (190, 206, 146)),
            ("Luzes suaves lembram direitos e memória.", (238, 232, 210)),
            ("Um livro cidadão brilha na praça.", (82, 150, 214)),
            ("Conexões do presente acendem no caminho.", (82, 150, 214)),
        )
        message, color = messages[self.level_index % len(messages)]
        trigger_x = min(self.level.width - 420, max(420, int(self.level.width * 0.28)))
        return trigger_x, message, color

    def _all_fragments_collected(self) -> bool:
        return len(self.fragments) == 0

    def _show_goal_feedback(self):
        if self.feedback_message_timer > 0:
            return

        remaining = len(self.fragments)
        plural = "s" if remaining != 1 else ""
        self.feedback_message = f"Falta coletar {remaining} pílula{plural} antes de atravessar o portal."
        self.feedback_message_timer = 2.4
        self.sounds.play("blocked")

    def _guardian_intro_text(self) -> str:
        block = self._history_block_for_level(self.level_index)
        if block:
            guide_lines = {
                "Primeiros contatos": "Respire e lembre: muitos povos já viviam aqui.",
                "Brasil colonial": "Vamos olhar para trabalho, caminhos e cuidado.",
                "Independência e Império": "Toda mudança pede perguntas e respeito.",
                "República e democracia": "Direitos e memória ajudam a escolher melhor.",
                "Brasil de hoje": "O presente também faz parte da história.",
            }
            return guide_lines.get(block.name, f"Vamos lembrar com calma: {block.phrase}")
        return "Vamos lembrar com calma uma descoberta importante."

    def _guardian_focus_text(self) -> str:
        if self.level.quiz_pill_index is None:
            return "A pergunta vem de uma descoberta desta fase."

        bank = get_level_pill_bank(self.level_index)
        if not 0 <= self.level.quiz_pill_index < len(bank):
            return "A pergunta vem de uma descoberta desta fase."

        info = bank[self.level.quiz_pill_index].info
        short_info = self._wrap_text(info, 54)[0]
        return f"Lembre da pílula: {short_info}"

    def _guardian_success_text(self) -> str:
        block = self._history_block_for_level(self.level_index)
        if block:
            return f"Muito bem! O Guardião celebrou o bloco {self._history_block_display_name(block)}."
        return "Muito bem! O Guardião abriu o portal com alegria."

    def _open_quiz_or_complete(self):
        if self.level.quiz is None:
            self._complete_level()
            return

        self.selected_quiz_option = 0
        self.quiz_feedback = ""
        self.quiz_feedback_timer = 0
        self.quiz_answered_correctly = False
        self.feedback_message = "O Guardião quer ouvir uma lembrança da fase."
        self.feedback_message_timer = 2.2
        self._clear_touch_controls()
        self.state = STATE_QUIZ
        self.sounds.play("portal")

    def _submit_quiz_answer(self, option_index: int):
        quiz = self.level.quiz
        if quiz is None:
            self._complete_level()
            return

        self.selected_quiz_option = max(0, min(option_index, len(quiz.options) - 1))
        if self.selected_quiz_option == quiz.correct_index:
            self.quiz_feedback = self._guardian_success_text()
            self.quiz_feedback_timer = 0
            self.quiz_answered_correctly = True
            self.sounds.play("correct")
            self._complete_level()
            return

        self.quiz_feedback = f"Quase! Você está aprendendo. {quiz.hint} Tente de novo."
        self.quiz_feedback_timer = 7.5
        self.sounds.play("hint")

    def _update_quiz_feedback(self, dt: float):
        if self.quiz_feedback_timer <= 0:
            return

        self.quiz_feedback_timer -= dt
        if self.quiz_feedback_timer <= 0:
            self.quiz_feedback = ""

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
        active_pill_indexes = self._session_pill_choices_for_level(self.level_index)
        quiz_pill_index = self._session_quiz_choice_for_level(self.level_index, active_pill_indexes)
        self.level = create_level(self.level_index, active_pill_indexes, quiz_pill_index)
        self.player = Player(self.level.start_position)
        self.fragments = list(self.level.fragments)
        self.total_fragments = len(self.fragments)
        self.respawn_position = self.level.start_position
        self.active_checkpoints = set()
        self.side_mission_completed = self.level_index in self.side_missions_completed
        self.fragment_message = ""
        self.fragment_message_timer = 0
        self.feedback_message = ""
        self.feedback_message_timer = 0
        self.selected_quiz_option = 0
        self.quiz_feedback = ""
        self.quiz_feedback_timer = 0
        self.quiz_answered_correctly = False
        self.recent_history_block_seal = None
        self.recent_phase_album_completed = None
        self.level_play_time = 0
        self.tutorial_actions = self._new_tutorial_actions()
        self.effects = []
        self.camera_x = 0
        self._clear_touch_controls()
        self.state = state

    def _session_pill_choices_for_level(self, index: int) -> tuple[int, ...]:
        if index in self.session_pill_choices:
            return self.session_pill_choices[index]

        bank_count = get_level_pill_count(index)
        active_count = min(get_active_pill_count(index), bank_count)
        if active_count <= 0:
            choices = ()
        else:
            choices = tuple(sorted(self.session_random.sample(range(bank_count), active_count)))
        self.session_pill_choices[index] = choices
        return choices

    def _session_quiz_choice_for_level(
        self,
        index: int,
        active_pill_indexes: tuple[int, ...],
    ) -> int | None:
        current_choice = self.session_quiz_choices.get(index)
        if current_choice in active_pill_indexes:
            return current_choice
        if not active_pill_indexes:
            return None

        choice = self.session_random.choice(active_pill_indexes)
        self.session_quiz_choices[index] = choice
        return choice

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

    def _return_to_start_screen(self):
        self.previous_state = STATE_MENU
        self.collection_scroll = 0
        self.selected_level_index = min(self.highest_unlocked_level, get_level_count() - 1)
        self._sync_level_select_scroll()
        self._load_level(self.level_index, STATE_MENU)

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
        earned_before = {
            block.name
            for block, _completed, _total, earned in self._history_block_progress()
            if earned
        }
        self.state = STATE_COMPLETED
        self.completed_levels.add(self.level_index)
        self.highest_unlocked_level = min(
            get_level_count() - 1,
            max(self.highest_unlocked_level, self.level_index + 1),
        )
        self.recent_history_block_seal = None
        for block, _completed, _total, earned in self._history_block_progress():
            if earned and block.name not in earned_before:
                self.recent_history_block_seal = block.name
                break
        self._save_progress()
        self._spawn_effect_burst(
            self.level.goal.center,
            GOAL_COLOR,
            count=28,
            radius=5,
        )
        if self.recent_history_block_seal:
            self.sounds.play("seal")
        else:
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
        self.collection_entries = self._normalize_collection_entries(
            progress["collection_entries"]
        )
        self.collection_entry_set = set(self.collection_entries)

    def _normalize_collection_entries(
        self,
        entries: list[tuple[str, str]],
    ) -> list[tuple[str, str]]:
        normalized_entries = []
        seen = set()

        for level_title, info in entries:
            normalized_entry = (
                self._canonical_level_title(level_title),
                self._canonical_fragment_info(level_title, info),
            )
            if normalized_entry in seen:
                continue
            seen.add(normalized_entry)
            normalized_entries.append(normalized_entry)

        return normalized_entries

    def _canonical_level_title(self, level_title: str) -> str:
        title_key = self._text_key(level_title)
        for index in range(get_level_count()):
            current_title = get_level_plain_title(index)
            if self._text_key(current_title) == title_key:
                return current_title
        return level_title

    def _canonical_fragment_info(self, level_title: str, info: str) -> str:
        level_key = self._text_key(level_title)
        info_key = self._text_key(info)

        for index in range(get_level_count()):
            if self._text_key(get_level_plain_title(index)) != level_key:
                continue
            for pill_info in get_level_pill_infos(index):
                if self._text_key(pill_info) == info_key:
                    return pill_info

        return info

    def _text_key(self, text: str) -> str:
        normalized = unicodedata.normalize("NFD", text)
        return "".join(
            character
            for character in normalized
            if unicodedata.category(character) != "Mn"
        ).casefold()

    def _start_temporary_new_journey(self):
        self.temporary_session = True
        self.session_random = Random()
        self.session_pill_choices.clear()
        self.session_quiz_choices.clear()
        self.side_missions_completed.clear()
        self.micro_events_seen.clear()
        self.session_discovery_count = 0
        self.recent_phase_album_completed = None
        collection_entries = list(self.collection_entries)
        self._apply_progress(
            {
                "highest_unlocked_level": 0,
                "completed_levels": set(),
                "collection_entries": collection_entries,
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
        if self.touch_ui_enabled:
            return pygame.Rect(496, 224, 430, 300)
        return pygame.Rect(548, 302, 382, 190)

    def _menu_touch_actions(self) -> list[tuple[str, pygame.Rect]]:
        panel = self._menu_panel_rect()
        if self.touch_ui_enabled:
            row_x = panel.x + 18
            row_y = panel.y + 76
            row_width = panel.width - 36
            row_height = 38
            gap = 5
            return [
                ("continue", pygame.Rect(row_x, row_y + 0 * (row_height + gap), row_width, row_height)),
                ("new", pygame.Rect(row_x, row_y + 1 * (row_height + gap), row_width, row_height)),
                ("timeline", pygame.Rect(row_x, row_y + 2 * (row_height + gap), row_width, row_height)),
                ("collection", pygame.Rect(row_x, row_y + 3 * (row_height + gap), row_width, row_height)),
                ("help", pygame.Rect(row_x, row_y + 4 * (row_height + gap), row_width // 2 - 5, row_height)),
                ("fullscreen", pygame.Rect(row_x + row_width // 2 + 5, row_y + 4 * (row_height + gap), row_width // 2 - 5, row_height)),
            ]
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
            "left": pygame.Rect(24, SCREEN_HEIGHT - 64, 92, 52),
            "right": pygame.Rect(132, SCREEN_HEIGHT - 64, 92, 52),
            "jump": pygame.Rect(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 106, 132, 90),
            "pause": pygame.Rect(SCREEN_WIDTH - 140, 68, 54, 44),
            "collection": pygame.Rect(SCREEN_WIDTH - 76, 68, 54, 44),
        }

    def _gameplay_touch_action_at(self, position: tuple[int, int]) -> str | None:
        for action, rect in self._touch_control_rects().items():
            hit_rect = rect.inflate(14, 12)
            if hit_rect.collidepoint(position):
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
            rows.append((index, pygame.Rect(box.x + 84, y - 7, box.width - 170, 35)))
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

    def _collection_visible_rows(self) -> int:
        return 4

    def _intro_box_rect(self) -> pygame.Rect:
        return pygame.Rect(70, SCREEN_HEIGHT - 195, SCREEN_WIDTH - 140, 150)

    def _pause_box_rect(self) -> pygame.Rect:
        return self._centered_rect(540, 292)

    def _pause_touch_actions(self) -> list[tuple[str, pygame.Rect]]:
        box = self._pause_box_rect()
        return [
            ("resume", pygame.Rect(box.x + 64, box.y + 78, box.width - 128, 38)),
            ("restart", pygame.Rect(box.x + 64, box.y + 122, box.width - 128, 38)),
            ("menu", pygame.Rect(box.x + 64, box.y + 166, box.width - 128, 38)),
            ("collection", pygame.Rect(box.x + 64, box.y + 210, box.width - 128, 38)),
        ]

    def _pause_touch_action_at(self, position: tuple[int, int]) -> str | None:
        for action, rect in self._pause_touch_actions():
            if rect.collidepoint(position):
                return action
        return None

    def _quiz_box_rect(self) -> pygame.Rect:
        return self._centered_rect(820, 420)

    def _quiz_option_rects(self) -> list[pygame.Rect]:
        box = self._quiz_box_rect()
        return [
            pygame.Rect(box.x + 64, box.y + 186 + index * 56, box.width - 128, 46)
            for index in range(3)
        ]

    def _quiz_option_at(self, position: tuple[int, int]) -> int | None:
        for index, rect in enumerate(self._quiz_option_rects()):
            if rect.collidepoint(position):
                return index
        return None

    def _help_box_rect(self) -> pygame.Rect:
        return self._centered_rect(780, 420)

    def _completion_box_rect(self) -> pygame.Rect:
        box = pygame.Rect(0, 0, 820, 208)
        box.center = (SCREEN_WIDTH // 2, 168)
        return box

    def _final_box_rect(self) -> pygame.Rect:
        return self._centered_rect(840, 430)

    def _collection_rows(self) -> list[tuple[str, str]]:
        rows = self._side_mission_memory_rows()
        rows.extend(self._recent_discovery_rows())
        entries_by_level: dict[str, list[str]] = {}
        for level_title, info in self.collection_entries:
            entries_by_level.setdefault(level_title, []).append(info)

        for index in range(get_level_count()):
            level_title = get_level_plain_title(index)
            entries = entries_by_level.get(level_title, [])

            total = get_level_fragment_count(index)
            completed_album = len(entries) >= total
            completion_label = " - Álbum completo!" if completed_album else ""
            rows.append(
                (
                    "header",
                    f"{index + 1:02d}. {get_level_title(index)} ({min(len(entries), total)}/{total} descobertas){completion_label}",
                )
            )
            for info in entries:
                rows.append(("item", info))
            if not entries:
                rows.append(("empty", "Ainda sem pílulas descobertas nesta fase."))

        return rows

    def _side_mission_memory_rows(self) -> list[tuple[str, str]]:
        completed_indexes = [
            index
            for index in sorted(self.side_missions_completed)
            if 0 <= index < get_level_count()
        ]
        rows = [
            (
                "memory_header",
                f"Lembranças da viagem: {len(completed_indexes)}/{get_level_count()} observadas",
            )
        ]
        if not completed_indexes:
            rows.append(
                (
                    "memory_empty",
                    "Observe marcadores Extra para guardar lembranças nesta sessão.",
                )
            )
            return rows

        for index in completed_indexes:
            title, complete_message = get_side_mission_summary(index)
            rows.append(("memory_item", f"{index + 1:02d}. {title} - {complete_message}"))
        return rows

    def _recent_discovery_rows(self) -> list[tuple[str, str]]:
        if not self.recent_collection_entry:
            return []

        level_title, info = self.recent_collection_entry
        return [
            ("favorite_header", "Descoberta recente da jornada"),
            ("favorite_item", f"{level_title}: {info}"),
        ]

    def _history_block_progress(self):
        progress = []
        for block in get_history_blocks():
            completed = sum(1 for index in block.level_indexes if index in self.completed_levels)
            total = len(block.level_indexes)
            progress.append((block, completed, total, completed == total))
        return progress

    def _history_block_for_level(self, level_index: int):
        for block in get_history_blocks():
            if level_index in block.level_indexes:
                return block
        return None

    def _history_block_display_name(self, block) -> str:
        display_names = {
            "Primeiros contatos": "Primeiros",
            "Brasil colonial": "Colonial",
            "Independência e Império": "Ind./Imp.",
            "República e democracia": "República",
            "Brasil de hoje": "Hoje",
        }
        return display_names.get(block.name, block.name)

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
            self._draw_side_mission()
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
        elif self.state == STATE_QUIZ:
            self._draw_quiz()
        elif self.state == STATE_COMPLETED:
            self._draw_completion_message()

        pygame.display.flip()
        self._hide_web_loading_overlay()

    def _hide_web_loading_overlay(self):
        if self.web_loading_overlay_hidden:
            return
        self.web_loading_overlay_hidden = True

        try:
            import platform

            window = getattr(platform, "window", None)
            hide_loading = getattr(window, "caminhosHideLoading", None) if window else None
            if hide_loading is not None:
                try:
                    hide_loading()
                    return
                except Exception:
                    pass

            document = getattr(platform, "document", None)
            loading = document.getElementById("caminhos-loading") if document else None
            if loading is not None:
                loading.style.display = "none"
        except Exception:
            pass

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
            for index in range(10):
                angle = self.animation_time * 1.7 + index * (pi / 5)
                ray_start = (
                    goal_rect.centerx + int(cos(angle) * 20),
                    goal_rect.centery + int(sin(angle) * 18),
                )
                ray_end = (
                    goal_rect.centerx + int(cos(angle) * 48),
                    goal_rect.centery + int(sin(angle) * 40),
                )
                pygame.draw.line(self.screen, (218, 246, 162), ray_start, ray_end, 2)
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

    def _draw_side_mission(self):
        mission = self.level.side_mission
        marker_rect = self._to_screen_rect(mission.rect)
        if marker_rect.right < -80 or marker_rect.left > SCREEN_WIDTH + 80:
            return

        wave = int(sin(self.animation_time * 4 + self.level_index) * 3)
        marker_rect.y += wave
        completed = self.side_mission_completed
        glow_color = (255, 231, 142) if not completed else (188, 225, 197)
        fill_color = (255, 205, 86) if not completed else (96, 174, 122)
        outline_color = (122, 91, 47) if not completed else (54, 116, 77)
        pulse_radius = 26 + int(sin(self.animation_time * 5) * 3)

        if not completed:
            pygame.draw.circle(self.screen, glow_color, marker_rect.center, pulse_radius, 2)

        pedestal = pygame.Rect(marker_rect.centerx - 22, marker_rect.bottom - 5, 44, 12)
        pygame.draw.rect(self.screen, (116, 96, 72), pedestal, border_radius=5)
        pygame.draw.ellipse(
            self.screen,
            (92, 74, 56),
            (pedestal.x + 4, pedestal.y + 5, pedestal.width - 8, 8),
        )
        pygame.draw.rect(self.screen, fill_color, marker_rect, border_radius=9)
        pygame.draw.rect(self.screen, outline_color, marker_rect, 2, border_radius=9)
        self._draw_side_mission_icon(marker_rect, mission.icon, completed)

        label = "Extra" if not completed else "Feito"
        label_surface = self.small_font.render(label, True, TEXT_COLOR)
        label_rect = label_surface.get_rect(
            center=(marker_rect.centerx, marker_rect.y - 12)
        )
        label_bg = label_rect.inflate(14, 6)
        pygame.draw.rect(self.screen, (255, 250, 230), label_bg, border_radius=6)
        pygame.draw.rect(self.screen, (168, 137, 80), label_bg, 1, border_radius=6)
        self.screen.blit(label_surface, label_rect)

        close_to_player = abs(self.player.rect.centerx - mission.rect.centerx) < 150
        if close_to_player and not completed and self.state == STATE_PLAYING:
            self._draw_side_mission_prompt(marker_rect, mission.prompt)

    def _draw_side_mission_prompt(self, marker_rect: pygame.Rect, prompt: str):
        lines = self._wrap_text(prompt, 30)[:3]
        if not lines:
            return

        box_width = 320
        box_height = 20 + len(lines) * 20
        box_x = max(18, min(marker_rect.centerx - box_width // 2, SCREEN_WIDTH - box_width - 18))
        box_y = max(136, marker_rect.y - box_height - 28)
        box = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (255, 250, 230), box, border_radius=7)
        pygame.draw.rect(self.screen, (168, 137, 80), box, 2, border_radius=7)
        for index, line in enumerate(lines):
            surface = self._render_fitting_text(
                line,
                TEXT_COLOR,
                box.width - 26,
                [self.font, self.small_font],
            )
            self.screen.blit(surface, (box.x + 13, box.y + 9 + index * 20))

    def _draw_side_mission_icon(self, rect: pygame.Rect, icon: str, completed: bool):
        center = rect.center
        line_color = (72, 61, 48) if not completed else (238, 255, 232)
        if completed:
            pygame.draw.line(
                self.screen,
                line_color,
                (center[0] - 10, center[1]),
                (center[0] - 2, center[1] + 8),
                4,
            )
            pygame.draw.line(
                self.screen,
                line_color,
                (center[0] - 2, center[1] + 8),
                (center[0] + 12, center[1] - 10),
                4,
            )
            return

        if icon in {"marker", "sign", "lamp", "connection"}:
            pygame.draw.rect(
                self.screen,
                line_color,
                (center[0] - 2, center[1] - 10, 4, 20),
                border_radius=2,
            )
            pygame.draw.circle(self.screen, line_color, (center[0], center[1] - 12), 7, 2)
        elif icon in {"map", "letter", "document"}:
            pygame.draw.rect(
                self.screen,
                (255, 249, 218),
                (rect.x + 9, rect.y + 8, 18, 20),
                border_radius=2,
            )
            pygame.draw.rect(
                self.screen,
                line_color,
                (rect.x + 9, rect.y + 8, 18, 20),
                2,
                border_radius=2,
            )
            pygame.draw.line(
                self.screen,
                line_color,
                (rect.x + 13, rect.y + 16),
                (rect.x + 23, rect.y + 16),
                2,
            )
        elif icon in {"rails", "press", "tower"}:
            pygame.draw.line(
                self.screen,
                line_color,
                (rect.x + 10, rect.y + 25),
                (rect.x + 27, rect.y + 11),
                3,
            )
            pygame.draw.line(
                self.screen,
                line_color,
                (rect.x + 10, rect.y + 11),
                (rect.x + 27, rect.y + 25),
                3,
            )
        else:
            points = [
                (center[0], center[1] - 12),
                (center[0] + 5, center[1] - 2),
                (center[0] + 16, center[1] - 2),
                (center[0] + 7, center[1] + 4),
                (center[0] + 10, center[1] + 15),
                (center[0], center[1] + 8),
                (center[0] - 10, center[1] + 15),
                (center[0] - 7, center[1] + 4),
                (center[0] - 16, center[1] - 2),
                (center[0] - 5, center[1] - 2),
            ]
            pygame.draw.polygon(self.screen, line_color, points)

    def _draw_fragments(self):
        for order, fragment in enumerate(self.fragments):
            fragment_rect = self._to_screen_rect(fragment.rect)
            float_y = int(sin(self.animation_time * 4 + fragment.rect.x * 0.02) * 5)
            fragment_rect.y += float_y
            center = fragment_rect.center
            glow_radius = 18 + int(sin(self.animation_time * 5 + fragment.rect.x) * 3)
            is_first_hint = (
                self.level_index == 0
                and order == 0
                and not self.tutorial_actions["collect"]
            )

            if is_first_hint:
                hint_radius = glow_radius + 8 + int(sin(self.animation_time * 6) * 2)
                pygame.draw.circle(self.screen, (255, 248, 190), center, hint_radius, 2)
                pygame.draw.circle(self.screen, (248, 218, 92), center, hint_radius + 6, 1)
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
        fragments_text = f"Pílulas históricas: {collected}/{self.total_fragments}"

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
            self._draw_feedback_message("Portal liberado! Encontre o Guardião do Portal.")

        if self.level_index == 0 and self.state == STATE_PLAYING:
            self._draw_tutorial_hints()

    def _draw_menu(self):
        self._draw_menu_scene()
        self._draw_menu_footer_banner()

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
        progress_text = f"Fases liberadas: {self.highest_unlocked_level + 1}/{get_level_count()}"
        if self.temporary_session:
            progress_text = "Nova jornada nesta sessão"
        progress_surface = self.font.render(progress_text, True, TEXT_COLOR)

        if self.touch_ui_enabled:
            title_surface = self.medium_font.render("Toque para começar", True, TEXT_COLOR)
            self.screen.blit(title_surface, (panel.x + 18, panel.y + 12))
            self.screen.blit(
                progress_surface,
                progress_surface.get_rect(midleft=(panel.x + 20, panel.y + 58)),
            )

            labels = {
                "continue": "Continuar",
                "new": "Nova jornada",
                "timeline": "Linha do tempo",
                "collection": "Coleção",
                "help": "Ajuda",
                "fullscreen": "Tela cheia",
            }
            for action, row in self._menu_touch_actions():
                pygame.draw.rect(self.screen, (248, 238, 190), row, border_radius=7)
                pygame.draw.rect(self.screen, TEXT_COLOR, row, 2, border_radius=7)
                label_surface = self.font.render(labels[action], True, TEXT_COLOR)
                self.screen.blit(label_surface, label_surface.get_rect(center=row.center))

        else:
            for _, row in self._menu_touch_actions():
                pygame.draw.rect(self.screen, (248, 238, 190), row, border_radius=5)
                pygame.draw.rect(self.screen, (128, 116, 86), row, 1, border_radius=5)

            start_surface = self.font.render("Enter: continuar", True, TEXT_COLOR)
            new_journey_surface = self.font.render("N: nova sessão", True, TEXT_COLOR)
            select_surface = self.font.render("S: linha do tempo", True, TEXT_COLOR)
            collection_surface = self.font.render("C: coleção", True, TEXT_COLOR)
            help_surface = self.font.render("H: ajuda", True, TEXT_COLOR)
            exit_surface = self.font.render("Esc: início", True, TEXT_COLOR)

            self.screen.blit(start_surface, (panel.x + 18, panel.y + 12))
            self.screen.blit(new_journey_surface, (panel.x + 18, panel.y + 40))
            self.screen.blit(select_surface, (panel.x + 18, panel.y + 68))
            self.screen.blit(collection_surface, (panel.x + 18, panel.y + 96))
            self.screen.blit(help_surface, (panel.x + 206, panel.y + 96))
            self.screen.blit(exit_surface, (panel.x + 18, panel.y + 124))
            self.screen.blit(progress_surface, (panel.x + 18, panel.y + 154))

        if self.feedback_message and self.feedback_message_timer > 0:
            feedback_surface = self.font.render(self.feedback_message, True, (116, 70, 42))
            feedback_y = panel.y - 26 if self.touch_ui_enabled else panel.y - 18
            self.screen.blit(feedback_surface, feedback_surface.get_rect(center=(panel.centerx, feedback_y)))

    def _draw_menu_footer_banner(self):
        footer = pygame.Rect(0, SCREEN_HEIGHT - 58, SCREEN_WIDTH, 58)
        surface = pygame.Surface(footer.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (32, 36, 40, 255), surface.get_rect())
        pygame.draw.line(surface, (248, 238, 190, 150), (0, 0), (footer.width, 0), 2)
        self.screen.blit(surface, footer)

        if self.touch_ui_enabled:
            hint_text = "Toque em uma opção para começar"
            hint_center = (252, footer.centery)
        else:
            hint_text = "Escolha uma opção no painel"
            hint_center = (SCREEN_WIDTH // 2, footer.centery)
        hint_surface = self.font.render(hint_text, True, (248, 238, 190))
        self.screen.blit(hint_surface, hint_surface.get_rect(center=hint_center))

    def _draw_touch_menu_footer_cover(self):
        self._draw_menu_footer_banner()

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
            ((154, 440), "açúcar", "cane"),
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

    def _draw_timeline_map_details(self, box: pygame.Rect):
        for offset in range(0, box.width - 120, 86):
            x = box.x + 80 + offset
            y = box.y + 70 + (offset // 86 % 2) * 8
            pygame.draw.circle(self.screen, (226, 214, 172), (x, y), 3)
            if offset:
                pygame.draw.line(self.screen, (226, 214, 172), (x - 70, y - 8), (x - 8, y), 2)

        compass_center = (box.right - 84, box.y + 46)
        pygame.draw.circle(self.screen, (238, 222, 166), compass_center, 22)
        pygame.draw.circle(self.screen, (128, 116, 86), compass_center, 22, 2)
        pygame.draw.polygon(
            self.screen,
            (226, 168, 74),
            [
                (compass_center[0], compass_center[1] - 16),
                (compass_center[0] + 6, compass_center[1] + 4),
                (compass_center[0], compass_center[1] + 1),
                (compass_center[0] - 6, compass_center[1] + 4),
            ],
        )

    def _draw_level_select(self):
        box = self._level_select_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render("Linha do tempo", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 46)))
        self._draw_timeline_map_details(box)

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

            block = self._history_block_for_level(index)
            if is_next:
                arrow_points = [
                    (row.x - 22, row.centery),
                    (row.x - 8, row.centery - 9),
                    (row.x - 8, row.centery + 9),
                ]
                pygame.draw.polygon(self.screen, (226, 168, 74), arrow_points)
                pygame.draw.polygon(self.screen, TEXT_COLOR, arrow_points, 2)

            dot_color = (82, 150, 214) if is_unlocked else (132, 132, 132)
            if is_completed:
                dot_color = GOAL_COLOR
            pygame.draw.circle(self.screen, dot_color, (line_x, y + 10), 11)
            pygame.draw.circle(self.screen, TEXT_COLOR, (line_x, y + 10), 11, 2)
            if block:
                block_label = self._render_fitting_text(
                    block.short_label,
                    (255, 250, 232) if is_unlocked else (230, 230, 222),
                    18,
                    [self.small_font],
                )
                self.screen.blit(block_label, block_label.get_rect(center=(line_x, y + 10)))

            if is_completed:
                status = "Concluída"
            elif is_next:
                status = "Próxima aventura"
            elif is_unlocked:
                status = "Liberada"
            else:
                status = "Complete a anterior"
            text = f"{index + 1:02d}. {get_level_title(index)}"
            color = TEXT_COLOR if is_unlocked else (112, 112, 112)
            status_column_width = 190
            status_left = row.right - status_column_width
            status_surface = self._render_fitting_text(
                status,
                color,
                status_column_width - 42,
                [self.small_font],
            )
            surface = self._render_fitting_text(
                text,
                color,
                row.width - status_column_width - 28,
                [self.font, self.small_font],
            )
            self.screen.blit(surface, (row.x + 14, row.y + 7))
            self.screen.blit(
                status_surface,
                status_surface.get_rect(midright=(row.right - 12, row.centery)),
            )

            if is_completed:
                medal_x = status_left + 20
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
        else:
            block = self._history_block_for_level(self.selected_level_index)
            if block:
                phrase = f"Bloco {self._history_block_display_name(block)}: {block.phrase}"
                phrase_surface = self._render_fitting_text(
                    phrase,
                    (72, 76, 70),
                    box.width - 90,
                    [self.font, self.small_font],
                )
                self.screen.blit(
                    phrase_surface,
                    phrase_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 60)),
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

        message_surface = self._render_fitting_text(
            message or self.feedback_message,
            TEXT_COLOR,
            box.width - 32,
            [self.font, self.small_font],
        )
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

    def _tutorial_hint_text(self) -> str | None:
        if self.level_index != 0:
            return None

        if not self.tutorial_actions["move"]:
            if self.touch_ui_enabled:
                return "Use os botões para andar."
            return "Use A/D ou setas para andar."
        if not self.tutorial_actions["jump"]:
            if self.touch_ui_enabled:
                return "Toque em Pular."
            return "Use Espaço para pular."
        if not self.tutorial_actions["collect"]:
            return "Pegue as pílulas brilhantes."
        if self._all_fragments_collected() and not self.tutorial_actions["portal"]:
            return "Agora vá ao portal verde."
        if not self.side_mission_completed:
            return "Opcional: observe o marco Extra."
        return None

    def _draw_tutorial_hints(self):
        hint = self._tutorial_hint_text()
        if not hint:
            return

        x = 420 if self.touch_ui_enabled else 24
        y = SCREEN_HEIGHT - 180 if self.touch_ui_enabled else SCREEN_HEIGHT - 72
        box_width = 430 if self.touch_ui_enabled else 388
        box = pygame.Rect(x, y, box_width, 44)
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=7)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=7)
        hint_surface = self._render_fitting_text(
            hint,
            TEXT_COLOR,
            box.width - 28,
            [self.font, self.small_font],
        )
        self.screen.blit(hint_surface, hint_surface.get_rect(center=box.center))

    def _draw_touch_controls(self):
        rects = self._touch_control_rects()
        self._draw_virtual_button(rects["left"], "<", "left" in self.active_touch_controls)
        self._draw_virtual_button(rects["right"], ">", "right" in self.active_touch_controls)
        self._draw_virtual_button(rects["jump"], "Pular", "jump" in self.active_touch_controls, alpha=100)
        self._draw_virtual_button(rects["pause"], "P", False, alpha=116)
        self._draw_virtual_button(rects["collection"], "C", False, alpha=116)

    def _draw_virtual_button(
        self,
        rect: pygame.Rect,
        label: str,
        active: bool,
        alpha: int = 88,
    ):
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        fill = (226, 202, 128, 164 if active else alpha)
        border = (*TEXT_COLOR, 216)
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
        collection_surface = self.font.render("Coleção", True, TEXT_COLOR)

        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 50)))
        for action, rect in self._pause_touch_actions():
            pygame.draw.rect(self.screen, (226, 202, 128), rect, border_radius=6)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, 2, border_radius=6)
            label = {
                "resume": resume_surface,
                "restart": restart_surface,
                "menu": menu_surface,
                "collection": collection_surface,
            }[action]
            self.screen.blit(label, label.get_rect(center=rect.center))

        hint_surface = self.font.render("P ou Enter continua | R reinicia | M menu | C coleção", True, (72, 76, 70))
        self.screen.blit(hint_surface, hint_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 20)))

    def _draw_quiz(self):
        quiz = self.level.quiz
        if quiz is None:
            return

        box = self._quiz_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)

        pygame.draw.circle(self.screen, GOAL_COLOR, (box.x + 46, box.y + 48), 22)
        pygame.draw.circle(self.screen, TEXT_COLOR, (box.x + 46, box.y + 48), 22, 2)
        pygame.draw.circle(self.screen, (248, 238, 126), (box.x + 46, box.y + 48), 8)

        title_surface = self.big_font.render("Guardião do Portal", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 42)))

        guardian_lines = self._wrap_text(
            f"Guardião: {self._guardian_intro_text()}",
            76,
        )[:2]
        for index, line in enumerate(guardian_lines):
            guardian_surface = self.font.render(line, True, (72, 76, 70))
            self.screen.blit(
                guardian_surface,
                guardian_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 76 + index * 23)),
            )

        focus_surface = self._render_fitting_text(
            self._guardian_focus_text(),
            (72, 76, 70),
            box.width - 112,
            [self.small_font],
        )
        self.screen.blit(
            focus_surface,
            focus_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 120)),
        )

        question_y = box.y + 140
        for index, line in enumerate(self._wrap_text(quiz.question, 68)[:2]):
            question_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(
                question_surface,
                question_surface.get_rect(center=(SCREEN_WIDTH // 2, question_y + index * 25)),
            )

        letters = ("A", "B", "C")
        for index, rect in enumerate(self._quiz_option_rects()):
            selected = index == self.selected_quiz_option
            fill_color = (226, 202, 128) if selected else (246, 234, 196)
            border_color = TEXT_COLOR if selected else (128, 116, 86)
            pygame.draw.rect(self.screen, fill_color, rect, border_radius=7)
            pygame.draw.rect(self.screen, border_color, rect, 3 if selected else 2, border_radius=7)

            letter_box = pygame.Rect(rect.x + 12, rect.y + 8, 30, 30)
            pygame.draw.rect(self.screen, (248, 238, 190), letter_box, border_radius=5)
            pygame.draw.rect(self.screen, TEXT_COLOR, letter_box, 2, border_radius=5)
            letter_surface = self.font.render(letters[index], True, TEXT_COLOR)
            self.screen.blit(letter_surface, letter_surface.get_rect(center=letter_box.center))

            option_surface = self._render_fitting_text(
                quiz.options[index],
                TEXT_COLOR,
                rect.width - 68,
                [self.font, self.small_font],
            )
            self.screen.blit(option_surface, option_surface.get_rect(midleft=(rect.x + 56, rect.centery)))

        if self.quiz_feedback:
            feedback_lines = self._wrap_text(self.quiz_feedback, 82)[:2]
            for index, line in enumerate(feedback_lines):
                feedback_surface = self.font.render(line, True, (116, 70, 42))
                self.screen.blit(
                    feedback_surface,
                    feedback_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 58 + index * 23)),
                )
        else:
            helper_surface = self.font.render(
                "Setas ou toque escolhem | Enter confirma | C coleção | M menu",
                True,
                (72, 76, 70),
            )
            self.screen.blit(helper_surface, helper_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 38)))

    def _draw_help(self):
        self._draw_menu_scene()
        box = self._help_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)

        title_surface = self.big_font.render("Ajuda rápida", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 44)))

        rows = [
            ("A/D ou setas", "Mover Mig pelos caminhos."),
            ("Espaço / W", "Pular com um pouco de perdão no tempo."),
            ("Toque < >", "Mover Mig no celular."),
            ("Toque Pular", "Pular usando o botão grande da tela."),
            ("Pílulas", "Pegue todas para chamar o Guardião."),
            ("C ou toque C", "Abrir a coleção histórica."),
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

    def _draw_history_block_seal_strip(self, box: pygame.Rect):
        progress = self._history_block_progress()
        seal_width = 128
        seal_height = 46
        gap = 8
        total_width = len(progress) * seal_width + (len(progress) - 1) * gap
        start_x = box.x + 108 + (box.width - 152 - total_width) // 2
        y = box.y + 84

        for index, (block, completed, total, earned) in enumerate(progress):
            rect = pygame.Rect(start_x + index * (seal_width + gap), y, seal_width, seal_height)
            self._draw_history_block_seal(rect, block, completed, total, earned, compact=True)

    def _draw_history_block_seal(
        self,
        rect: pygame.Rect,
        block,
        completed: int,
        total: int,
        earned: bool,
        compact: bool = False,
    ):
        fill_color = (252, 236, 154) if earned else (232, 224, 198)
        border_color = (226, 168, 74) if earned else (150, 132, 92)
        medal_color = (248, 218, 92) if earned else (206, 198, 178)
        text_color = TEXT_COLOR if earned else (88, 88, 84)

        pygame.draw.rect(self.screen, fill_color, rect, border_radius=7)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=7)

        medal_center = (rect.x + (20 if compact else 24), rect.centery)
        medal_radius = 14 if compact else 18
        pygame.draw.circle(self.screen, medal_color, medal_center, medal_radius)
        pygame.draw.circle(self.screen, TEXT_COLOR, medal_center, medal_radius, 2)

        label_surface = self._render_fitting_text(
            block.short_label,
            TEXT_COLOR,
            medal_radius * 2 - 4,
            [self.small_font],
        )
        self.screen.blit(label_surface, label_surface.get_rect(center=medal_center))

        text_left = rect.x + (42 if compact else 50)
        name_surface = self._render_fitting_text(
            self._history_block_display_name(block),
            text_color,
            rect.right - text_left - 8,
            [self.small_font],
        )
        progress_text = "Selo!" if earned else f"{completed}/{total} fases"
        progress_surface = self._render_fitting_text(
            progress_text,
            text_color,
            rect.right - text_left - 8,
            [self.small_font],
        )
        self.screen.blit(name_surface, (text_left, rect.y + (5 if compact else 8)))
        self.screen.blit(progress_surface, (text_left, rect.y + (25 if compact else 32)))

    def _draw_collection(self):
        box = self._collection_box_rect()
        pygame.draw.rect(self.screen, (244, 230, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)
        pygame.draw.rect(self.screen, (214, 184, 118), (box.x, box.y, 76, box.height), border_radius=8)
        pygame.draw.line(self.screen, TEXT_COLOR, (box.x + 76, box.y), (box.x + 76, box.bottom), 2)
        for ring_y in range(box.y + 88, box.bottom - 72, 48):
            pygame.draw.circle(self.screen, (248, 238, 190), (box.x + 38, ring_y), 9)
            pygame.draw.circle(self.screen, TEXT_COLOR, (box.x + 38, ring_y), 9, 2)
            pygame.draw.line(self.screen, (128, 116, 86), (box.x + 38, ring_y), (box.x + 88, ring_y), 2)

        title_surface = self.big_font.render("Coleção histórica", True, TEXT_COLOR)
        collected_count = len(self.collection_entries)
        total_count = get_total_fragment_count()
        count_surface = self.font.render(
            f"Pílulas descobertas: {collected_count}/{total_count}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2 + 26, box.y + 34)))
        self.screen.blit(count_surface, count_surface.get_rect(center=(SCREEN_WIDTH // 2 + 26, box.y + 66)))

        pygame.draw.circle(self.screen, GOAL_COLOR, (box.x + 38, box.y + 48), 18)
        pygame.draw.circle(self.screen, TEXT_COLOR, (box.x + 38, box.y + 48), 18, 2)
        medal_surface = self.font.render(str(collected_count), True, TEXT_COLOR)
        self.screen.blit(medal_surface, medal_surface.get_rect(center=(box.x + 38, box.y + 48)))

        back_rect = self._collection_back_button_rect()
        pygame.draw.rect(self.screen, (226, 202, 128), back_rect, border_radius=6)
        pygame.draw.rect(self.screen, TEXT_COLOR, back_rect, 2, border_radius=6)
        back_surface = self.font.render("Voltar", True, TEXT_COLOR)
        self.screen.blit(back_surface, back_surface.get_rect(center=back_rect.center))

        self._draw_history_block_seal_strip(box)

        rows = self._collection_rows()
        visible_rows = rows[self.collection_scroll: self.collection_scroll + self._collection_visible_rows()]
        y = box.y + 144
        content_x = box.x + 108
        content_width = box.width - 152
        for row_type, text in visible_rows:
            if row_type == "memory_header":
                header_box = pygame.Rect(content_x, y - 3, content_width, 32)
                pygame.draw.rect(self.screen, (218, 232, 190), header_box, border_radius=6)
                pygame.draw.rect(self.screen, (80, 126, 78), header_box, 2, border_radius=6)
                pygame.draw.circle(self.screen, (255, 231, 142), (header_box.x + 17, header_box.centery), 8)
                pygame.draw.circle(self.screen, (80, 126, 78), (header_box.x + 17, header_box.centery), 8, 2)
                surface = self._render_fitting_text(
                    text,
                    TEXT_COLOR,
                    header_box.width - 52,
                    [self.font, self.small_font],
                )
                self.screen.blit(surface, surface.get_rect(midleft=(header_box.x + 34, header_box.centery)))
                y += 40
            elif row_type == "memory_empty":
                empty_box = pygame.Rect(content_x + 18, y, content_width - 36, 42)
                pygame.draw.rect(self.screen, (240, 246, 222), empty_box, border_radius=7)
                pygame.draw.rect(self.screen, (112, 146, 92), empty_box, 1, border_radius=7)
                surface = self._render_fitting_text(
                    text,
                    (82, 106, 72),
                    empty_box.width - 28,
                    [self.font, self.small_font],
                )
                self.screen.blit(surface, surface.get_rect(center=empty_box.center))
                y += 50
            elif row_type == "memory_item":
                card = pygame.Rect(content_x + 18, y, content_width - 36, 54)
                pygame.draw.rect(self.screen, (240, 248, 220), card, border_radius=7)
                pygame.draw.rect(self.screen, (80, 126, 78), card, 2, border_radius=7)
                pygame.draw.circle(self.screen, (255, 205, 86), (card.x + 24, card.y + 27), 11)
                pygame.draw.circle(self.screen, (80, 126, 78), (card.x + 24, card.y + 27), 11, 2)
                pygame.draw.line(self.screen, TEXT_COLOR, (card.x + 18, card.y + 27), (card.x + 23, card.y + 33), 2)
                pygame.draw.line(self.screen, TEXT_COLOR, (card.x + 23, card.y + 33), (card.x + 31, card.y + 20), 2)
                for index, line in enumerate(self._wrap_text(text, 70)[:2]):
                    surface = self._render_fitting_text(
                        line,
                        (58, 78, 58),
                        card.width - 62,
                        [self.font, self.small_font],
                    )
                    self.screen.blit(surface, (card.x + 48, card.y + 7 + index * 22))
                y += 60
            elif row_type == "favorite_header":
                header_box = pygame.Rect(content_x, y - 3, content_width, 32)
                pygame.draw.rect(self.screen, (252, 236, 154), header_box, border_radius=6)
                pygame.draw.rect(self.screen, (226, 168, 74), header_box, 2, border_radius=6)
                pygame.draw.circle(self.screen, (248, 218, 92), (header_box.x + 17, header_box.centery), 8)
                pygame.draw.circle(self.screen, TEXT_COLOR, (header_box.x + 17, header_box.centery), 8, 2)
                surface = self._render_fitting_text(
                    text,
                    TEXT_COLOR,
                    header_box.width - 52,
                    [self.font, self.small_font],
                )
                self.screen.blit(surface, surface.get_rect(midleft=(header_box.x + 34, header_box.centery)))
                y += 40
            elif row_type == "favorite_item":
                card = pygame.Rect(content_x + 18, y, content_width - 36, 54)
                pygame.draw.rect(self.screen, (255, 248, 218), card, border_radius=7)
                pygame.draw.rect(self.screen, (226, 168, 74), card, 2, border_radius=7)
                pygame.draw.polygon(
                    self.screen,
                    FRAGMENT_COLOR,
                    [
                        (card.x + 24, card.y + 13),
                        (card.x + 29, card.y + 24),
                        (card.x + 41, card.y + 24),
                        (card.x + 31, card.y + 31),
                        (card.x + 35, card.y + 43),
                        (card.x + 24, card.y + 36),
                        (card.x + 13, card.y + 43),
                        (card.x + 17, card.y + 31),
                        (card.x + 7, card.y + 24),
                        (card.x + 19, card.y + 24),
                    ],
                )
                pygame.draw.polygon(
                    self.screen,
                    FRAGMENT_OUTLINE,
                    [
                        (card.x + 24, card.y + 13),
                        (card.x + 29, card.y + 24),
                        (card.x + 41, card.y + 24),
                        (card.x + 31, card.y + 31),
                        (card.x + 35, card.y + 43),
                        (card.x + 24, card.y + 36),
                        (card.x + 13, card.y + 43),
                        (card.x + 17, card.y + 31),
                        (card.x + 7, card.y + 24),
                        (card.x + 19, card.y + 24),
                    ],
                    2,
                )
                for index, line in enumerate(self._wrap_text(text, 68)[:2]):
                    surface = self._render_fitting_text(
                        line,
                        (64, 68, 72),
                        card.width - 62,
                        [self.font, self.small_font],
                    )
                    self.screen.blit(surface, (card.x + 52, card.y + 7 + index * 22))
                y += 60
            elif row_type == "header":
                header_box = pygame.Rect(content_x, y - 3, content_width, 32)
                is_album_complete = "Álbum completo!" in text
                header_fill = (252, 236, 154) if is_album_complete else (236, 216, 158)
                header_border = (226, 168, 74) if is_album_complete else (128, 116, 86)
                pygame.draw.rect(self.screen, header_fill, header_box, border_radius=6)
                pygame.draw.rect(
                    self.screen,
                    header_border,
                    header_box,
                    2 if is_album_complete else 1,
                    border_radius=6,
                )
                surface = self._render_fitting_text(
                    text,
                    TEXT_COLOR,
                    header_box.width - 74,
                    [self.font, self.small_font],
                )
                pygame.draw.circle(self.screen, GOAL_COLOR, (header_box.x + 17, header_box.centery), 7)
                if is_album_complete:
                    pygame.draw.circle(
                        self.screen,
                        (255, 248, 214),
                        (header_box.right - 22, header_box.centery),
                        10,
                    )
                    pygame.draw.circle(
                        self.screen,
                        (226, 168, 74),
                        (header_box.right - 22, header_box.centery),
                        10,
                        2,
                    )
                    pygame.draw.line(
                        self.screen,
                        TEXT_COLOR,
                        (header_box.right - 27, header_box.centery),
                        (header_box.right - 23, header_box.centery + 5),
                        2,
                    )
                    pygame.draw.line(
                        self.screen,
                        TEXT_COLOR,
                        (header_box.right - 23, header_box.centery + 5),
                        (header_box.right - 16, header_box.centery - 6),
                        2,
                    )
                self.screen.blit(surface, surface.get_rect(midleft=(header_box.x + 34, header_box.centery)))
                y += 40
            elif row_type == "empty":
                empty_box = pygame.Rect(content_x + 18, y, content_width - 36, 42)
                pygame.draw.rect(self.screen, (248, 238, 204), empty_box, border_radius=7)
                pygame.draw.rect(self.screen, (178, 160, 116), empty_box, 1, border_radius=7)
                surface = self._render_fitting_text(
                    text,
                    (106, 102, 88),
                    empty_box.width - 28,
                    [self.font, self.small_font],
                )
                self.screen.blit(surface, surface.get_rect(center=empty_box.center))
                y += 50
            else:
                card = pygame.Rect(content_x + 18, y, content_width - 36, 54)
                is_recent = bool(self.recent_collection_entry and text == self.recent_collection_entry[1])
                fill_color = (252, 236, 154) if is_recent else (255, 248, 218)
                border_color = (226, 168, 74) if is_recent else (150, 132, 92)
                pygame.draw.rect(self.screen, fill_color, card, border_radius=7)
                pygame.draw.rect(self.screen, border_color, card, 2, border_radius=7)
                pygame.draw.circle(self.screen, FRAGMENT_COLOR, (card.x + 24, card.y + 27), 11)
                pygame.draw.circle(self.screen, FRAGMENT_OUTLINE, (card.x + 24, card.y + 27), 11, 2)
                text_width = card.width - (126 if is_recent else 62)
                for index, line in enumerate(self._wrap_text(text, 62)[:2]):
                    surface = self._render_fitting_text(
                        line,
                        (64, 68, 72),
                        text_width,
                        [self.font, self.small_font],
                    )
                    self.screen.blit(surface, (card.x + 48, card.y + 7 + index * 22))
                if is_recent:
                    badge = pygame.Rect(card.right - 66, card.y + 10, 48, 22)
                    pygame.draw.rect(self.screen, (255, 248, 214), badge, border_radius=6)
                    pygame.draw.rect(self.screen, (226, 168, 74), badge, 2, border_radius=6)
                    badge_surface = self.small_font.render("Novo!", True, TEXT_COLOR)
                    self.screen.blit(badge_surface, badge_surface.get_rect(center=badge.center))
                y += 60

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

        if self.touch_ui_enabled:
            continue_text = "Toque aqui para iniciar."
        else:
            continue_text = "Pressione Enter ou toque aqui para iniciar."
        continue_surface = self.font.render(continue_text, True, TEXT_COLOR)
        self.screen.blit(
            continue_surface,
            continue_surface.get_rect(bottomright=(box.right - 22, box.bottom - 16)),
        )

    def _draw_completion_message(self):
        title = "Fase concluída!"
        if self.recent_history_block_seal:
            subtitle = f"Selo da jornada conquistado: {self.recent_history_block_seal}!"
        elif self.quiz_answered_correctly:
            subtitle = self._guardian_success_text()
        else:
            subtitle = "Medalha recebida: todas as pílulas da fase foram encontradas."
        if self.level_index + 1 >= get_level_count():
            restart = "Enter abre o final | toque continua | R reinicia | C coleção."
        else:
            restart = "Enter avança | toque continua | R reinicia | C coleção."

        box = self._completion_box_rect()
        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        subtitle_surface = self._render_fitting_text(
            subtitle,
            TEXT_COLOR,
            box.width - 92,
            [self.font, self.small_font],
        )
        restart_surface = self.font.render(restart, True, TEXT_COLOR)

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
            "Pergunta para pensar: quem já vivia nesse território?",
            "Pergunta para pensar: o que mudou nesse período?",
            "Pergunta para pensar: por que estudar isso com respeito?",
            "Pergunta para pensar: o que podemos aprender com esse momento?",
        ]
        return questions[self.level_index % len(questions)]

    def _draw_final(self):
        box = self._final_box_rect()
        pygame.draw.rect(self.screen, (248, 238, 190), box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2, border_radius=8)
        pygame.draw.circle(self.screen, (255, 238, 154), (box.x + 62, box.y + 50), 28)
        pygame.draw.circle(self.screen, (226, 168, 74), (box.x + 62, box.y + 50), 28, 2)
        pygame.draw.polygon(
            self.screen,
            (226, 168, 74),
            [(box.x + 46, box.y + 72), (box.x + 62, box.y + 104), (box.x + 78, box.y + 72)],
        )

        title_surface = self.big_font.render("Jornada concluída!", True, TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 44)))

        lines = [
            "Mig viajou de 1500 até o Brasil contemporâneo.",
            "A história do Brasil continua sendo estudada, contada e vivida.",
            "Você montou um mapa de descobertas com curiosidade e respeito.",
        ]
        for index, line in enumerate(lines):
            surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 92 + index * 32)))

        block_progress = self._history_block_progress()
        seal_width = 148
        seal_height = 58
        seal_gap = 10
        total_seal_width = len(block_progress) * seal_width + (len(block_progress) - 1) * seal_gap
        seal_x = SCREEN_WIDTH // 2 - total_seal_width // 2
        seal_y = box.y + 180
        for index, (block, completed, total, earned) in enumerate(block_progress):
            seal_rect = pygame.Rect(
                seal_x + index * (seal_width + seal_gap),
                seal_y,
                seal_width,
                seal_height,
            )
            self._draw_history_block_seal(seal_rect, block, completed, total, earned)

        earned_seals = sum(1 for _block, _completed, _total, earned in block_progress if earned)

        completed_surface = self.font.render(
            f"Fases concluídas: {len(self.completed_levels)}/{get_level_count()}",
            True,
            TEXT_COLOR,
        )
        collected_surface = self.font.render(
            f"Coleção: {len(self.collection_entries)}/{get_total_fragment_count()} pílulas",
            True,
            TEXT_COLOR,
        )
        seals_surface = self.font.render(
            f"Selos da jornada: {earned_seals}/{len(block_progress)}",
            True,
            TEXT_COLOR,
        )
        session_surface = self.font.render(
            f"Descobertas nesta sessão: {self.session_discovery_count}",
            True,
            TEXT_COLOR,
        )
        side_surface = self.font.render(
            f"Lembranças da viagem: {len(self.side_missions_completed)}/{get_level_count()}",
            True,
            TEXT_COLOR,
        )
        closing_surface = self._render_fitting_text(
            "Mensagem final: revisite fases, complete álbuns e conte o que aprendeu.",
            TEXT_COLOR,
            box.width - 72,
            [self.font, self.small_font],
        )
        credits_surface = self._render_fitting_text(
            "Créditos: jogo educativo criado com Python, Pygame-CE e carinho pelo aprendizado.",
            TEXT_COLOR,
            box.width - 72,
            [self.font, self.small_font],
        )
        help_surface = self._render_fitting_text(
            "Enter, M ou toque volta ao menu | C abre coleção | R revisita a última fase",
            TEXT_COLOR,
            box.width - 72,
            [self.font, self.small_font],
        )

        left_stat_x = SCREEN_WIDTH // 2 - 210
        right_stat_x = SCREEN_WIDTH // 2 + 210
        self.screen.blit(completed_surface, completed_surface.get_rect(center=(left_stat_x, box.y + 260)))
        self.screen.blit(collected_surface, collected_surface.get_rect(center=(right_stat_x, box.y + 260)))
        self.screen.blit(seals_surface, seals_surface.get_rect(center=(left_stat_x, box.y + 286)))
        self.screen.blit(session_surface, session_surface.get_rect(center=(right_stat_x, box.y + 286)))
        self.screen.blit(side_surface, side_surface.get_rect(center=(SCREEN_WIDTH // 2, box.y + 316)))
        self.screen.blit(closing_surface, closing_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 82)))
        self.screen.blit(credits_surface, credits_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 62)))
        self.screen.blit(help_surface, help_surface.get_rect(center=(SCREEN_WIDTH // 2, box.bottom - 30)))

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

        font = fonts[-1]
        suffix = "..."
        shortened = text
        while shortened and font.render(f"{shortened}{suffix}", True, color).get_width() > max_width:
            shortened = shortened[:-1].rstrip()

        if shortened:
            return font.render(f"{shortened}{suffix}", True, color)
        return font.render(text[:1], True, color)
