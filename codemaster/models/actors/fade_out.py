"""Module fade_out."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg


class FadeOut(pg.sprite.Sprite):
    def __init__(self, delay=0):
        super().__init__()

        self.delay = delay
        self.rect = pg.display.get_surface().get_rect()
        self.image = pg.Surface(self.rect.size, flags=pg.SRCALPHA)
        self.alpha = 0

    def update(self):
        if self.delay > 0:
            self.delay -= 1
            return

        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha < 255:
            self.alpha += 0.65

    def die_hard(self):
        pass
