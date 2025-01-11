"""Module screen_start_game."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

import pygame as pg
import pygame_gui as pgui

from codemaster.tools.utils.colors import Color
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.screens.screen_base import ScreenBase
from codemaster.tools.logger.logger import log


class ScreenStartGame(ScreenBase):
    """Represents a Start Game screen."""

    def __init__(self, game):
        super().__init__(game)

        text_size_multiplier = 28 if self.game.is_persist_data else 32
        text_start_game_pos_factor_y = 1.34 if self.game.is_persist_data else 1.4

        libg_jp.render_text(
            '– Press Ctrl + Alt + Enter to Start –', Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // text_start_game_pos_factor_y,
                Resource.txt_surfaces, 'game_start', color=Color.CYAN,
                size=int(text_size_multiplier*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text(
            '– Press Ctrl + Alt + Space to Continue Last Game –', Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // 1.44,
                Resource.txt_surfaces, 'game_continue_last', color=Color.CYAN,
                size=int(text_size_multiplier*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text(
            '– Load Last Game Failed. Maybe last game ended as Game Over or a Win ? –',
                Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // 1.44,
                Resource.txt_surfaces, 'game_continue_last_failed', color=Color.RED_DARK,
                size=int(text_size_multiplier*Settings.font_pos_factor_t2), align="center")

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_black_t1'], (0, 0))
        self.game.screen.blit(
            Resource.images['screen_start'],
            (Settings.screen_width // 2 - Resource.images['screen_start'].get_width() // 2, 0))
        self.game.screen.blit(
            Resource.images['help_key'],
            (50 * Settings.font_pos_factor,
             Settings.screen_height - Resource.images['help_key'].get_height()
             - 28 * Settings.font_pos_factor))
        self.game.screen.blit(
            Resource.images['logo_jp'],
            (Settings.screen_width - Resource.images['logo_jp'].get_width()
             - 44 * Settings.font_pos_factor,
             Settings.screen_height - Resource.images['logo_jp'].get_height()
             - 32 * Settings.font_pos_factor))
        self.game.screen.blit(
            Resource.images['seal_just_a_demo'],
            (Settings.screen_width // 2 - Resource.images['seal_just_a_demo'].get_width() // 2,
             Settings.screen_height // 1.05 - Resource.images['seal_just_a_demo'].get_height() // 1.05))
        self.game.screen.blit(*Resource.txt_surfaces['game_start'])

        if self.game.is_persist_data:
            if self.game.is_load_last_game_failed:
                self.game.screen.blit(*Resource.txt_surfaces['game_continue_last_failed'])
            else:
                self.game.screen.blit(*Resource.txt_surfaces['game_continue_last'])

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.set_is_exit_game(True)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.game.screen_help.start_up()
                    self.done = True
                elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                    if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT:
                        self.game.__class__.new_game = True
                elif event.key == pg.K_SPACE:
                    if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT:
                        if self.game.is_persist_data:
                            self.game.is_continue_game = True
                elif event.key == pg.K_KP_DIVIDE:
                    if self.game.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL \
                            and pg.key.get_mods() & pg.KMOD_LALT:
                        if log.level != logging.DEBUG:
                            log.setLevel(logging.DEBUG)
                            self.game.__class__.is_log_debug = True
                            log.info("Set logger level to: Debug")
                        else:
                            log.setLevel(logging.INFO)
                            self.game.__class__.is_log_debug = False
                            log.info("Set logger level to: Info")
            # Manage In Game UI events
            self.game.ui_manager.ui_main_menu.manager.process_events(event)
            if event.type == pgui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if event.ui_element == self.game.ui_manager.ui_main_menu.items[
                    'delete_saved_game_confirm_dialog']:
                    self.game.ui_manager.ui_main_menu.delete_game_directory_action()

        if self.game.is_exit_game:
            self.game.is_start_screen = False
            self.done = True
        elif self.game.__class__.new_game:
            self.game.is_start_screen = False
            self.game.is_continue_game = False
            self.done = True
        elif self.game.is_continue_game:
            self.game.is_start_screen = False
            self.done = True

        if self.done:
            self.game.ui_manager.ui_main_menu.hide_additional_game_items()
            self.game.ui_manager.ui_main_menu.clean_ui_items()

    def _game_loop(self):
        ui_ingame_manager = self.game.ui_manager.ui_main_menu.manager
        clock = pg.time.Clock()
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)

            try:
                ui_ingame_manager.update(self.game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            self._draw()
            ui_ingame_manager.draw_ui(self.game.screen)

            pg.display.flip()
            clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, *args, **kwargs):
        super().start_up(current_time=self.game.current_time)

        self.game.is_start_screen = True
        self.game.persistence_path_from_user = ''

        self._game_loop()
