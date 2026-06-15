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
                "jump": self._make_chime([(520, 0.06, 0.16), (660, 0.04, 0.1)]),
                "collect": self._make_chime([(760, 0.04, 0.18), (980, 0.05, 0.18), (1180, 0.07, 0.14)]),
                "checkpoint": self._make_chime([(520, 0.05, 0.14), (660, 0.06, 0.15), (820, 0.08, 0.13)]),
                "complete": self._make_chime([(660, 0.06, 0.18), (840, 0.07, 0.2), (1040, 0.1, 0.18)]),
                "final": self._make_chime([(620, 0.1, 0.16), (780, 0.1, 0.18), (980, 0.16, 0.18)]),
                "bonus": self._make_chime([(680, 0.05, 0.15), (920, 0.06, 0.16)]),
                "correct": self._make_chime([(740, 0.04, 0.15), (960, 0.06, 0.17), (1220, 0.08, 0.14)]),
                "seal": self._make_chime([(540, 0.07, 0.15), (720, 0.08, 0.16), (980, 0.12, 0.18)]),
                "portal": self._make_chime([(420, 0.08, 0.12), (640, 0.08, 0.15), (860, 0.12, 0.16)]),
                "hint": self._make_chime([(360, 0.05, 0.1), (460, 0.08, 0.11)]),
                "menu": self._make_tone(420, 0.07, 0.14),
                "select": self._make_tone(560, 0.06, 0.14),
                "blocked": self._make_chime([(220, 0.07, 0.12), (170, 0.08, 0.1)]),
                "reset": self._make_chime([(300, 0.05, 0.14), (240, 0.1, 0.12)]),
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
        return pygame.mixer.Sound(buffer=self._make_tone_samples(frequency, duration, volume).tobytes())

    def _make_chime(self, tones: list[tuple[int, float, float]]) -> pygame.mixer.Sound:
        samples = array("h")
        for frequency, duration, volume in tones:
            samples.extend(self._make_tone_samples(frequency, duration, volume))

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _make_tone_samples(self, frequency: int, duration: float, volume: float) -> array:
        sample_rate = 44100
        sample_count = int(sample_rate * duration)
        samples = array("h")

        for index in range(sample_count):
            fade = 1 - (index / sample_count)
            value = int(sin(2 * pi * frequency * index / sample_rate) * 32767 * volume * fade)
            samples.append(value)

        return samples
