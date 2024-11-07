"""Module ui_ingame."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.config.constants import (
    UI_Y_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from codemaster.tools.logger.logger import log


class UIInGame:
    def __init__(self, game):
        self.game = game
        self.game.__class__.ui_ingame = pgui.UIManager(game.size, theme_path=UI_MAIN_THEME_FILE)
        self.manager = self.game.__class__.ui_ingame

        self._add_items()

    def clean_game_data(self):
        self.game = None

    def set_game_data(self, game):
        self.game = game

    def _add_items(self):
        def option_1_action():
            log.info("Option 1")

        def option_2_action():
            log.info("Option 2")

        button_pos_x = 350
        button_pos_y = 275
        button_size = 110, 40
        pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Option 1",
            manager=self.manager,
            command=option_1_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Option 2",
            manager=self.manager,
            command=option_2_action,
            )
