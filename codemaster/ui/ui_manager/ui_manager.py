"""Module ui_manager."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.ui.ui_ingame.ui_ingame import UIInGame
from codemaster.ui.ui_main_menu.ui_main_menu import UIMainMenu


class UIManager:
    def __init__(self, game):
        self.name = "UI In Game"
        self.ui_ingame = UIInGame(game)
        self.ui_main_menu = UIMainMenu(game)

    def clean_game_data(self):
        self.ui_ingame.clean_game_data()
        self.ui_main_menu.clean_game_data()

    def set_game_data(self, game):
        self.ui_ingame.set_game_data(game)
        self.ui_main_menu.set_game_data(game)
