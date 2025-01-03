"""Module invisible_holders."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_MISC_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class InvisibleHolder(ActorItem):
    """Represents an invisible holder.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_MISC_FOLDER
        self.file_name_key = 'im_invisible_holders'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.INVISIBLE_HOLDER
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.cannot_be_copied = True

        super().__init__(x, y, game, name=name)

        self.hostility_level = 0
        self.magic_resistance = 990

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class InvisibleHolderA(InvisibleHolder):
    """Represents an invisible holder of type A.
    This invisible_holder follows the player, so it can hold messages
    that must be seen on the screen.
    """

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.INVISIBLE_HOLDER_A
        super().__init__(x, y, game, name=name)


class InvisibleHolderNarrator(InvisibleHolder):
    """Represents an invisible holder of type narrator.
    This invisible_holder follows the player, so it can hold messages
    that must be seen on the screen.
    """

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.INVISIBLE_HOLDER_N
        super().__init__(x, y, game, name=name)
