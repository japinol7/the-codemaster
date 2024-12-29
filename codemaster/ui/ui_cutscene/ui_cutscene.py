"""Module ui_cutscene."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.config.constants import (
    UI_X_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from codemaster.ui.ui_main_utils.ui_main_utils import clean_general_ui_items


class UICutscene:
    def __init__(self, game):
        self.game = game
        self.game.__class__.ui_cutscene = pgui.UIManager(game.size, theme_path=UI_MAIN_THEME_FILE)
        self.manager = self.game.__class__.ui_cutscene
        self.items = {}

        self._add_items()

    def clean_game_data(self):
        self.game = None

    def set_game_data(self, game):
        self.game = game

    def clean_ui_items(self):
        clean_general_ui_items(self)

    def hide_additional_game_items(self):
        pass

    def _add_items(self):
        def pause_cutscene_action():
            self.game.is_paused = not self.game.is_paused

            if self.game.is_paused:
                self.game.screen_cutscene.background_screenshot.blit(self.game.screen, (0, 0))
            else:
                self.hide_additional_game_items()
                self.clean_ui_items()

        def skip_cutscene_action():
            self.game.level_cutscene.cutscene.update_pc_leave_level()

        button_pos_x = 466
        button_pos_y = 720
        button_size = 110, 40
        self.items['pause_cutscene'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Pause on/off",
            manager=self.manager,
            command=pause_cutscene_action,
            )
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['skip_cutscene'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Skip",
            manager=self.manager,
            command=skip_cutscene_action,
            )
