"""Module persistence."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy
import json
import traceback

from codemaster.config.constants import (
    GAME_DATA_HEADER,
    JSON_INDENT_SIZE,
    PERSISTENCE_PC_FILE,
    PERSISTENCE_ITEMS_FILE,
    PERSISTENCE_ITEMS_NEW_FILE,
    PERSISTENCE_NPCS_FILE,
    PERSISTENCE_NPCS_NEW_FILE,
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
    _clear_persisted_data_file(PERSISTENCE_PC_FILE, 'player')
    _clear_persisted_data_file(PERSISTENCE_ITEMS_FILE, 'game_levels')
    _clear_persisted_data_file(PERSISTENCE_ITEMS_NEW_FILE, 'game_levels')
    _clear_persisted_data_file(PERSISTENCE_NPCS_FILE, 'game_levels')
    _clear_persisted_data_file(PERSISTENCE_NPCS_NEW_FILE, 'game_levels')

def _clear_persisted_data_file(file_name, key_to_add):
    game_data = deepcopy(GAME_DATA_HEADER)
    game_data['saved_game_data']['continue_game'] = False
    game_data[key_to_add] = {}
    data_json = json.dumps(game_data, indent=JSON_INDENT_SIZE)
    with open(file_name, 'w') as file_out:
        file_out.write(data_json)

def load_game_data(game):
    def game_done():
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
        game_done()
        return
    except LoadGameNoSavedGameDataException as e:
        log.warning("%s: %s", log_error_msg, e)
        game_done()
        return
    except LoadGameException as e:
        log.warning("%s: %s", log_error_msg, e)
        game_done()
        return
    except Exception as e:
        if game.is_debug:
            traceback.print_tb(e.__traceback__)
            log.warning("%s: %s", log_error_msg, e)
        else:
            log.warning("%s", log_error_msg)
        game_done()
        return

    game.__class__.is_load_last_game_failed = False
