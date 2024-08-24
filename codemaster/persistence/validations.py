"""Module validations."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import (
    APP_NAME_LONG,
    APP_TECH_NAME,
    )
from codemaster.persistence.persistence_settings import (
    PERSISTENCE_NO_SAVED_GAME_DATA_MSG,
    )
from codemaster.persistence.exceptions import (
    LoadGameNoSavedGameDataException,
    LoadGameWrongVersionException,
    )
from codemaster.version import version


def validate_load_data_game_basic_metadata(game_data):
    if game_data['saved_game_data'].get('app_name') != APP_NAME_LONG:
        raise LoadGameWrongVersionException(
            "Wrong general game metadata. "
            f"\n   Expected:     {APP_NAME_LONG} "
            f"\n   but received: {game_data['saved_game_data'].get('app_name')}")

    if game_data['saved_game_data'].get('app_tech_name') != APP_TECH_NAME:
        raise LoadGameWrongVersionException(
            "Wrong general game metadata. "
            f"Expected: {APP_TECH_NAME} "
            f"but received: {game_data['saved_game_data'].get('app_tech_name')}")

    if game_data['saved_game_data'].get('app_version') != version.get_version():
        raise LoadGameWrongVersionException(
            "You cannot load a game from another version! "
            f"Expected: {version.get_version()} "
            f"but received: {game_data['saved_game_data'].get('app_version')}")

    if not game_data['saved_game_data'].get('continue_game'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)
