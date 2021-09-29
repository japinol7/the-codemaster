"""Module cartridges."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_CARTRIDGES_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Cartridge(ActorItem):
    """Represents a cartridge.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_CARTRIDGES_FOLDER
        self.file_name_key = 'im_cartridges'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.CARTRIDGE
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class CartridgeGreen(Cartridge):
    """Represents a green cartridge."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.CARTRIDGE_GREEN
        super().__init__(x, y, game, name=name)


class CartridgeBlue(Cartridge):
    """Represents a blue cartridge."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.CARTRIDGE_BLUE
        super().__init__(x, y, game, name=name)


class CartridgeYellow(Cartridge):
    """Represents a yellow cartridge."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '03'
        self.type = ActorType.CARTRIDGE_YELLOW
        super().__init__(x, y, game, name=name)


class CartridgeRed(Cartridge):
    """Represents a red cartridge."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '04'
        self.type = ActorType.CARTRIDGE_RED
        super().__init__(x, y, game, name=name)
