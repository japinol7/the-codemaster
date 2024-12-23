"""Module screen."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

import pygame as pg
import pygame_gui as pgui

from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.config.settings import Settings
from codemaster.tools.utils import utils
from codemaster.models.actors.actors import NPC, ActorItem
from codemaster.tools.logger.logger import log


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
                elif not isinstance(self, StartGame) and not self.game.is_start_screen:
                    if event.key == pg.K_F1 and not self.game.is_over:
                        self.game.is_help_screen = True
                        self.done = True
                    elif event.key == pg.K_h:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.game.help_info.print_help_keys()
                            if self.game.is_debug:
                                self.game.debug_info.print_help_keys()


class ExitCurrentGame(Screen):
    """Represents an Exit Current Game screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self, current_time=None, *args, **kwargs):
        super().start_up(current_time=self.game.current_time)

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)
        self.game.is_exit_curr_game_confirm = False

    def _draw(self):
        super()._draw()

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
                    self.done = True


class GameOver(Screen):
    """Represents a Game Over screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self, current_time=None, *args, **kwargs):
        self.background_screenshot.blit(self.game.screen, (0, 0))

        super().start_up(current_time=self.game.current_time)

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            self._draw()
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)
        self.game.is_paused = False

    def _draw(self):
        super()._draw()

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


class Help(Screen):
    """Represents a Help screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self, current_time=None, *args, **kwargs):
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


class Pause(Screen):
    """Represents a Pause screen."""

    def __init__(self, game):
        super().__init__(game)
        self.is_full_screen_switch = False

    def start_up(self, current_time=None, is_full_screen_switch=False, *args, **kwargs):
        self.background_screenshot.blit(self.game.screen, (0, 0))

        pg.mouse.set_visible(True)
        self.is_full_screen_switch = is_full_screen_switch
        if self.is_full_screen_switch:
            self._full_screen_switch_hook()
            libg_jp.full_screen_switch(self.game)

        super().start_up(current_time=self.game.current_time)

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)

            try:
                self.game.__class__.ui_ingame.update(self.game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            self._draw()

            self.game.__class__.ui_ingame.draw_ui(self.game.screen)

            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)

        self.game.is_paused = False
        self.game.is_full_screen_switch = False
        pg.mouse.set_visible(False)

    def _full_screen_switch_hook(self):
        self.is_full_screen_switch = True

    def _draw(self):
        super()._draw()

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.is_exit_curr_game_confirm = True
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p and pg.key.get_mods() & pg.KMOD_LCTRL:
                    self.done = True
                elif event.key == pg.K_F1:
                    self.game.is_help_screen = True
                    self.done = True
                # Super cheat input events
                elif self.game.super_cheat:
                    if event.key == pg.K_KP_MINUS and pg.key.get_mods() & pg.KMOD_LCTRL:
                        self.game.debug_info.super_cheat_superhero()
                        log.info(f"Replenish stats to superhero maximum (cheat).")
                    elif event.key == pg.K_KP_MULTIPLY and pg.key.get_mods() & pg.KMOD_LCTRL:
                        self.game.player.invulnerable = not self.game.player.invulnerable
                        log.info(f"Set player invulnerability state to: "
                                 f"{self.game.player.invulnerable} (cheat)")

            # Debug input events
            if self.game.is_debug and event.type == pg.KEYDOWN:
                if event.key == pg.K_d and pg.key.get_mods() & pg.KMOD_LCTRL:
                    self.game.debug_info.print_debug_info()
                elif event.key == pg.K_l and pg.key.get_mods() & pg.KMOD_LCTRL:
                    self.game.debug_info.print_debug_info(to_log_file=True)
                elif (event.key == pg.K_KP_DIVIDE and pg.key.get_mods() & pg.KMOD_LCTRL
                      and pg.key.get_mods() & pg.KMOD_LALT):
                    if log.level != logging.DEBUG:
                        log.setLevel(logging.DEBUG)
                        self.game.__class__.is_log_debug = True
                        log.info("Set logger level to: Debug")
                    else:
                        log.setLevel(logging.INFO)
                        self.game.__class__.is_log_debug = False
                        log.info("Set logger level to: Info")
                elif event.key == pg.K_g:
                    if pg.key.get_mods() & pg.KMOD_LCTRL \
                            and pg.key.get_mods() & pg.KMOD_RALT:
                        self.game.show_grid = not self.game.show_grid

            # Debug input events with debug and log debug activated
            if self.game.is_log_debug and event.type == pg.KEYDOWN:
                if event.key == pg.K_n:
                    if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT \
                            and pg.key.get_mods() & pg.KMOD_LSHIFT:
                        log.debug("NPCs health from all levels, ordered by NPC name:")
                        log.debug("\n" + utils.pretty_dict_to_string(
                            NPC.get_npc_ids_health(self.game, sorted_by_level=False)))
                    elif pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LSHIFT:
                        log.debug("NPCs health from all levels, ordered by level:")
                        log.debug("\n" + utils.pretty_dict_to_string(NPC.get_npc_ids_health(self.game)))
                    elif pg.key.get_mods() & pg.KMOD_LALT and pg.key.get_mods() & pg.KMOD_LSHIFT:
                        log.debug("Items from all levels, ordered by level:")
                        log.debug("\n" + utils.pretty_dict_to_string(
                            ActorItem.get_all_item_ids_basic_info(self.game)))
                    elif pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT:
                        log.debug("Items from all levels, ordered by item name:")
                        log.debug("\n" + utils.pretty_dict_to_string(
                            ActorItem.get_all_item_ids_basic_info(self.game, sorted_by_level=False)))
                    elif pg.key.get_mods() & pg.KMOD_LCTRL:
                        log.debug("NPCs health from the current level %i:", self.game.level.id)
                        log.debug("\n" + utils.pretty_dict_to_string(
                            NPC.get_npc_ids_health_from_level(self.game.level)))
                    elif pg.key.get_mods() & pg.KMOD_LALT:
                        log.debug("Items from the current level %i:", self.game.level.id)
                        log.debug("\n" + utils.pretty_dict_to_string(
                            ActorItem.get_all_item_ids_basic_info_from_level(self.game.level)))

            # Manage In Game UI events
            self.game.__class__.ui_ingame.process_events(event)

            if self.done:
                self.game.ui_manager.ui_ingame.hide_additional_game_items()
                self.game.ui_manager.ui_ingame.clean_ui_items()


class StartGame(Screen):
    """Represents a Start Game screen."""

    def __init__(self, game):
        super().__init__(game)

    def start_up(self, current_time=None, *args, **kwargs):
        super().start_up(current_time=self.game.current_time)
        clock = pg.time.Clock()
        self.game.is_start_screen = True
        self.game.persistence_path_from_user = ''

        while not self.done:
            events = pg.event.get()
            self._events_handle(events)

            try:
                self.game.__class__.ui_main_menu.update(self.game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            self._draw()
            self.game.__class__.ui_main_menu.draw_ui(self.game.screen)

            pg.display.flip()
            clock.tick(Settings.fps_paused)

    def _draw(self):
        super()._draw()

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
            self.game.__class__.ui_main_menu.process_events(event)
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
