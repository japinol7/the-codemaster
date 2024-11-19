"""Module persistence_items."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy
from itertools import chain

from codemaster.models.actors.actor_types import ActorCategoryType
from codemaster.models.actors.actors import Actor, ActorItem
from codemaster.models.actors import items as items_module
from codemaster.persistence.persistence_settings import (
    GAME_DATA_HEADER,
    PERSISTENCE_NO_SAVED_GAME_DATA_MSG,
    PersistenceSettings,
    )
from codemaster.persistence.exceptions import (
    LoadGameItemsException,
    LoadGameNoSavedGameDataException,
    )
from codemaster.persistence.persistence_utils import (
    load_data_from_file,
    save_data_to_file,
    )
from codemaster.persistence.validations import (
    validate_load_data_game_basic_metadata,
    )
from codemaster.persistence.working_data import (
    actors_map_previous_save_id_with_new_instance,
    )
from codemaster.tools.logger.logger import log


def persist_game_items_data(game):
    _persist_items_data(game)
    _persist_items_not_initial_data(game)


def load_game_items_data(game):
    _load_items_data(game)
    _load_items_not_initial_data(game)


def _persist_items_data(game):
    game.is_debug and log.debug("Save current game items")
    game_data = deepcopy(GAME_DATA_HEADER)
    items_data = ActorItem.get_items_stats_to_persist(game)
    game_data.update(items_data)
    save_data_to_file(PersistenceSettings.settings['items_file'], game_data)


def _persist_items_not_initial_data(game):
    game.is_debug and log.debug("Save current game items: Not initial actors")
    game_data = deepcopy(GAME_DATA_HEADER)
    items_data = ActorItem.get_items_not_initial_actor_stats_to_persist(game)
    game_data.update(items_data)
    save_data_to_file(PersistenceSettings.settings['items_new_file'], game_data)


def validate_load_data_basic_structure(items_data):
    if (not items_data or not isinstance(items_data.get('saved_game_data'), dict)
            or not isinstance(items_data.get('game_levels'), dict)):
        raise LoadGameItemsException("No game data or invalid format!")


def _load_items_data(game):
    game.is_debug and log.debug("Load last saved game items")
    items_data = load_data_from_file(PersistenceSettings.settings['items_file'])

    validate_load_data_basic_structure(items_data)
    validate_load_data_game_basic_metadata(items_data)

    if items_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for level in game.levels:
        level_data = items_data['game_levels'].get(f"{level.id}")
        if not level_data or not isinstance(level_data['items'], dict):
            continue
        items_level = level_data['items']
        scroll_shift, scroll_shift_top = level.get_scroll_shift_delta_tuple(level, level_data)
        for item in chain(level.items, level.doors, level.mines):
            item_data = items_level.get(item.id)
            if not item_data:
                item.kill_hook()
                item.kill()
                continue

            if item_data['category_type'] == ActorCategoryType.DOOR.name:
                item.is_locked = item_data['is_locked']
                continue

            item.health = item_data['health']
            item.stats.health_total = item_data['health_total']
            item.rect.x = item_data['x'] + scroll_shift
            item.rect.y = item_data['y'] - scroll_shift_top
            item.direction = item_data['direction']


def _load_items_not_initial_data(game):
    game.is_debug and log.debug("Load last saved game items: Not initial actors")
    items_data = load_data_from_file(PersistenceSettings.settings['items_new_file'])

    validate_load_data_basic_structure(items_data)
    validate_load_data_game_basic_metadata(items_data)

    if items_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for level_id, level_data in items_data['game_levels'].items():
        level = game.levels[int(level_id) - 1]
        scroll_shift, scroll_shift_top = level.get_scroll_shift_delta_tuple(level, level_data)
        items = []
        for item_id, item_data in level_data['items'].items():
            kwargs_ = {}
            if item_data['category_type'] == ActorCategoryType.POTION.name:
                kwargs_ = {
                    'power': item_data['power'],
                    'power_total': item_data['power_total'],
                    }
            elif item_data['category_type'] == ActorCategoryType.DOOR_KEY.name:
                kwargs_ = {
                    'door': Actor.get_actor(item_data['door']),
                    }
            item = Actor.factory(
                items_module,
                item_data['type_name'],
                x=item_data['x'] + scroll_shift,
                y=item_data['y'] - scroll_shift_top,
                game=game,
                kwargs=kwargs_,
                )
            item.health = item_data['health']
            item.stats.health_total = item_data['health_total']
            item.direction = item_data['direction']
            item.is_location_in_inventory = item_data['is_location_in_inventory']
            if item.is_location_in_inventory:
                actors_map_previous_save_id_with_new_instance[item_id] = item
            items.append(item)
        level.add_actors(items)
        for item in items:
            if item.is_location_in_inventory:
                item.kill_hook()
