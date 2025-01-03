"""Module persistence_npcs."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy

from codemaster.models.actors.actors import NPC, Actor, DropItem
from codemaster.models.actors import npcs as npcs_module
from codemaster.models.actors import items as items_module
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.persistence.persistence_settings import (
    GAME_DATA_HEADER,
    PERSISTENCE_NO_SAVED_GAME_DATA_MSG,
    PersistenceSettings,
    )
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
    save_data_to_file(PersistenceSettings.settings['npcs_file'], game_data)


def _persist_npcs_not_initial_data(game):
    game.is_debug and log.debug("Save current game NPCs: Not initial actors")
    game_data = deepcopy(GAME_DATA_HEADER)
    npcs_data = NPC.get_npcs_not_initial_actor_stats_to_persist(game)
    game_data.update(npcs_data)
    save_data_to_file(PersistenceSettings.settings['npcs_new_file'], game_data)


def validate_load_data_basic_structure(npcs_data):
    if (not npcs_data or not isinstance(npcs_data.get('saved_game_data'), dict)
            or not isinstance(npcs_data.get('game_levels'), dict)):
        raise LoadGameNPCsException("No game data or invalid format!")


def _load_npcs_data(game):
    game.is_debug and log.debug("Load last saved game NPCs")
    npcs_data = load_data_from_file(PersistenceSettings.settings['npcs_file'])

    validate_load_data_basic_structure(npcs_data)
    validate_load_data_game_basic_metadata(npcs_data)

    if npcs_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for game_level in game.levels:
        level_data = npcs_data['game_levels'].get(f"{game_level.id}")
        if not level_data or not isinstance(level_data['npcs'], dict):
            continue
        npcs_level = level_data['npcs']
        scroll_shift, scroll_shift_top = game_level.get_scroll_shift_delta_tuple(
            game_level, level_data)
        for npc in game_level.npcs:
            npc_data = npcs_level.get(npc.id)
            if not npc_data:
                npc.kill_hook()
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
            npc.npc_summoned_count = npc_data['npc_summoned_count']
            if npc.stats.energy_shield:
                npc.stats.energy_shield.stats.health = npc_data.get(
                    'energy_shield_health', 100)


def _load_npcs_not_initial_data(game):
    game.is_debug and log.debug("Load last saved game NPCs: Not initial actors")
    npcs_data = load_data_from_file(PersistenceSettings.settings['npcs_new_file'])

    validate_load_data_basic_structure(npcs_data)
    validate_load_data_game_basic_metadata(npcs_data)

    if npcs_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for level_id, level_data in npcs_data['game_levels'].items():
        level = game.levels[int(level_id) - 1]
        scroll_shift, scroll_shift_top = level.get_scroll_shift_delta_tuple(
            level, level_data)
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
            npc.hostility_level = npc_data['hostility_level']
            npc.magic_resistance = npc_data['magic_resistance']
            npc.npc_summoned_count = npc_data['npc_summoned_count']
            npcs.append(npc)

            if npc_data['has_energy_shield']:
                EnergyShield.actor_acquire_energy_shield(
                    npc, game, health_total=npc_data['energy_shield_health_total'])
                npc.stats.energy_shield.stats.health = npc_data['energy_shield_health']

            if npc_data['items_to_drop']:
                items_to_drop = []
                for item_data in npc_data['items_to_drop']:
                    item_to_drop = DropItem(
                        getattr(items_module, item_data['type_name'], None)
                        or getattr(npcs_module, item_data['type_name']),
                        probability_to_drop=item_data['probability_to_drop'],
                        x_delta=item_data['x_delta'],
                        y_delta=item_data['y_delta'],
                        **item_data['args'],
                        )
                    items_to_drop.append(item_to_drop)
                npc.items_to_drop = items_to_drop

        level.add_actors(npcs)
