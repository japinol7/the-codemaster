"""Module mines."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_MINES_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats
from codemaster.models.actors.items.explosions import ExplosionA, ExplosionB


class Mine(ActorItem):
    """Represents a mine.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_MINES_FOLDER
        self.file_name_key = 'im_mines'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.MINE
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def explosion(self):
        """When hit, explodes."""
        super().explosion()
        explosion = self.explosion_class(self.rect.x - self.rect.w // 2, self.rect.y - 60,
                                         self.game, owner=self.player)
        self.game.level.explosions.add(explosion)
        self.game.level.all_sprites.add(explosion)


class MineCyan(Mine):
    """Represents a cyan mine."""

    def __init__(self, x, y, game, name=None):
        self.explosion_class = ExplosionB
        self.file_mid_prefix = 't1'
        self.type = ActorType.MINE_CYAN
        super().__init__(x, y, game, name=name)


class MineLilac(Mine):
    """Represents a lilac mine."""

    def __init__(self, x, y, game, name=None):
        self.explosion_class = ExplosionA
        self.file_mid_prefix = 't2'
        self.type = ActorType.MINE_LILAC
        super().__init__(x, y, game, name=name)
