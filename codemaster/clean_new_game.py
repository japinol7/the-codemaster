"""Module clean_new_game."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actors import Actor
from codemaster.models.actors.items.platforms import Platform
from codemaster.models.actors.items.bullets import Bullet
from codemaster.models.actors.npcs.snakes import SnakeBodyPiece
from codemaster.models.clocks import ClockBase


def clean_entity_ids():
    Actor.type_id_count.clear()
    SnakeBodyPiece.type_id_count.clear()
    Platform.type_id_count.clear()
    Bullet.type_id_count.clear()
    ClockBase.type_id_count.clear()
