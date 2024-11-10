"""Module persistence_utils."""
__author__ = 'Joan A. Pinol  (japinol)'

import json
import os
import shutil

from codemaster.config.constants import JSON_INDENT_SIZE
from codemaster.persistence.persistence_settings import (
    PERSISTENCE_BASE_PATH_DEFAULT,
    PERSISTENCE_AUTO_SAVED_GAME_NAME,
    PersistenceSettings,
    )
from codemaster.tools.logger.logger import log


def load_data_from_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file_in:
            data_json = json.load(file_in)
    except Exception as e:
        return {}

    return data_json


def save_data_to_file(file_name, data):
    data_json = json.dumps(data, indent=JSON_INDENT_SIZE)
    with open(file_name, 'w', encoding='utf-8') as file_out:
        file_out.write(data_json)


def is_json_serializable(obj):
    try:
        json.dumps(obj)
    except (TypeError, OverflowError):
        return False
    return True


def get_persistence_path(path):
    return os.path.join(PERSISTENCE_BASE_PATH_DEFAULT, path)


def get_persistence_directories():
    sub_dirs = []
    try:
        sub_dirs = [f.name for f in os.scandir(PERSISTENCE_BASE_PATH_DEFAULT)
                    if f.is_dir() and f.name.lower() != PERSISTENCE_AUTO_SAVED_GAME_NAME]
    except Exception as e:
        log.warning(f"ERROR: Cannot access directory: {e}")
    finally:
        return sub_dirs


def get_persistence_can_continue_game():
    data = load_data_from_file(PersistenceSettings.settings['can_continue_game_file'])

    # Validate data basic structure
    if (not data or not isinstance(data.get('saved_game_data'), dict)
            or not isinstance(data.get('can_continue_game'), dict)):
        return False

    # Validate continue game value
    if not data['saved_game_data'].get('continue_game', False):
        return False

    return True


def copy_persistence_saved_game(path_src, path_dest):
    shutil.copytree(path_src, path_dest)


def delete_persistence_saved_game(path):
    shutil.rmtree(path)
