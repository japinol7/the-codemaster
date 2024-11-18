"""Module potions."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.config.constants import BM_POTION_HEALTH_FOLDER, BM_POTION_POWER_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Potion(ActorItem):
    """Represents a potion.
    It is not intended to be instantiated.
    """
    def __init__(
            self, x, y, game, name=None, random_min=0, random_max=0,
            power=None, power_total=None):
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.POTION
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.random_min = random_min
        self.random_max = random_max
        self.stats.strength = self.stats.strength_total = 1

        if power is None:
            self.calculate_power()
        else:
            self.stats.power = power
            self.stats.power_total = self.stats.power if power_total is None else power_total
            if self.stats.power_total < self.stats.power:
                self.stats.power_total = self.stats.power

        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def calculate_power(self):
        if self.random_min == 0 and self.random_max == 0:
            if randint(1, 100) > 85:
                self.stats.power = randint(32, 85)
            else:
                self.stats.power = randint(25, 40)
            self.stats.power_total = self.stats.power
            return
        self.stats.power = randint(self.random_min, self.random_max)
        self.stats.power_total = self.stats.power

    def drink(self):
        self.player.stats[self.owner_stats_key] += self.stats.power
        if self.player.stats[self.owner_stats_key] > 100:
            self.player.stats[self.owner_stats_key] = 100
        self.kill()


class PotionHealth(Potion):
    """Represents a health potion."""

    def __init__(
            self, x, y, game, name=None, random_min=0, random_max=0,
            power=None, power_total=None):
        self.file_folder = BM_POTION_HEALTH_FOLDER
        self.file_name_key = 'im_potion_health'
        self.file_mid_prefix = 't1'
        self.type = ActorType.POTION_HEALTH
        self.owner_stats_key = 'health'

        super().__init__(
            x, y, game, name=name,
            random_min=random_min, random_max=random_max,
            power=power, power_total=power_total)


class PotionPower(Potion):
    """Represents a power potion."""

    def __init__(
            self, x, y, game, name=None, random_min=0, random_max=0,
            power=None, power_total=None):
        self.file_folder = BM_POTION_POWER_FOLDER
        self.file_name_key = 'im_potion_power'
        self.file_mid_prefix = 't1'
        self.type = ActorType.POTION_POWER
        self.owner_stats_key = 'power'

        super().__init__(
            x, y, game, name=name,
            random_min=random_min, random_max=random_max,
            power=power, power_total=power_total)
