"""Module screens."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.utils.colors import Color
from codemaster.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.config.settings import Settings


class Screen:
    """Represents a screen."""
    def __init__(self, game):
        self.start_time = 0
        self.current_time = 0
        self.persistant = True
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.game = game

    def start_up(self, current_time):
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
                    if pg.key.get_mods() & pg.KMOD_ALT:
                        self._full_screen_switch_hook()
                        libg_jp.full_screen_switch(self.game)
                        self._draw()
                    else:
                        self.done = True
                elif event.key == pg.K_m:
                    if pg.key.get_mods() & pg.KMOD_LCTRL:
                        self.game.is_music_paused = not self.game.is_music_paused
                        if self.game.is_music_paused:
                            pg.mixer.music.pause()
                        else:
                            pg.mixer.music.unpause()
                elif not isinstance(self, StartGame) and not self.game.is_start_screen:
                    if event.key == pg.K_F1 and not self.game.is_over:
                        self.game.is_help_screen = True
                        self.done = True
                    elif event.key == pg.K_h:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.game.help_info.print_help_keys()
                            self.game.debug_info.print_help_keys()
                    elif event.key == pg.K_d:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.game.debug_info.print_debug_info()
                    elif event.key == pg.K_l:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.game.debug_info.print_debug_info(to_log_file=True)


class ExitCurrentGame(Screen):
    """Represents an Exit Current Game screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self):
        super().start_up(current_time=self.game.current_time)

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)
        self.game.is_exit_curr_game_confirm = False

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['exit_current_game_confirm'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_2'])
        self.game.screen.blit(Resource.images['seal_just_a_demo'],
                              (Settings.screen_width // 2 - Resource.images['seal_just_a_demo'].get_width() // 2,
                               Settings.screen_height // 1.16 - Resource.images['seal_just_a_demo'].get_height() // 1.16
                               ))

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                self.game.done = True
                self.done = True


class GameOver(Screen):
    """Represents a Game Over screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self):
        super().start_up(current_time=self.game.current_time)

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)
        self.game.is_paused = False

    def _draw(self):
        super()._draw()
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
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key in(pg.K_ESCAPE, pg.K_KP_ENTER, pg.K_RETURN)):
                self.game.done = True
                self.done = True


class Help(Screen):
    """Represents a Help screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self):
        super().start_up(current_time=self.game.current_time)
        clock = pg.time.Clock()

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            clock.tick(Settings.fps_paused)
        self.game.is_help_screen = False

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(Resource.images['screen_help'],
                              (Settings.screen_width // 2 - Resource.images['screen_help'].get_width() // 2,
                               Settings.screen_height // 2 - Resource.images['screen_help'].get_height() // 2))

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.is_exit_game = True
                self.game.is_exit_curr_game_confirm = True
                self.done = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_F1:
                self.done = True


class Pause(Screen):
    """Represents a Pause screen."""

    def __init__(self, game):
        super().__init__(game)
        self.background_screenshot = None
        self.is_full_screen_switch = False

    def start_up(self, is_full_screen_switch=False):
        self.is_full_screen_switch = is_full_screen_switch
        if self.is_full_screen_switch:
            self._full_screen_switch_hook()
            libg_jp.full_screen_switch(self.game)

        super().start_up(current_time=self.game.current_time)

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)
        self.game.is_paused = False
        self.game.is_full_screen_switch = False
        self.background_screenshot = None

    def _full_screen_switch_hook(self):
        self.is_full_screen_switch = True
        self.background_screenshot = pg.Surface((Settings.screen_width, Settings.screen_height))
        self.background_screenshot.blit(self.game.screen, (0, 0))

    def _draw(self):
        super()._draw()
        if self.is_full_screen_switch:
            self.game.screen.blit(self.background_screenshot, (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['game_paused'])
        self.game.screen.blit(Resource.images['dim_screen'], (0, 0))

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.is_exit_curr_game_confirm = True
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.done = True
                elif event.key == pg.K_F1:
                    self.game.is_help_screen = True
                    self.done = True


class StartGame(Screen):
    """Represents a Start Game screen."""

    def __init__(self, game):
        super().__init__(game)
        libg_jp.render_text('– Press Enter to Start –', Settings.screen_width // 2,
                            114 * Settings.font_pos_factor_t2 + Settings.screen_height // 1.82,
                            Resource.txt_surfaces, 'game_start', color=Color.CYAN,
                            size=int(96*Settings.font_pos_factor_t2), align="center")

    def start_up(self):
        super().start_up(current_time=self.game.current_time)
        clock = pg.time.Clock()
        self.game.is_start_screen = True

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            clock.tick(Settings.fps_paused)

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_black_t1'], (0, 0))
        self.game.screen.blit(Resource.images['screen_start'],
                              (Settings.screen_width // 2 - Resource.images['screen_start'].get_width() // 2, 0))
        self.game.screen.blit(Resource.images['help_key'],
                              (50 * Settings.font_pos_factor,
                              Settings.screen_height - Resource.images['help_key'].get_height()
                              - 35 * Settings.font_pos_factor))
        self.game.screen.blit(Resource.images['logo_jp'],
                              (Settings.screen_width - Resource.images['logo_jp'].get_width()
                              - 36 * Settings.font_pos_factor,
                              Settings.screen_height - Resource.images['logo_jp'].get_height()
                              - 36 * Settings.font_pos_factor))
        self.game.screen.blit(Resource.images['seal_just_a_demo'],
                              (Settings.screen_width // 2 - Resource.images['seal_just_a_demo'].get_width() // 2,
                               Settings.screen_height // 1.16 - Resource.images['seal_just_a_demo'].get_height() // 1.16
                               ))
        self.game.screen.blit(*Resource.txt_surfaces['game_start'])

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.is_start_screen = False
                self.game.set_is_exit_game(True)
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.game.screen_help.start_up()
                    self.done = True
                elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                    self.game.is_start_screen = False
