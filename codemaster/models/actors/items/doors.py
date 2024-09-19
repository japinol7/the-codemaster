"""Module doors."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import (
    BM_DOORS_FOLDER,
    DOOR_POSITION_L,
    DOOR_POSITION_R,
    )
from codemaster.tools.utils.colors import ColorName
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem, Actor
from codemaster.models.stats import Stats


class Door(ActorItem):
    """Represents a door.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_folder = BM_DOORS_FOLDER
        self.file_name_key = 'im_doors'
        self.images_sprite_no = 2
        self.category_type = ActorCategoryType.DOOR
        self.level_dest = level_dest
        self.door_dest_pos = door_dest_pos
        self.is_locked = is_locked
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.cannot_be_copied = True

        super().__init__(x, y, game, name=name)

    def update(self):
        # Set door image as unlocked or locked
        old_frame_index = self.frame_index
        self.frame_index = 1 if self.is_locked else 0
        if old_frame_index != self.frame_index:
            self.image = Actor.sprite_images[self.type.name][self.direction][int(self.frame_index)]

    def init_after_load_sprites_hook(self):
        self.frame_index = 1 if self.is_locked else 0
        self.image = Actor.sprite_images[self.type.name][self.direction][int(self.frame_index)]

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    @staticmethod
    def get_doors_dest_to_level(level_dest, game):
        """Gets all the doors that go to a given level."""
        return [door for level in game.levels for door in level.doors
                if door.level_dest == level_dest]

    @staticmethod
    def get_level_doors_dest_to_level(level_dest, game, level_orig):
        """Gets all the doors from a level that go to a given level."""
        return [door for door in game.levels[level_orig].doors
                if door.level_dest == level_dest]

    @staticmethod
    def get_doors_dest_to_level_filtered_by_door_type_position(
            level_dest, door_position, game):
        """Gets all the doors that go to a given level filtered by a given
        door type position.
        """
        return [door for level in game.levels for door in level.doors
                if door.level_dest == level_dest and door.door_type == door_position]

    @staticmethod
    def get_level_doors_dest_to_level_filtered_by_door_type_pos(
            level_dest, door_position, game, level_orig):
        """Gets all the doors from a level that go to a given level filtered by a given
        door type position.
        """
        return [door for door in game.levels[level_orig].doors
                if door.level_dest == level_dest and door.door_type == door_position]


class DoorLeftGreen(Door):
    """Represents a left green door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't01_left'
        self.type = ActorType.DOOR_LEFT_GREEN
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.GREEN.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightGreen(Door):
    """Represents a right green door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't01_right'
        self.type = ActorType.DOOR_RIGHT_GREEN
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.GREEN.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftBlue(Door):
    """Represents a left blue door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't02_left'
        self.type = ActorType.DOOR_LEFT_BLUE
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.BLUE.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightBlue(Door):
    """Represents a right blue door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't02_right'
        self.type = ActorType.DOOR_RIGHT_BLUE
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.BLUE.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftYellow(Door):
    """Represents a left yellow door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't03_left'
        self.type = ActorType.DOOR_LEFT_YELLOW
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.YELLOW.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightYellow(Door):
    """Represents a right yellow door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't03_right'
        self.type = ActorType.DOOR_RIGHT_YELLOW
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.YELLOW.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftAqua(Door):
    """Represents a left aqua door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't05_left'
        self.type = ActorType.DOOR_LEFT_AQUA
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.AQUA.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightAqua(Door):
    """Represents a right aqua door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't05_right'
        self.type = ActorType.DOOR_RIGHT_AQUA
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.AQUA.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftWhite(Door):
    """Represents a left white door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't06_left'
        self.type = ActorType.DOOR_LEFT_WHITE
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.WHITE.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightWhite(Door):
    """Represents a right white door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't06_right'
        self.type = ActorType.DOOR_RIGHT_WHITE
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.WHITE.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftGold(Door):
    """Represents a left gold door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't07_left'
        self.type = ActorType.DOOR_LEFT_GOLD
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.GOLD.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightGold(Door):
    """Represents a right gold door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't07_right'
        self.type = ActorType.DOOR_RIGHT_GOLD
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.GOLD.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftRed(Door):
    """Represents a left red door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't04_left'
        self.type = ActorType.DOOR_LEFT_RED
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.RED.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightRed(Door):
    """Represents a right red door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't04_right'
        self.type = ActorType.DOOR_RIGHT_RED
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.RED.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorLeftMagenta(Door):
    """Represents a left magenta door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't08_left'
        self.type = ActorType.DOOR_LEFT_MAGENTA
        self.door_type = DOOR_POSITION_L
        self.color = ColorName.MAGENTA.name
        self.is_right_door = False
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)


class DoorRightMagenta(Door):
    """Represents a right magenta door."""

    def __init__(self, x, y, game, level_dest, door_dest_pos, name=None, is_locked=False):
        self.file_mid_prefix = 't08_right'
        self.type = ActorType.DOOR_RIGHT_MAGENTA
        self.door_type = DOOR_POSITION_R
        self.color = ColorName.MAGENTA.name
        self.is_right_door = True
        super().__init__(x, y, game, level_dest, door_dest_pos, name=name, is_locked=is_locked)
