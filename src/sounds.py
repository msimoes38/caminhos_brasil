from array import array
from math import pi, sin

import pygame


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.sounds = {
                "jump": self._make_tone(520, 0.08, 0.18),
                "collect": self._make_tone(760, 0.1, 0.22),
                "checkpoint": self._make_tone(620, 0.14, 0.2),
                "complete": self._make_tone(880, 0.18, 0.24),
                "final": self._make_tone(980, 0.28, 0.22),
                "menu": self._make_tone(420, 0.07, 0.14),
                "select": self._make_tone(560, 0.06, 0.14),
                "blocked": self._make_tone(180, 0.12, 0.14),
                "reset": self._make_tone(240, 0.12, 0.16),
            }
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def play(self, name: str):
        if not self.enabled:
            return

        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def _make_tone(self, frequency: int, duration: float, volume: float) -> pygame.mixer.Sound:
        sample_rate = 44100
        sample_count = int(sample_rate * duration)
        samples = array("h")

        for index in range(sample_count):
            fade = 1 - (index / sample_count)
            value = int(sin(2 * pi * frequency * index / sample_rate) * 32767 * volume * fade)
            samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())
