"""Module persistence_npcs."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy

from codemaster.config.constants import (
    GAME_DATA_HEADER,
    PERSISTENCE_NPCS_FILE,
    PERSISTENCE_NPCS_NEW_FILE,
    PERSISTENCE_NO_SAVED_GAME_DATA_MSG,
    )
from codemaster.models.actors.actors import NPC, Actor
from codemaster.models.actors import npcs as npcs_module
from codemaster.persistence.exceptions import (
    LoadGameNPCsException,
    LoadGameNoSavedGameDataException,
    )
from codemaster.persistence.persistence_utils import (
    load_data_from_file,
    save_data_to_file,
    )
from codemaster.persistence.validations import (
    validate_load_data_game_basic_metadata,
    )
from codemaster.tools.logger.logger import log


def persist_game_npcs_data(game):
    _persist_npcs_data(game)
    _persist_npcs_not_initial_data(game)


def load_game_npcs_data(game):
    _load_npcs_data(game)
    _load_npcs_not_initial_data(game)


def _persist_npcs_data(game):
    game.is_debug and log.debug("Save current game NPCs")
    game_data = deepcopy(GAME_DATA_HEADER)
    npcs_data = NPC.get_npcs_stats_to_persist(game)
    game_data.update(npcs_data)
    save_data_to_file(PERSISTENCE_NPCS_FILE, game_data)


def _persist_npcs_not_initial_data(game):
    game.is_debug and log.debug("Save current game NPCs: Not initial actors")
    game_data = deepcopy(GAME_DATA_HEADER)
    npcs_data = NPC.get_npcs_not_initial_actor_stats_to_persist(game)
    game_data.update(npcs_data)
    save_data_to_file(PERSISTENCE_NPCS_NEW_FILE, game_data)


def validate_load_data_basic_structure(npcs_data):
    if (not npcs_data or not isinstance(npcs_data.get('saved_game_data'), dict)
            or not isinstance(npcs_data.get('game_levels'), dict)):
        raise LoadGameNPCsException("No game data or invalid format!")


def _load_npcs_data(game):
    game.is_debug and log.debug("Load last saved game NPCs")
    npcs_data = load_data_from_file(PERSISTENCE_NPCS_FILE)

    validate_load_data_basic_structure(npcs_data)
    validate_load_data_game_basic_metadata(npcs_data)

    if npcs_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for game_level in game.levels:
        level_data = npcs_data['game_levels'].get(f"{game_level.id}")
        if not level_data or not isinstance(level_data['npcs'], dict):
            continue
        npcs_level = level_data['npcs']
        scroll_shift, scroll_shift_top = game_level.get_scroll_shift_delta_tuple(game_level, level_data)
        for npc in game_level.npcs:
            npc_data = npcs_level.get(npc.id)
            if not npc_data:
                npc.kill()
                continue
            npc.health = npc_data['health']

            if npc.is_a_dragon or npc.is_a_snake:
                continue
            npc.stats.health_total = npc_data['health_total']
            npc.rect.x = npc_data['x'] + scroll_shift
            npc.rect.y = npc_data['y'] - scroll_shift_top
            npc.change_x = npc_data['change_x']
            npc.change_y = npc_data['change_y']
            npc.direction = npc_data['direction']
            npc.hostility_level = npc_data['hostility_level']


def _load_npcs_not_initial_data(game):
    game.is_debug and log.debug("Load last saved game NPCs: Not initial actors")
    npcs_data = load_data_from_file(PERSISTENCE_NPCS_NEW_FILE)

    validate_load_data_basic_structure(npcs_data)
    validate_load_data_game_basic_metadata(npcs_data)

    if npcs_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for level_id, level_data in npcs_data['game_levels'].items():
        level = game.levels[int(level_id) - 1]
        scroll_shift, scroll_shift_top = level.get_scroll_shift_delta_tuple(level, level_data)
        npcs = []
        for npc_id, npc_data in level_data['npcs'].items():
            kwargs_ = {
                'change_x': npc_data['change_x'],
                'change_y': npc_data['change_y'],
                'border_left': npc_data['border_left'] if npc_data['border_left'] else 0,
                'border_right': npc_data['border_right'] if npc_data['border_right'] else 0,
                'border_top': npc_data['border_top'] if npc_data['border_top'] else 0,
                'border_down': npc_data['border_down'] if npc_data['border_down'] else 0,
                }
            npc = Actor.factory(
                npcs_module,
                npc_data['type_name'],
                x=npc_data['x'] + scroll_shift,
                y=npc_data['y'] - scroll_shift_top,
                game=game,
                kwargs=kwargs_,
                )
            npc.health = npc_data['health']
            npc.stats.health_total = npc_data['health_total']
            npc.direction = npc_data['direction']
            npcs.append(npc)
        level.add_actors(npcs)
