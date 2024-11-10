"""Module persistence_settings."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

from codemaster.config.constants import (
    APP_NAME_LONG,
    APP_TECH_NAME,
    )
from codemaster.tools.logger.logger import log
from codemaster.version import version

PERSISTENCE_AUTO_SAVED_GAME_NAME = 'save_data'
PERSISTENCE_BASE_PATH_DEFAULT = os.path.join('save_data')
PERSISTENCE_PATH_DEFAULT = os.path.join('save_data', PERSISTENCE_AUTO_SAVED_GAME_NAME)
PERSISTENCE_NO_SAVED_GAME_DATA_MSG = "No saved data to load. " \
                                     "Maybe last game ended with a Game Over or a Win?"
GAME_DATA_HEADER = {
    'saved_game_data': {
        'app_name': APP_NAME_LONG,
        'app_tech_name': APP_TECH_NAME,
        'app_version': version.get_version(),
        "continue_game": True,
        },
    }


class PersistenceSettings:
    settings = {}

    @classmethod
    def init_settings(cls, persistence_path):
        log.debug(f"{persistence_path=}")
        cls.settings.update({
            'pc_file': os.path.join(persistence_path, "player.json"),
            'items_file': os.path.join(persistence_path, "items.json"),
            'items_new_file': os.path.join(persistence_path, "items_not_initial.json"),
            'npcs_file': os.path.join(persistence_path, "npcs.json"),
            'npcs_new_file': os.path.join(persistence_path, "npcs_not_initial.json"),
            'can_continue_game_file': os.path.join(persistence_path, "can_continue_game.json"),
            })
