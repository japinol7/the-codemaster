"""Module vampires."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_NPCS_FOLDER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats


class Vampire(NPC):
    """Represents a vampire.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_vampires'
        self.images_sprite_no = 1
        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class VampireMale(Vampire):
    """Represents a classic male vampire."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '15'
        self.type = ActorType.VAMPIRE_MALE

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 6
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 8
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class VampireFemale(Vampire):
    """Represents a modern female vampire."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '16'
        self.type = ActorType.VAMPIRE_FEMALE

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 7
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 10
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)
