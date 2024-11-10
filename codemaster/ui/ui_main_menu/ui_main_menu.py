"""Module ui_main_menu."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.version import version
from codemaster.config.constants import (
    APP_WEBSITE_URL,
    UI_Y_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from codemaster.config.settings import Settings
from codemaster.persistence.persistence_settings import PERSISTENCE_AUTO_SAVED_GAME_NAME
from codemaster.persistence.persistence_utils import (
    get_persistence_can_continue_game,
    get_persistence_directories,
    get_persistence_path,
    copy_persistence_saved_game,
    delete_persistence_saved_game,
    )
from codemaster.tools.logger.logger import log


class InvalidDirectoryNameException(Exception):
    pass


class CannotDeleteAutoSavedGameException(Exception):
    pass


class CannotSaveEmptyGameException(Exception):
    pass


class SaveNameMustBeDiffToAutoSavedGameException(Exception):
    pass


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

    def _create_credits_dialog_msg(self):
        self.items['credits_message_window'] = pgui.windows.ui_message_window.UIMessageWindow(
            rect=pg.Rect((310, 298), (542, 330)),
            manager=self.manager,
            html_message=
            "<p>The CodeMaster is a spin-off sci-fi mystery based on the 1988 RPG "
            "platformer game Pac's Revenge series games by @japinol.</p>\n"
            "<p>Code & Pixel art graphics (c) Joan A Pinol 1987, 1988, 2015, 2021, 2024.</p>"
            f'''<p>Website: <a href="{APP_WEBSITE_URL}">{APP_WEBSITE_URL}</a> </p>'''
            f"<p>Version: {version.get_version()}</p>\n"
            "<p>Thanks for trying this demo! </p\n"
            "<p>Have a wonderful day! </p\n"
            "<p>: ) </p\n",
            window_title="Credits",
            visible=True,
            )

    def _create_error_dialog_msg(self, text):
        self.items['error_message_window'] = pgui.windows.ui_message_window.UIMessageWindow(
            rect=pg.Rect((406, 450), (350, 165)),
            manager=self.manager,
            html_message=text,
            window_title="ERROR",
            object_id=pgui.core.ObjectID(class_id='@dialog_msgs', object_id='#error_msg'),
            visible=True,
            )

    def _create_confirmation_dialog_msg(self, text, title, action_short_text, items_key):
        self.items[items_key] = pgui.windows.ui_confirmation_dialog.UIConfirmationDialog(
            rect=pg.Rect((406, 450), (350, 205)),
            manager=self.manager,
            action_long_desc=text,
            window_title=title,
            action_short_name=action_short_text,
            blocking=True,
            visible=True,
            )

    def _hide_additional_game_items(self):
        self.items['load_game_selection_list'].hide()
        self.items['load_game_ok_button'].hide()
        self.items['delete_game_button'].hide()
        self.items['save_game_ok_button'].hide()
        self.items['text_entry_line'].hide()
        if self.items.get('credits_message_window'):
            self.items['credits_message_window'].hide()
        if self.items.get('error_message_window'):
            self.items['error_message_window'].hide()

    def _show_load_game_selection_items(self):
        self.items['load_game_selection_list'].set_item_list(get_persistence_directories())
        self.items['load_game_selection_list'].show()
        self.items['load_game_ok_button'].show()
        self.items['delete_game_button'].show()

    def delete_game_directory_action(self):
        dir_name = self.items['load_game_selection_list'].get_single_selection()
        log.info(f"Delete Saved Game: {dir_name or ''}")
        self._hide_additional_game_items()
        try:
            if dir_name.lower() == PERSISTENCE_AUTO_SAVED_GAME_NAME:
                raise CannotDeleteAutoSavedGameException(
                    "You are not allowed to delete the auto saved game data directory: "
                    f"{PERSISTENCE_AUTO_SAVED_GAME_NAME or ''}")

            delete_persistence_saved_game(get_persistence_path(dir_name))
        except CannotDeleteAutoSavedGameException as e:
            log.warning(f"ERROR: Cannot delete saved game: {e}")
            self._hide_additional_game_items()
            self._create_error_dialog_msg(
                f"Error: You are not allowed to delete the "
                f"auto saved game data: {dir_name or ''}")
            return
        except Exception as e:
            log.warning(f"ERROR: Cannot delete saved game: {e}")
            self._hide_additional_game_items()
            self._create_error_dialog_msg(
                f"Error deleting saved game with name: {dir_name or ''}")
            return
        self._show_load_game_selection_items()

    def _add_items(self):
        def new_game_action():
            self._hide_additional_game_items()
            self.game.__class__.new_game = True

        def continue_game_action():
            self._hide_additional_game_items()
            self.game.is_continue_game = True

        def load_game_action():
            self._hide_additional_game_items()
            load_game_sel_list = self.items['load_game_selection_list']
            load_game_sel_list.set_item_list(get_persistence_directories())
            load_game_sel_list.show()
            self.items['load_game_ok_button'].show()
            self.items['delete_game_button'].show()

        def load_game_directory_action():
            dir_name = self.items['load_game_selection_list'].get_single_selection()
            log.info(f"Load Saved Game: {dir_name or ''}")
            self._hide_additional_game_items()
            try:
                self.game.persistence_path_from_user = get_persistence_path(dir_name)
                self.game.is_continue_game = True
                self.game.is_load_user_game = True
            except Exception as e:
                log.warning(f"ERROR: Cannot load saved game: {e}")
                self._hide_additional_game_items()
                self._create_error_dialog_msg(
                    f"Error loading saved game with name: {dir_name or ''}")

        def delete_game_directory_confirmation():
            dir_name = self.items['load_game_selection_list'].get_single_selection()
            self._hide_additional_game_items()

            if not dir_name:
                self._create_error_dialog_msg(
                    f"Error: You must choose a saved game to delete.")
                self._show_load_game_selection_items()
                return

            self._create_confirmation_dialog_msg(
                f"Delete saved game with name: {dir_name or ''}",
                title="Delete saved game",
                action_short_text="Delete",
                items_key='delete_saved_game_confirm_dialog')

        def save_game_action():
            self._hide_additional_game_items()
            self.items['save_game_ok_button'].show()
            self.items['text_entry_line'].show()

        def save_game_directory_action():
            self._hide_additional_game_items()
            dir_dest_name = self.items['text_entry_line'].get_text().strip()
            log.info(f"Save Game name: {dir_dest_name}")
            try:
                if not get_persistence_can_continue_game():
                    raise CannotSaveEmptyGameException("Cannot save an empty game.")
                if len(dir_dest_name) < 3:
                    raise InvalidDirectoryNameException(
                        f"Your game name must have at least 3 chars. "
                        f"Name: {dir_dest_name or ''}")
                if len(dir_dest_name) > 30:
                    raise InvalidDirectoryNameException(
                        f"Your game name must have a maximum of 30 chars. "
                        f"Name: {dir_dest_name or ''}")
                if dir_dest_name.lower() == PERSISTENCE_AUTO_SAVED_GAME_NAME:
                    raise SaveNameMustBeDiffToAutoSavedGameException(
                        "You cannot use this name. It is reserved for the system: "
                        f"{PERSISTENCE_AUTO_SAVED_GAME_NAME or ''}")
                if dir_dest_name in get_persistence_directories():
                    raise InvalidDirectoryNameException(
                        f"There is already one saved game with this "
                        f"name: {dir_dest_name or ''}")

                copy_persistence_saved_game(
                    get_persistence_path('save_data'), get_persistence_path(dir_dest_name))
            except CannotSaveEmptyGameException as e:
                log.warning(f"ERROR: Cannot save current game: {e}")
                self._create_error_dialog_msg(f"Error Saving Game: {e}")
            except InvalidDirectoryNameException as e:
                log.warning(f"ERROR: Cannot save current game: {e}")
                self._create_error_dialog_msg(f"Error Saving Game: {e}")
            except SaveNameMustBeDiffToAutoSavedGameException as e:
                log.warning(f"ERROR: Cannot save current game: {e}")
                self._create_error_dialog_msg(f"Error Saving Game: {e}")
            except Exception as e:
                log.warning(f"ERROR: Cannot save current game: {e}")
                self._create_error_dialog_msg(
                    f"Error Saving Game with name: {dir_dest_name or ''}")

        def show_credits_action():
            log.debug("Show Credits")
            self._hide_additional_game_items()
            self._create_credits_dialog_msg()

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

        self.items['text_entry_line'] = pgui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pg.Rect((375, 480), (390, 42)),
            manager=self.manager,
            visible=False,
            )
        self.items['text_entry_line'].set_allowed_characters(
            self.game.allowed_chars_alphanum_space)

        self.items['load_game_selection_list'] = pgui.elements.ui_selection_list.UISelectionList(
            relative_rect=pg.Rect((290, 395), (285, 300)),
            manager=self.manager,
            item_list = [],
            visible=False,
            )
        self.items['load_game_ok_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((578, 470), button_size),
            text="Load Selected Game",
            manager=self.manager,
            command=load_game_directory_action,
            visible=False,
            )
        self.items['delete_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((578, 512), button_size),
            text="Delete Selected Game",
            manager=self.manager,
            command=delete_game_directory_confirmation,
            visible=False,
            )
        self.items['save_game_ok_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((485, 524), button_size),
            text="Save Named Game",
            manager=self.manager,
            command=save_game_directory_action,
            visible=False,
            )
