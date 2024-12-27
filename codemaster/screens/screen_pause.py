"""Module screen_pause."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

import pygame as pg

from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.tools.utils import utils
from codemaster.models.actors.actors import NPC, ActorItem
from codemaster.screens.screen_base import ScreenBase
from codemaster.tools.logger.logger import log


class ScreenPause(ScreenBase):
    """Represents a pause screen."""

    def __init__(self, game):
        super().__init__(game)
        self.is_full_screen_switch = False

    def _full_screen_switch_hook(self):
        self.is_full_screen_switch = True

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

    def _game_loop(self):
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)

            try:
                self.game.__class__.ui_ingame.update(self.game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            self.game.screen.blit(self.background_screenshot, (0, 0))
            self.game.screen.blit(*Resource.txt_surfaces['game_paused'])

            self.game.__class__.ui_ingame.draw_ui(self.game.screen)

            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, is_full_screen_switch=False, *args, **kwargs):
        self.background_screenshot.blit(self.game.screen, (0, 0))

        pg.mouse.set_visible(True)
        self.is_full_screen_switch = is_full_screen_switch
        if self.is_full_screen_switch:
            self._full_screen_switch_hook()
            libg_jp.full_screen_switch(self.game)

        super().start_up(current_time=self.game.current_time)

        self._game_loop()

        self.game.is_paused = False
        self.game.is_full_screen_switch = False
        pg.mouse.set_visible(False)
