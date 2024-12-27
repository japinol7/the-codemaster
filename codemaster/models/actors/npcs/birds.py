"""Module birds."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_BIRDS_FOLDER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats


class Bird(NPC):
    """Represents a bird.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_BIRDS_FOLDER
        self.file_name_key = 'im_birds'
        self.images_sprite_no = 4
        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class BirdGreen(Bird):
    """Represents a green bird."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.BIRD_GREEN

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 0.2
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 0.26
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class BirdBrown(Bird):
    """Represents a brown bird."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.BIRD_BROWN

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 0.26
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 0.3
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)
