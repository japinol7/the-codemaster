"""Module life recoveries."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_LIVES_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class LifeRecovery(ActorItem):
    """Represents a life recovery.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_LIVES_FOLDER
        self.file_name_key = 'life_recoveries'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.LIFE_RECOVERY
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class LifeRecoveryA(LifeRecovery):
    """Represents a life recovery of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.LIFE_RECOVERY
        self.owner_stats_key = 'lives'
        super().__init__(x, y, game, name=name)
