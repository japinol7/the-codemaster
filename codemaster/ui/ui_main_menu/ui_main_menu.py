"""Module ui_main_menu."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.config.constants import (
    UI_Y_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from codemaster.config.settings import Settings
from codemaster.tools.logger.logger import log


class UIMainMenu:
    def __init__(self, game):
        self.game = game
        self.game.__class__.ui_main_menu = pgui.UIManager(game.size, theme_path=UI_MAIN_THEME_FILE)
        self.manager = self.game.__class__.ui_main_menu
        self.items = {}

        self._add_items()

    def clean_game_data(self):
        self.game = None

    def set_game_data(self, game):
        self.game = game

    def _add_items(self):
        def new_game_action():
            self.game.__class__.new_game = True

        def continue_game_action():
            self.game.is_load_last_game = True

        def load_game_action():
            log.info("Load Game")

        def save_game_action():
            log.info("Save Game")

        def show_credits_action():
            log.info("Show Credits")

        def quit_game_action():
            self.game.set_is_exit_game(True)

        button_pos_x = 100
        button_pos_y = 470
        button_size = 170, 40

        self.items['new_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="New Game",
            manager=self.manager,
            command=new_game_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['continue_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Continue Last Game",
            manager=self.manager,
            command=continue_game_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['load_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Load Game",
            manager=self.manager,
            command=load_game_action,
            )

        button_pos_x = Settings.screen_width - 270
        button_pos_y = 470
        button_size = 170, 40

        self.items['save_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Save Game",
            manager=self.manager,
            command=save_game_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['show_credits_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Credits",
            manager=self.manager,
            command=show_credits_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['quit_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Quit Game",
            manager=self.manager,
            command=quit_game_action,
            )

        if not self.game.is_persist_data:
            self.items['continue_game_button'].disable()
            self.items['load_game_button'].disable()
            self.items['save_game_button'].disable()
