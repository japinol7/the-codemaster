"""Module working_data."""
__author__ = 'Joan A. Pinol  (japinol)'

# Mapping of previous saved items in inventory ids with the
# new instance created, needed when loading a game for actors
# not initially on a level that are allocated in the PC inventory.
actors_map_previous_save_id_with_new_instance = {}


def clear_persistence_working_data():
    actors_map_previous_save_id_with_new_instance.clear()


def get_actors_by_previous_save_ids(actor_ids):
    return [actors_map_previous_save_id_with_new_instance[k]
            for k in actor_ids]


def get_actors_by_previous_save_ids_if_exist(actor_ids):
    return [actors_map_previous_save_id_with_new_instance[k]
            for k in actor_ids
            if actors_map_previous_save_id_with_new_instance.get(k)]
