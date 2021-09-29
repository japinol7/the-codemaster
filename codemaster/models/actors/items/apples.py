"""Module apples."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_APPLES_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Apple(ActorItem):
    """Represents a apple.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_APPLES_FOLDER
        self.file_name_key = 'im_apples'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.APPLE
        self.stats.health = self.stats.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def eat(self):
        self.player.stats['health'] += self.stats.power
        if self.player.stats['health'] > 100:
            self.player.stats['health'] = 100
        self.kill()


class AppleGreen(Apple):
    """Represents a green apple."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = 't2'
        self.type = ActorType.APPLE_GREEN
        self.apple_type = 'G'
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 2
        super().__init__(x, y, game, name=name)


class AppleYellow(Apple):
    """Represents a yellow apple."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = 't3'
        self.type = ActorType.APPLE_YELLOW
        self.apple_type = 'Y'
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 5
        super().__init__(x, y, game, name=name)


class AppleRed(Apple):
    """Represents a red apple."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = 't1'
        self.type = ActorType.APPLE_RED
        self.apple_type = 'R'
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 7
        super().__init__(x, y, game, name=name)
