"""Module ghosts."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_GHOSTS_FOLDER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats


class Ghost(NPC):
    """Represents a ghost.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_GHOSTS_FOLDER
        self.file_name_key = 'im_en_ghosts'
        self.images_sprite_no = 1
        self.can_be_killed_normally = False
        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

    def update_when_hit(self):
        """Ghosts cannot be hit with normal weapons.
        Right now is transparent for bullets and cannot be killed
        """
        pass


class GhostGreen(Ghost):
    """Represents a green ghost."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '05'
        self.type = ActorType.GHOST_GREEN

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 1
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 1.1
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class GhostBlue(Ghost):
    """Represents a blue ghost."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '06'
        self.type = ActorType.GHOST_BLUE

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 1
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 1.2
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class GhostYellow(Ghost):
    """Represents a yellow ghost."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '07'
        self.type = ActorType.GHOST_YELLOW

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 1
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 2
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class GhostRed(Ghost):
    """Represents a red ghost."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '08'
        self.type = ActorType.GHOST_RED

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 1
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 5
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)
