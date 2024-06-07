"""Module radios."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_MISC_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Radio(ActorItem):
    """Represents a radio.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_MISC_FOLDER
        self.file_name_key = 'im_radios'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.RADIO
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1

        super().__init__(x, y, game, name=name)

        self.hostility_level = 0
        self.magic_resistance = 990

    def update_after_inc_index_hook(self):
        self.rect.x = self.player.rect.x - 300
        if self.rect.x < 10:
            self.rect.x = 10
        self.rect.y = self.player.rect.y - 250

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class RadioA(Radio):
    """Represents a radio of type A.
    This radio follows the player, so it can hold messages
    that must be seen on the screen.
    """

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.RADIO_A
        super().__init__(x, y, game, name=name)
