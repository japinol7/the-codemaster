"""Module ui_ingame."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame_gui as pgui

from codemaster.config.constants import (
    UI_MAIN_THEME_FILE,
    )


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
        pass
