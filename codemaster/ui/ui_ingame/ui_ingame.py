"""Module ui_ingame."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.config.constants import (
    N_LEVELS,
    UI_X_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from codemaster.ui.ui_main_utils.ui_main_utils import (
    create_text_dialog_msg,
    )


class UIInGame:
    def __init__(self, game):
        self.game = game
        self.game.__class__.ui_ingame = pgui.UIManager(game.size, theme_path=UI_MAIN_THEME_FILE)
        self.manager = self.game.__class__.ui_ingame
        self.items = {}

        self._add_items()

    def clean_game_data(self):
        self.game = None

    def set_game_data(self, game):
        self.game = game

    def _hide_additional_game_items(self):
        if self.items.get('text_message_window'):
            self.items['text_message_window'].hide()

    def _add_items(self):
        def levels_visited_action():
            self._hide_additional_game_items()
            create_text_dialog_msg(
                self,
                f"Levels Visited: {self.game.player.stats['levels_visited']}\n"
                f"Count: {len(self.game.player.stats['levels_visited'])} / {N_LEVELS}"
                )

        def levels_completed_action():
            self._hide_additional_game_items()
            create_text_dialog_msg(
                self,
                f"Levels Completed: {self.game.level.levels_completed_ids(self.game)}\n"
                f"Count: {self.game.level.levels_completed_count(self.game)} / {N_LEVELS}"
                )

        button_pos_x = 200
        button_pos_y = 720
        button_size = 110, 40
        self.items['levels_visited_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="L. Visited",
            manager=self.manager,
            command=levels_visited_action,
            )
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['levels_completed_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="L. Completed",
            manager=self.manager,
            command=levels_completed_action,
            )
