"""Module screen_cutscene."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.config.settings import Settings
from codemaster.resources import Resource
from codemaster.level_scroll_screen import (
    level_scroll_shift_control,
    change_screen_level,
    )
from codemaster.screens.screen_base import ScreenBase
from codemaster.tools.logger.logger import log


class ScreenCutScene(ScreenBase):
    """Represents a cutscene screen."""

    def __init__(self, game):
        super().__init__(game)
        self.is_full_screen_switch = False

    def _full_screen_switch_hook(self):
        self.is_full_screen_switch = True

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.level_cutscene.cutscene.update_pc_leave_level()
                self.game.is_exit_curr_game_confirm = True
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p and pg.key.get_mods() & pg.KMOD_LCTRL:
                    self.game.is_paused = not self.game.is_paused
                    if not self.game.is_paused:
                        self.game.ui_manager.ui_cutscene.hide_additional_game_items()
                        self.game.ui_manager.ui_cutscene.clean_ui_items()

            # Manage In Game UI events
            self.game.__class__.ui_cutscene.process_events(event)

    def _game_loop(self):
        game = self.game
        game.update_state_counter = -1
        while not self.done:
            # Increase and check counter to delay stats x iterations
            game.update_state_counter += 1
            if game.update_state_counter > 20:
                game.update_state_counter = 0

            events = pg.event.get()
            self._events_handle(events)

            if game.level_cutscene.done:
                self.done = True
                break

            try:
                game.__class__.ui_cutscene.update(game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            level_scroll_shift_control(game)

            if not game.is_paused:
                # update sprites and level
                game.active_sprites.update()
                game.level_cutscene.update()

            # Draw cutscene level sprites
            game.level_cutscene.draw()
            game.active_sprites.draw(game.screen)

            for text_msg in game.text_msg_sprites:
                text_msg.draw_text()
            for clock in game.clock_sprites:
                clock.draw_text()

            if not game.is_paused:
                for sprite in game.level_cutscene.particle_tuple_sprites:
                    sprite.update_particle_sprites()
                for sprite in game.level_cutscene.particle_sprites:
                    sprite.update_particle_sprites()

            if game.is_magic_on:
                for selector in game.selector_sprites:
                    selector.update()
                game.selector_sprites.draw(game.screen)

            game.level_cutscene.magic_sprites.draw(game.screen)

            if game.is_paused:
                game.screen.blit(*Resource.txt_surfaces['game_paused'])
            game.screen.blit(Resource.images['seal_cutscene'], (488, 0))

            game.__class__.ui_cutscene.draw_ui(game.screen)

            pg.display.flip()
            game.is_paused and game.clock.tick(Settings.fps_paused) or game.clock.tick(Settings.fps)

    def start_up(self, current_time=None, is_full_screen_switch=False, *args, **kwargs):
        game = self.game
        self.background_screenshot.blit(game.screen, (0, 0))

        pg.mouse.set_visible(True)
        self.is_full_screen_switch = is_full_screen_switch
        if self.is_full_screen_switch:
            self._full_screen_switch_hook()
            libg_jp.full_screen_switch(game)

        super().start_up(current_time=game.current_time)

        self._game_loop()

        game.ui_manager.ui_cutscene.hide_additional_game_items()
        game.ui_manager.ui_cutscene.clean_ui_items()

        change_screen_level(
            game,
            door=game.level_cutscene.level_to_return_door)
        game.level_cutscene = None

        game.is_paused = False
        game.is_cutscene_screen = False
        game.is_full_screen_switch = False
        pg.mouse.set_visible(False)
