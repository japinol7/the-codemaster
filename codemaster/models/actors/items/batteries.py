"""Module batteries."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_BATTERIES_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Battery(ActorItem):
    """Represents a battery.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_BATTERIES_FOLDER
        self.file_name_key = 'im_batteries'
        self.images_sprite_no = 4
        self.category_type = ActorCategoryType.BATTERY
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class BatteryA(Battery):
    """Represents a battery of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.BATTERY_A
        super().__init__(x, y, game, name=name)
