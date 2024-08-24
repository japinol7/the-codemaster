"""Module persistence_pc."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy

from codemaster.config.constants import DOOR_POSITION_R
from codemaster.models.actors.actors import Actor
from codemaster.models.actors.player import Player
from codemaster.models.actors.items.doors import Door
from codemaster.level_scroll_screen import change_screen_level
from codemaster.persistence.persistence_settings import (
    GAME_DATA_HEADER,
    PersistenceSettings,
    )
from codemaster.persistence.exceptions import (
    LoadGamePcException,
    )
from codemaster.persistence.persistence_utils import (
    load_data_from_file,
    save_data_to_file,
    )
from codemaster.persistence.validations import (
    validate_load_data_game_basic_metadata,
    )
from codemaster.persistence.working_data import get_actors_by_ids_considering_old_ids
from codemaster.tools.logger.logger import log


def persist_game_pc_data(game):
    game.is_debug and log.debug("Save current game PC")

    game_data = deepcopy(GAME_DATA_HEADER)
    pc_data = Player.get_stats_to_persist(game)
    game_data.update(pc_data)
    save_data_to_file(PersistenceSettings.settings['pc_file'], game_data)


def load_game_pc_data(game):
    game.is_debug and log.debug("Load last saved game PC")
    _load_pc_data(game)


def validate_load_data_basic_structure(pc_data):
    if (not pc_data or not isinstance(pc_data.get('saved_game_data'), dict)
            or not isinstance(pc_data.get('player'), dict)):
        raise LoadGamePcException("No game data or invalid format!")


def _load_pc_data(game):
    pc_data = load_data_from_file(PersistenceSettings.settings['pc_file'])

    validate_load_data_basic_structure(pc_data)
    validate_load_data_game_basic_metadata(pc_data)

    pc = game.player
    pc_data = pc_data['player']

    pc.direction = pc_data['direction']
    pc.power = pc_data['power']
    pc.health = pc_data['health']
    pc.stats.update({
        'lives': pc_data['lives'],
        'score': pc_data['score'],
        'level': pc_data['level'] - 1,
        'levels_visited': set(pc_data['levels_visited']),
        'door_previous_position': pc_data['door_previous_position'],
        'door_previous_pos_player': pc_data['door_previous_pos_player'],
        'door_previous_pos_world': pc_data['door_previous_pos_world'],
        'batteries': pc_data['batteries'],
        'files_disks': pc_data['files_disks'],
        'files_disks_type': pc_data['files_disks_type'],
        'bullets_t01': pc_data['bullets_t01'],
        'bullets_t01_shot': pc_data['bullets_t01_shot'],
        'bullets_t02': pc_data['bullets_t02'],
        'bullets_t02_shot': pc_data['bullets_t02_shot'],
        'bullets_t03': pc_data['bullets_t03'],
        'bullets_t03_shot': pc_data['bullets_t03_shot'],
        'bullets_t04': pc_data['bullets_t04'],
        'bullets_t04_shot': pc_data['bullets_t04_shot'],
        'POTION_POWER': pc_data['POTION_POWER'],
        'POTION_HEALTH': pc_data['POTION_HEALTH'],
        'FILES_DISK_D': pc_data['FILES_DISK_D'],
        'FILES_DISK_C': pc_data['FILES_DISK_C'],
        'FILES_DISK_B': pc_data['FILES_DISK_B'],
        'FILES_DISK_A': pc_data['FILES_DISK_A'],
        'apples': pc_data['apples'],
        'apples_type': pc_data['apples_type'],
        'APPLE_GREEN': pc_data['APPLE_GREEN'],
        'APPLE_YELLOW': pc_data['APPLE_YELLOW'],
        'APPLE_RED': pc_data['APPLE_RED'],
        'door_keys': pc_data['door_keys'],
        'door_keys_type': pc_data['door_keys_type'],
        'DOOR_KEY_GREEN': pc_data['DOOR_KEY_GREEN'],
        'DOOR_KEY_BLUE': pc_data['DOOR_KEY_BLUE'],
        'DOOR_KEY_AQUA': pc_data['DOOR_KEY_AQUA'],
        'DOOR_KEY_YELLOW': pc_data['DOOR_KEY_YELLOW'],
        'DOOR_KEY_RED': pc_data['DOOR_KEY_RED'],
        'DOOR_KEY_MAGENTA': pc_data['DOOR_KEY_MAGENTA'],
        'door_keys_stock': get_actors_by_ids_considering_old_ids(pc_data['door_keys_stock']),
        'potions_power': get_actors_by_ids_considering_old_ids(pc_data['potions_power']),
        'potions_health': get_actors_by_ids_considering_old_ids(pc_data['potions_health']),
        'apples_stock': get_actors_by_ids_considering_old_ids(pc_data['apples_stock']),
        })
    pc.sound_effects = game.sound_effects = pc_data['sound_effects']
    game.is_music_paused = pc_data['is_music_paused']

    levels_completed_ids = set(pc_data['levels_completed'])
    levels_completed = [level for level in game.levels if level.id in levels_completed_ids]
    pc.level_up(msg_echo=False)

    for level in levels_completed:
        level.completed = True

    if pc_data['previous_door_crossed']:
        door = Actor.get_actor(pc_data['previous_door_crossed'])
    elif pc_data['game_level'] == 1:
        door = Door.get_doors_dest_to_level_filtered_by_door_type_position(
                pc_data['game_level'] - 1, DOOR_POSITION_R, game
            )[0]
    else:
        door = Door.get_doors_dest_to_level(pc_data['game_level'] - 1, game)[0]
    change_screen_level(game, door=door)
