"""Module screen_base."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.config.settings import Settings


class ScreenBase:
    """Represents a screen base.
    It is not intended to be instantiated.
    """
    def __init__(self, game):
        self.start_time = 0
        self.current_time = 0
        self.persistant = True
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.game = game
        self.background_screenshot = pg.Surface((Settings.screen_width, Settings.screen_height))

    def start_up(self, current_time=None, *args, **kwargs):
        self.start_time = current_time
        self.done = False
        pg.display.set_caption(self.game.name_short)
        self._draw()
        pg.event.clear()

    def _draw(self):
        """This method is expected to be overridden by Screen subclasses."""
        pass

    def _full_screen_switch_hook(self):
        """This method will be executed before a full or normal screen switch."""
        pass

    def _events_handle(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                    if pg.key.get_mods() & pg.KMOD_ALT and not pg.key.get_mods() & pg.KMOD_LCTRL:
                        self._full_screen_switch_hook()
                        libg_jp.full_screen_switch(self.game)
                        self._draw()
                elif event.key == pg.K_m:
                    if pg.key.get_mods() & pg.KMOD_LALT:
                        self.game.is_music_paused = not self.game.is_music_paused
                        if self.game.is_music_paused:
                            pg.mixer.music.pause()
                        else:
                            pg.mixer.music.unpause()
                elif not isinstance(self, self.game.screen_start_game.__class__) \
                        and not self.game.is_start_screen:
                    if event.key == pg.K_F1 and not self.game.is_over:
                        if not isinstance(self, self.game.screen_cutscene.__class__):
                            self.game.is_help_screen = True
                            self.done = True
                    elif event.key == pg.K_h:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.game.help_info.print_help_keys()
                            if self.game.is_debug:
                                self.game.debug_info.print_help_keys()
