import asyncio

import pygame

from src.levels import create_level, get_level_count
from src.player import Player
from src.settings import (
    FPS,
    GOAL_COLOR,
    GROUND_COLOR,
    PLATFORM_COLOR,
    PLAYER_COLOR,
    PLAYER_OUTLINE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKY_COLOR,
    TEXT_COLOR,
    TITLE,
)


STATE_MENU = "menu"
STATE_INTRO = "intro"
STATE_PLAYING = "playing"
STATE_COMPLETED = "completed"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 44)

        self.level_index = 0
        self.level = create_level(self.level_index)
        self.player = Player(self.level.start_position)
        self.running = True
        self.state = STATE_MENU
        self.camera_x = 0

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self.state != STATE_MENU:
                    self._restart_level()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.state == STATE_MENU:
                    self.state = STATE_INTRO
                elif self.state == STATE_INTRO:
                    self.state = STATE_PLAYING
                elif self.state == STATE_COMPLETED:
                    self._go_to_next_level()

    def _update(self, dt: float):
        if self.state != STATE_PLAYING:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt, self.level.platforms, self.level.width)
        self._update_camera()

        if self.player.rect.colliderect(self.level.goal):
            self.state = STATE_COMPLETED

    def _update_camera(self):
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        max_camera_x = max(0, self.level.width - SCREEN_WIDTH)
        self.camera_x = max(0, min(target_x, max_camera_x))

    def _restart_level(self):
        self.level = create_level(self.level_index)
        self.player = Player(self.level.start_position)
        self.state = STATE_PLAYING
        self.camera_x = 0

    def _go_to_next_level(self):
        self.level_index = (self.level_index + 1) % get_level_count()
        self._restart_level()
        self.state = STATE_INTRO

    def _draw(self):
        self.screen.fill(SKY_COLOR)

        self._draw_background()
        self._draw_level()
        self._draw_player()
        self._draw_hud()

        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_INTRO:
            self._draw_intro()
        elif self.state == STATE_COMPLETED:
            self._draw_completion_message()

        pygame.display.flip()

    def _draw_background(self):
        sun_color = (248, 220, 116)
        ocean_color = (65, 145, 190)
        beach_color = (226, 202, 128)

        pygame.draw.circle(self.screen, sun_color, (820, 88), 38)
        pygame.draw.rect(self.screen, ocean_color, (0, 360, SCREEN_WIDTH, 120))
        pygame.draw.rect(self.screen, beach_color, (0, 430, SCREEN_WIDTH, 52))

    def _draw_level(self):
        for platform in self.level.platforms:
            color = GROUND_COLOR if platform.width >= self.level.width else PLATFORM_COLOR
            pygame.draw.rect(self.screen, color, self._to_screen_rect(platform))

        goal_rect = self._to_screen_rect(self.level.goal)
        pygame.draw.rect(self.screen, GOAL_COLOR, goal_rect)
        pygame.draw.rect(self.screen, (36, 92, 52), goal_rect, 3)

    def _draw_player(self):
        player_rect = self._to_screen_rect(self.player.rect)
        pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect)
        pygame.draw.rect(self.screen, PLAYER_OUTLINE, player_rect, 3)

        eye = pygame.Rect(player_rect.x + 23, player_rect.y + 15, 5, 5)
        pygame.draw.rect(self.screen, PLAYER_OUTLINE, eye)

    def _to_screen_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-self.camera_x, 0)

    def _draw_hud(self):
        title = f"{self.level.year} - {self.level.title}"
        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        mission_surface = self.font.render(self.level.mission, True, TEXT_COLOR)

        self.screen.blit(title_surface, (24, 20))
        self.screen.blit(mission_surface, (24, 64))

    def _draw_menu(self):
        box = pygame.Rect(0, 0, 760, 230)
        box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        title_surface = self.big_font.render(TITLE, True, TEXT_COLOR)
        subtitle_surface = self.font.render(
            "Uma aventura de plataforma pela historia do Brasil.",
            True,
            TEXT_COLOR,
        )
        start_surface = self.font.render("Pressione Enter para comecar.", True, TEXT_COLOR)
        controls_surface = self.font.render(
            "A/D ou setas movem | Espaco pula | Esc sai",
            True,
            TEXT_COLOR,
        )

        self.screen.blit(
            title_surface,
            title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70)),
        )
        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)),
        )
        self.screen.blit(
            start_surface,
            start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)),
        )
        self.screen.blit(
            controls_surface,
            controls_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 74)),
        )

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
        restart = "R reinicia a fase | Enter avanca para a proxima."

        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        subtitle_surface = self.font.render(subtitle, True, TEXT_COLOR)
        note_surface = self.font.render(self.level.historical_note, True, TEXT_COLOR)
        restart_surface = self.font.render(restart, True, TEXT_COLOR)

        box = pygame.Rect(0, 0, 760, 150)
        box.center = (SCREEN_WIDTH // 2, 155)
        pygame.draw.rect(self.screen, (248, 238, 190), box)
        pygame.draw.rect(self.screen, TEXT_COLOR, box, 2)

        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, 105)))
        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 142)),
        )
        self.screen.blit(note_surface, note_surface.get_rect(center=(SCREEN_WIDTH // 2, 174)))
        self.screen.blit(
            restart_surface,
            restart_surface.get_rect(center=(SCREEN_WIDTH // 2, 207)),
        )

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
