"""Module working_data."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actors import Actor

# Mapping of old items in inventory ids with the new instance created,
# needed when loading a game for actors not initially on a level
actors_map_old_id_with_new_instance = {}


def clear_persistence_working_data():
    actors_map_old_id_with_new_instance.clear()


def get_actors_by_ids_considering_old_ids(actor_ids):
    return [Actor.actors.get(k)
            or actors_map_old_id_with_new_instance[k]
            for k in actor_ids]


def get_actors_by_ids_considering_old_ids_if_exist(actor_ids):
    return [Actor.actors.get(k)
            or actors_map_old_id_with_new_instance[k]
            for k in actor_ids
            if Actor.actors.get(k) or actors_map_old_id_with_new_instance.get(k)]


def get_actor_by_id_considering_old_id(actor_id):
    return actors_map_old_id_with_new_instance[actor_id]


def get_actor_by_id_considering_old_id_if_exists(actor_id):
    return actors_map_old_id_with_new_instance.get(actor_id)


def set_actor_map_old_id_with_new_instance(actor_id, actor):
    actors_map_old_id_with_new_instance[actor_id] = actor
