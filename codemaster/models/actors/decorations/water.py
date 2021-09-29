"""Module water."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_PLAT_WATER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats

PLAT_WATER_WIDTH = 216
PLAT_WATER_HEIGHT = 72


class Water(ActorItem):
    """Represents a block of water.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_PLAT_WATER
        self.file_name_key = 'im_water'
        self.transparency_alpha = True
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """A block of water cannot be hit."""
        pass

    @staticmethod
    def create_water(x, y, game, qty, qty_depth, add_to_list):
        xx, yy = x, y
        for _ in range(qty):
            add_to_list.add(WaterA(xx, yy, game))
            xx += PLAT_WATER_WIDTH
        for __ in range(qty_depth):
            xx = x
            yy += PLAT_WATER_HEIGHT
            for _ in range(qty):
                add_to_list.add(WaterADeep(xx, yy, game))
                xx += PLAT_WATER_WIDTH


class WaterA(Water):
    """Represents a superficial block of water."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.images_sprite_no = 4
        self.type = ActorType.PLAT_WATER_A
        super().__init__(x, y, game, name=name)


class WaterADeep(Water):
    """Represents a deep block of water."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_WATER_A_DEEP
        super().__init__(x, y, game, name=name)
