"""Module ui_main_utils."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from codemaster.persistence import persistence
from codemaster.persistence.persistence_settings import PERSISTENCE_AUTO_SAVED_GAME_NAME
from codemaster.persistence.persistence_utils import (
    get_persistence_can_continue_game,
    get_persistence_directories,
    get_persistence_path,
    copy_persistence_saved_game,
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


def create_text_dialog_msg(obj, text, title="Message", rect=None, visible=True):
    obj.items['text_message_window'] = pgui.windows.ui_message_window.UIMessageWindow(
        rect=rect or pg.Rect((406, 450), (350, 194)),
        manager=obj.manager,
        html_message=text,
        window_title=title,
        object_id=pgui.core.ObjectID(class_id='@dialog_msgs', object_id='#text_msg'),
        visible=visible,
        )


def create_error_dialog_msg(obj, text, rect=None, visible=True):
    obj.items['error_message_window'] = pgui.windows.ui_message_window.UIMessageWindow(
        rect=rect or pg.Rect((406, 450), (350, 194)),
        manager=obj.manager,
        html_message=text,
        window_title="ERROR",
        object_id=pgui.core.ObjectID(class_id='@dialog_msgs', object_id='#error_msg'),
        visible=visible,
        )


def create_confirmation_dialog_msg(obj, text, title, action_short_text, items_key, visible=True):
    obj.items[items_key] = pgui.windows.ui_confirmation_dialog.UIConfirmationDialog(
        rect=pg.Rect((406, 450), (350, 205)),
        manager=obj.manager,
        action_long_desc=text,
        window_title=title,
        action_short_name=action_short_text,
        blocking=True,
        visible=visible,
        )


def save_game_ui_action(ui_manager):
    ui_manager.hide_additional_game_items()
    ui_manager.items['save_game_ok_button'].show()
    ui_manager.items['text_entry_line'].show()


def save_game_directory_ui_action(ui_manager, persist_game_before_copy=False):
    ui_manager.hide_additional_game_items()
    dir_dest_name = ui_manager.items['text_entry_line'].get_text().strip()
    log.info(f"Save Game name: {dir_dest_name}")
    try:
        if not persist_game_before_copy and not get_persistence_can_continue_game():
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

        if persist_game_before_copy:
            persistence.persist_game_data(ui_manager.game)

        copy_persistence_saved_game(
            get_persistence_path('save_data'), get_persistence_path(dir_dest_name))
    except CannotSaveEmptyGameException as e:
        log.warning(f"ERROR: Cannot save current game: {e}")
        create_error_dialog_msg(ui_manager, f"Error Saving Game: {e}")
    except InvalidDirectoryNameException as e:
        log.warning(f"ERROR: Cannot save current game: {e}")
        create_error_dialog_msg(ui_manager, f"Error Saving Game: {e}")
    except SaveNameMustBeDiffToAutoSavedGameException as e:
        log.warning(f"ERROR: Cannot save current game: {e}")
        create_error_dialog_msg(ui_manager, f"Error Saving Game: {e}")
    except Exception as e:
        log.warning(f"ERROR: Cannot save current game: {e}")
        create_error_dialog_msg(
            ui_manager, f"Error Saving Game with name: {dir_dest_name or ''}")
