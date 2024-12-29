"""Module screen_game_over."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.screens.screen_base import ScreenBase


class ScreenGameOver(ScreenBase):
    """Represents a Game Over screen."""

    def __init__(self, game):
        super().__init__(game)

    def _draw(self):
        super()._draw()
        self.game.screen.blit(self.background_screenshot, (0, 0))
        if self.game.is_over and not self.game.winner:
            self.game.screen.blit(*Resource.txt_surfaces['game_over'])
            self.game.screen.blit(*Resource.txt_surfaces['game_over_2'])
        else:
            self.game.screen.blit(*Resource.txt_surfaces['congrats'])
            self.game.screen.blit(*Resource.txt_surfaces['congrats_2'])
            self.game.screen.blit(*Resource.txt_surfaces['you_have_beaten_the_game'])
            self.game.screen.blit(*Resource.txt_surfaces['you_have_beaten_the_game_2'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_2'])

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if (event.type == pg.QUIT
                    or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
                self.game.done = True
                self.done = True
            elif event.type == pg.KEYDOWN:
                if (event.key in (pg.K_KP_ENTER, pg.K_RETURN)
                        and pg.key.get_mods() & pg.KMOD_LCTRL):
                    self.game.done = True
                    self.done = True

    def _game_loop(self):
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            self._draw()
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, *args, **kwargs):
        self.background_screenshot.blit(self.game.screen, (0, 0))

        super().start_up(current_time=self.game.current_time)

        self._game_loop()

        self.game.is_paused = False
