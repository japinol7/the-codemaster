"""Module clean_new_game."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actors import Actor
from codemaster.models.actors.items.platforms import Platform
from codemaster.models.actors.items.bullets import Bullet
from codemaster.models.actors.npcs.snakes import SnakeBodyPiece
from codemaster.models.actors.npcs.dragons import DragonBodyPiece
from codemaster.models.clocks import ClockBase
from codemaster.models.special_effects.light import Light
from codemaster.models.special_effects.vortex import Vortex
from codemaster.persistence.working_data import clear_persistence_working_data
from codemaster.tools.logger.logger import log


def clean_entity_ids():
    log.info("Clean game data")
    Actor.actors.clear()
    clear_persistence_working_data()
    Actor.type_id_count.clear()
    SnakeBodyPiece.type_id_count.clear()
    DragonBodyPiece.type_id_count.clear()
    Platform.type_id_count.clear()
    Bullet.type_id_count.clear()
    ClockBase.type_id_count.clear()
    Light.type_id_count.clear()
    Vortex.type_id_count.clear()
