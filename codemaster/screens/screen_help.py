"""Module screen_help."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.screens.screen_base import ScreenBase


class ScreenHelp(ScreenBase):
    """Represents a help screen."""

    def __init__(self, game):
        super().__init__(game)

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(
            Resource.images['screen_help'],
            (Settings.screen_width // 2 - Resource.images['screen_help'].get_width() // 2,
             Settings.screen_height // 2 - Resource.images['screen_help'].get_height() // 2))

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.game.is_start_screen:
                    self.done = True
                else:
                    self.game.is_exit_game = True
                    self.game.is_exit_curr_game_confirm = True
                    self.done = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_F1:
                self.done = True

    def _game_loop(self):
        clock = pg.time.Clock()
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, *args, **kwargs):
        super().start_up(current_time=self.game.current_time)

        self._game_loop()

        self.game.is_help_screen = False
