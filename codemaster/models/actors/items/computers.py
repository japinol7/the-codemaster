"""Module computers."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_COMPUTERS_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Computer(ActorItem):
    """Represents a computer.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_COMPUTERS_FOLDER
        self.file_name_key = 'im_computer'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.COMPUTER
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class ComputerA(Computer):
    """Represents a computer of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.COMPUTER_01
        super().__init__(x, y, game, name=name)
