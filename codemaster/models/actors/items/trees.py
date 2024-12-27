"""Module trees."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_ITEM_DECORATIONS
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class Tree(ActorItem):
    """Represents a tree.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_ITEM_DECORATIONS
        self.file_name_key = 'im_tree'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.ITEM_DECORATION
        self.transparency_alpha = True
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.visited = False
        self.cannot_be_copied = True

        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class TreeA(Tree):
    """Represents a tree of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.TREE_A
        super().__init__(x, y, game, name=name)


class TreeB(Tree):
    """Represents a tree of type B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.TREE_B
        super().__init__(x, y, game, name=name)
