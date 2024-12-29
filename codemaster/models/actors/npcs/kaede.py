"""Module kaede."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    BM_KAEDE_FOLDER,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats


class KaedeBase(NPC):
    """Represents the Kaede NPC base.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_KAEDE_FOLDER
        self.file_name_key = 'im_kaede'
        self.images_sprite_no = 1
        self.can_cast_spells = False

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.magic_resistance = 0
        self.hostility_level = 0


class Kaede(KaedeBase):
    """Represents Kaede NPC."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.KAEDE

        self.stats = Stats()
        self.stats.power = self.stats.power_total = NPC_STRENGTH_BASE
        self.stats.power_recovery = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 2
        self.stats.health = self.stats.health_total = NPC_STRENGTH_BASE * 2

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)
