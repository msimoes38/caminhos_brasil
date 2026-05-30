from collections import deque

import pygame

from src.settings import (
    GRAVITY,
    PLAYER_AIR_ACCELERATION,
    PLAYER_ANIMATION_FRAMES,
    PLAYER_COYOTE_TIME,
    PLAYER_DRAW_SIZE,
    PLAYER_FRICTION,
    PLAYER_GROUND_ACCELERATION,
    PLAYER_JUMP_SPEED,
    PLAYER_JUMP_BUFFER_TIME,
    PLAYER_MAX_FALL_SPEED,
    PLAYER_SPEED,
    PLAYER_SPRITE_PATH,
)


class Player:
    def __init__(self, position: tuple[int, int]):
        self.rect = pygame.Rect(position[0], position[1], 36, 56)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True
        self.animations = self._load_animations()
        self.animation_name = "idle"
        self.animation_time = 0
        self.current_frame_index = 0
        self.coyote_timer = 0
        self.jump_buffer_timer = 0
        self.jump_was_pressed = False
        self.jump_started = False

    def handle_input(
        self,
        keys: pygame.key.ScancodeWrapper,
        dt: float,
        touch_direction: int = 0,
        touch_jump_held: bool = False,
        touch_jump_pressed: bool = False,
    ):
        self.jump_started = False
        horizontal_direction = touch_direction

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            horizontal_direction -= 1
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            horizontal_direction += 1
            self.facing_right = True
        horizontal_direction = max(-1, min(1, horizontal_direction))
        if touch_direction < 0:
            self.facing_right = False
        elif touch_direction > 0:
            self.facing_right = True

        target_speed = horizontal_direction * PLAYER_SPEED
        if horizontal_direction:
            acceleration = PLAYER_GROUND_ACCELERATION if self.on_ground else PLAYER_AIR_ACCELERATION
            self.velocity.x = self._approach(
                self.velocity.x,
                target_speed,
                PLAYER_SPEED * acceleration * dt,
            )
        else:
            friction = PLAYER_FRICTION if self.on_ground else PLAYER_FRICTION * 0.22
            self.velocity.x = self._approach(self.velocity.x, 0, PLAYER_SPEED * friction * dt)

        if self.on_ground:
            self.coyote_timer = PLAYER_COYOTE_TIME
        else:
            self.coyote_timer = max(0, self.coyote_timer - dt)

        keyboard_jump_held = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        wants_to_jump = keyboard_jump_held or touch_jump_held
        if (wants_to_jump and not self.jump_was_pressed) or touch_jump_pressed:
            self.jump_buffer_timer = PLAYER_JUMP_BUFFER_TIME
        self.jump_was_pressed = wants_to_jump

        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self._start_jump()

        self.jump_buffer_timer = max(0, self.jump_buffer_timer - dt)

    def update(self, dt: float, platforms: list[pygame.Rect], level_width: int):
        self.velocity.y += GRAVITY * dt
        self.velocity.y = min(self.velocity.y, PLAYER_MAX_FALL_SPEED)

        self.rect.x += round(self.velocity.x * dt)
        self._resolve_horizontal_collisions(platforms)
        self._keep_inside_level_bounds(level_width)

        self.rect.y += round(self.velocity.y * dt)
        self._resolve_vertical_collisions(platforms)
        self._update_animation(dt)

    def _start_jump(self):
        self.velocity.y = -PLAYER_JUMP_SPEED
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer_timer = 0
        self.jump_started = True

    def _approach(self, current: float, target: float, amount: float) -> float:
        if current < target:
            return min(current + amount, target)
        if current > target:
            return max(current - amount, target)
        return target

    def _keep_inside_level_bounds(self, level_width: int):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level_width:
            self.rect.right = level_width

    def _resolve_horizontal_collisions(self, platforms: list[pygame.Rect]):
        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            if self.velocity.x > 0:
                self.rect.right = platform.left
            elif self.velocity.x < 0:
                self.rect.left = platform.right

    def _resolve_vertical_collisions(self, platforms: list[pygame.Rect]):
        self.on_ground = False

        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue

            if self.velocity.y > 0:
                self.rect.bottom = platform.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = platform.bottom
                self.velocity.y = 0

        if not self.on_ground and self.velocity.y >= 0:
            self._check_ground_below(platforms)

    def _check_ground_below(self, platforms: list[pygame.Rect]):
        foot_probe = self.rect.move(0, 1)

        for platform in platforms:
            if foot_probe.colliderect(platform):
                self.on_ground = True
                self.velocity.y = 0
                return

    def draw(self, screen: pygame.Surface, camera_x: int):
        draw_rect = self._get_draw_rect(camera_x)
        sprite = self._get_current_sprite()

        if sprite:
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, draw_rect)
            return

        pygame.draw.rect(screen, (235, 196, 82), draw_rect)
        pygame.draw.rect(screen, (74, 52, 38), draw_rect, 3)

    def _get_draw_rect(self, camera_x: int) -> pygame.Rect:
        draw_rect = pygame.Rect((0, 0), PLAYER_DRAW_SIZE)
        draw_rect.midbottom = (self.rect.centerx - camera_x, self.rect.bottom)
        return draw_rect

    def _load_animations(self) -> dict[str, list[pygame.Surface]]:
        try:
            sheet = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()
        except (FileNotFoundError, pygame.error):
            return {}

        animations = {}

        for name, frame_rects in PLAYER_ANIMATION_FRAMES.items():
            frames = []
            for frame_rect in frame_rects:
                frame = sheet.subsurface(pygame.Rect(frame_rect)).copy()
                self._remove_light_background(frame)
                frames.append(pygame.transform.smoothscale(frame, PLAYER_DRAW_SIZE))
            animations[name] = frames

        return animations

    def _remove_light_background(self, surface: pygame.Surface):
        width, height = surface.get_size()
        visited = set()
        queue = deque()

        for x in range(width):
            queue.append((x, 0))
            queue.append((x, height - 1))
        for y in range(height):
            queue.append((0, y))
            queue.append((width - 1, y))

        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            visited.add((x, y))
            color = surface.get_at((x, y))
            if not self._is_light_background(color):
                continue

            surface.set_at((x, y), (255, 255, 255, 0))
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    def _is_light_background(self, color: pygame.Color) -> bool:
        return color.r >= 238 and color.g >= 238 and color.b >= 238

    def _update_animation(self, dt: float):
        next_animation = self._choose_animation()
        if next_animation != self.animation_name:
            self.animation_name = next_animation
            self.animation_time = 0
            self.current_frame_index = 0

        frames = self.animations.get(self.animation_name, [])
        if len(frames) <= 1:
            return

        self.animation_time += dt
        if self.animation_time >= 0.14:
            self.animation_time = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(frames)

    def _choose_animation(self) -> str:
        if not self.on_ground:
            if self.velocity.y < 0:
                return "jump"
            return "fall"

        if self.velocity.x != 0:
            return "walk"

        return "idle"

    def _get_current_sprite(self) -> pygame.Surface | None:
        frames = self.animations.get(self.animation_name, [])
        if not frames:
            return None

        return frames[self.current_frame_index % len(frames)]
