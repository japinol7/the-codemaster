"""Module persistence."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy
import traceback

from codemaster.persistence.persistence_settings import (
    GAME_DATA_HEADER,
    PersistenceSettings,
    )
from codemaster.persistence.exceptions import (
    LoadGameException,
    LoadGameNoSavedGameDataException,
    LoadGameWrongVersionException,
    )
from codemaster.persistence.persistence_pc import (
    load_game_pc_data,
    persist_game_pc_data,
    )
from codemaster.persistence.persistence_items import (
    load_game_items_data,
    persist_game_items_data,
    )
from codemaster.persistence.persistence_npcs import (
    load_game_npcs_data,
    persist_game_npcs_data,
    )
from codemaster.persistence.persistence_utils import save_data_to_file
from codemaster.persistence.working_data import clear_persistence_working_data
from codemaster.tools.logger.logger import log


def persist_game_data(game):
    log.info("Save current game")
    game.__class__.is_load_last_game_failed = False

    persist_game_pc_data(game)
    persist_game_items_data(game)
    persist_game_npcs_data(game)


def clear_all_persisted_data():
    log.info("Clean last saved game")
    settings = PersistenceSettings.settings
    _clear_persisted_data_file(settings['pc_file'], 'player')
    _clear_persisted_data_file(settings['items_file'], 'game_levels')
    _clear_persisted_data_file(settings['items_new_file'], 'game_levels')
    _clear_persisted_data_file(settings['npcs_file'], 'game_levels')
    _clear_persisted_data_file(settings['npcs_new_file'], 'game_levels')

def _clear_persisted_data_file(file_name, key_to_add):
    game_data = deepcopy(GAME_DATA_HEADER)
    game_data['saved_game_data']['continue_game'] = False
    game_data[key_to_add] = {}
    save_data_to_file(file_name, game_data)

def load_game_data(game):
    def set_game_done():
        game.done = True
        game.__class__.is_load_last_game_failed = True
        game.level.clean_entity_ids()

    log.info("Load last saved game")
    log_error_msg = "Error loading last saved game data"
    try:
        load_game_items_data(game)
        load_game_npcs_data(game)
        load_game_pc_data(game)
        clear_persistence_working_data()
    except LoadGameWrongVersionException as e:
        log.warning("%s: %s", log_error_msg, e)
        set_game_done()
        return
    except LoadGameNoSavedGameDataException as e:
        log.warning("%s: %s", log_error_msg, e)
        set_game_done()
        return
    except LoadGameException as e:
        log.warning("%s: %s", log_error_msg, e)
        set_game_done()
        return
    except Exception as e:
        if game.is_debug:
            traceback.print_tb(e.__traceback__)
            log.warning("%s: %s", log_error_msg, e)
        else:
            log.warning("%s", log_error_msg)
        set_game_done()
        return

    game.__class__.is_load_last_game_failed = False
