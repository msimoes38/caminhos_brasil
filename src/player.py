import pygame

from src.settings import GRAVITY, PLAYER_JUMP_SPEED, PLAYER_SPEED


class Player:
    def __init__(self, position: tuple[int, int]):
        self.rect = pygame.Rect(position[0], position[1], 36, 56)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def handle_input(self, keys: pygame.key.ScancodeWrapper):
        self.velocity.x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED

        wants_to_jump = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        if wants_to_jump and self.on_ground:
            self.velocity.y = -PLAYER_JUMP_SPEED
            self.on_ground = False

    def update(self, dt: float, platforms: list[pygame.Rect], level_width: int):
        self.velocity.y += GRAVITY * dt

        self.rect.x += round(self.velocity.x * dt)
        self._resolve_horizontal_collisions(platforms)
        self._keep_inside_level_bounds(level_width)

        self.rect.y += round(self.velocity.y * dt)
        self._resolve_vertical_collisions(platforms)

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
