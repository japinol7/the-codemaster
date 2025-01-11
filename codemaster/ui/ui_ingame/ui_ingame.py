"""Module ui_ingame."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.config.constants import (
    ALLOWED_CHARS_ALPHANUM_SPACE,
    N_LEVELS,
    UI_X_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from codemaster.models.actors.items.files_disks import FilesDisk
from codemaster.ui.ui_main_utils.ui_main_utils import (
    clean_general_ui_items,
    create_text_dialog_msg,
    save_game_ui_action,
    save_game_directory_ui_action,
    )
from codemaster.cutscene_manager.cutscene_manager import start_cutscene


class UIInGame:
    def __init__(self, game):
        self.game = game
        self.manager = pgui.UIManager(game.size, theme_path=UI_MAIN_THEME_FILE)
        self.items = {}

        self._add_items()

    def clean_game_data(self):
        self.game = None

    def set_game_data(self, game):
        self.game = game

    def clean_ui_items(self):
        clean_general_ui_items(self)

    def hide_additional_game_items(self):
        self.items['potion_selection_list'].hide()
        self.items['potion_drink_text_box'].hide()
        self.items['health_potion_drink_button'].hide()
        self.items['power_potion_drink_button'].hide()

        self.items['files_disks_selection_list'].hide()
        self.items['files_disk_text_box'].hide()
        self.items['files_disks_read_button'].hide()

        self.items['cutscene_selection_list'].hide()
        self.items['cutscene_sel_text_box'].hide()
        self.items['cutscene_watch_button'].hide()

        if self.items.get('text_message_window'):
            self.items['text_message_window'].hide()

        self.items['save_game_ok_button'].hide()
        self.items['text_entry_line'].hide()

    def _add_items(self):
        def levels_visited_action():
            self.hide_additional_game_items()
            create_text_dialog_msg(
                self,
                "Levels Visited: "
                f"{', '.join(self.game.player.levels_visited_names())}\n"
                "Count: "
                f"{len(self.game.player.stats['levels_visited'])} / {N_LEVELS}"
                )

        def levels_completed_action():
            self.hide_additional_game_items()
            create_text_dialog_msg(
                self,
                "Levels Completed:"
                f" {', '.join(self.game.level.levels_completed_names(self.game))}\n"
                "Count: "
                f"{self.game.level.levels_completed_count(self.game)} / {N_LEVELS}"
                )

        def health_potions_action():
            self.hide_additional_game_items()
            potions = self.game.player.get_health_potion_powers_sorted_str()
            self.items['potion_selection_list'].set_item_list(potions)
            self.items['potion_selection_list'].show()
            text = f"PC Health: {self.game.player.get_health_rounded()}".center(30)
            self.items['potion_drink_text_box'].set_text(text)

            if (not potions
                    or self.game.player.get_health_rounded()
                    >= self.game.player.health_total):
                self.items['potion_selection_list'].disable()
                self.items['health_potion_drink_button'].disable()
            else:
                self.items['potion_selection_list'].enable()
                self.items['health_potion_drink_button'].enable()

            self.items['potion_drink_text_box'].show()
            self.items['health_potion_drink_button'].show()

        def power_potions_action():
            self.hide_additional_game_items()
            potions = self.game.player.get_power_potion_powers_sorted_str()
            self.items['potion_selection_list'].set_item_list(potions)
            self.items['potion_selection_list'].show()
            text = f"PC Power: {self.game.player.get_power_rounded()}".center(30)
            self.items['potion_drink_text_box'].set_text(text)

            if (not potions
                    or self.game.player.get_power_rounded() >= self.game.player.power_total):
                self.items['potion_selection_list'].disable()
                self.items['power_potion_drink_button'].disable()
            else:
                self.items['potion_selection_list'].enable()
                self.items['power_potion_drink_button'].enable()

            self.items['potion_drink_text_box'].show()
            self.items['power_potion_drink_button'].show()

        def health_potion_drink_action():
            self.hide_additional_game_items()
            potion_power = self.items['potion_selection_list'].get_single_selection()
            if not potion_power:
                health_potions_action()
                return

            potion = self.game.player.get_health_potion_by_power(int(potion_power))
            if potion:
                self.game.player.drink_health_potion(potion)
            health_potions_action()

        def power_potion_drink_action():
            self.hide_additional_game_items()
            potion_power = self.items['potion_selection_list'].get_single_selection()
            if not potion_power:
                power_potions_action()
                return

            potion = self.game.player.get_power_potion_by_power(int(potion_power))
            if potion:
                self.game.player.drink_power_potion(potion)
            power_potions_action()

        def files_disks_action():
            self.hide_additional_game_items()
            files_disks = self.game.player.get_files_disks_with_status_str()
            self.items['files_disks_selection_list'].set_item_list(files_disks)
            self.items['files_disks_selection_list'].show()
            self.items['files_disk_text_box'].set_text("Files Disks".center(34))

            if not files_disks:
                self.items['files_disks_selection_list'].disable()
                self.items['files_disks_read_button'].disable()
            else:
                self.items['files_disks_selection_list'].enable()
                self.items['files_disks_read_button'].enable()

            self.items['files_disk_text_box'].show()
            self.items['files_disks_read_button'].show()

        def files_disks_read_action():
            self.hide_additional_game_items()
            files_disk_msg_sel = self.items[
                'files_disks_selection_list'].get_single_selection()
            if not files_disk_msg_sel:
                files_disks_action()
                return

            files_disk_msg_id = files_disk_msg_sel[8:]
            files_disk_msg = FilesDisk.read_msg(files_disk_msg_id, self.game)
            files_disks_action()
            create_text_dialog_msg(
                self,
                f"{files_disk_msg}\nEOF",
                rect=pg.Rect((309, 98), (542, 330)),
                title=f"File: {files_disk_msg_id}"
                )

        def cutscenes_action():
            self.hide_additional_game_items()
            cutscenes = [x.cutscene.name_short for x in self.game.cutscene_levels]
            self.items['cutscene_selection_list'].set_item_list(cutscenes)
            self.items['cutscene_selection_list'].show()
            text = "Cutscenes you can watch"
            self.items['cutscene_sel_text_box'].set_text(text)

            if not cutscenes:
                self.items['cutscene_selection_list'].disable()
                self.items['cutscene_watch_button'].disable()
            else:
                self.items['cutscene_selection_list'].enable()
                self.items['cutscene_watch_button'].enable()

            self.items['cutscene_sel_text_box'].show()
            self.items['cutscene_watch_button'].show()

        def cutscene_watch_action():
            self.hide_additional_game_items()
            cutscene_name = self.items['cutscene_selection_list'].get_single_selection()
            if not cutscene_name:
                cutscenes_action()
                return

            cutscene_id = [i for i, x in enumerate(self.game.cutscene_levels)
                           if x.cutscene.name_short == cutscene_name]

            if not cutscene_id:
                cutscenes_action()
                return

            self.game.screen_pause.done = True
            start_cutscene(cutscene_id[0], self.game)
            cutscenes_action()

        def save_game_action():
            save_game_ui_action(self)

        def save_game_directory_action():
            save_game_directory_ui_action(self, persist_game_before_copy=True)

        button_pos_x = 177
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
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['health_potions_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Health Potions",
            manager=self.manager,
            command=health_potions_action,
            )
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['power_potions_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Power Potions",
            manager=self.manager,
            command=power_potions_action,
            )
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['files_disks_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Info Files",
            manager=self.manager,
            command=files_disks_action,
            )
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['watch_cutscene'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Cutscenes",
            manager=self.manager,
            command=cutscenes_action,
            )
        button_pos_x += UI_X_SPACE_BETWEEN_BUTTONS
        self.items['save_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Save Game",
            manager=self.manager,
            command=save_game_action,
            )

        if not self.game.is_persist_data:
            self.items['save_game_button'].disable()

        self.items['text_entry_line'] = (pgui.elements.ui_text_entry_line.
                UITextEntryLine(
            relative_rect=pg.Rect((385, 480), (390, 42)),
            manager=self.manager,
            visible=False,
            ))
        self.items['text_entry_line'].set_allowed_characters(
            ALLOWED_CHARS_ALPHANUM_SPACE)

        self.items['potion_selection_list'] = (pgui.elements.ui_selection_list.
                UISelectionList(
            relative_rect=pg.Rect((355, 430), (220, 275)),
            manager=self.manager,
            item_list = [],
            visible=False,
            ))

        self.items['potion_drink_text_box'] = pgui.elements.UITextBox(
            relative_rect=pg.Rect((578, 470), (190, 40)),
            html_text="Current value:",
            manager=self.manager,
            plain_text_display_only=True,
            visible=False,
            )

        self.items['health_potion_drink_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((578, 514), (190, 40)),
            text="Drink Health Potion",
            manager=self.manager,
            command=health_potion_drink_action,
            visible=False,
            )
        self.items['power_potion_drink_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((578, 514), (190, 40)),
            text="Drink Power Potion",
            manager=self.manager,
            command=power_potion_drink_action,
            visible=False,
            )

        self.items['files_disks_selection_list'] = (pgui.elements.ui_selection_list.
                UISelectionList(
            relative_rect=pg.Rect((360, 430), (215, 275)),
            manager=self.manager,
            item_list = [],
            visible=False,
            ))
        self.items['files_disk_text_box'] = pgui.elements.UITextBox(
            relative_rect=pg.Rect((578, 470), (190, 40)),
            html_text="Current value:",
            manager=self.manager,
            plain_text_display_only=True,
            visible=False,
            )
        self.items['files_disks_read_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((578, 514), (190, 40)),
            text="Read Files",
            manager=self.manager,
            command=files_disks_read_action,
            visible=False,
            )

        self.items['cutscene_selection_list'] = (pgui.elements.ui_selection_list.
                UISelectionList(
            relative_rect=pg.Rect((355, 430), (220, 275)),
            manager=self.manager,
            item_list = [],
            visible=False,
            ))

        self.items['cutscene_sel_text_box'] = pgui.elements.UITextBox(
            relative_rect=pg.Rect((578, 470), (190, 40)),
            html_text="Current value:",
            manager=self.manager,
            plain_text_display_only=True,
            visible=False,
            )

        self.items['cutscene_watch_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((578, 514), (190, 40)),
            text="Watch Cutscene",
            manager=self.manager,
            command=cutscene_watch_action,
            visible=False,
            )

        self.items['save_game_ok_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((495, 524), (170, 40)),
            text="Save Named Game",
            manager=self.manager,
            command=save_game_directory_action,
            visible=False,
            )
