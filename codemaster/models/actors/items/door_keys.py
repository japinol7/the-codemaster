"""Module door keys."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_DOOR_KEYS_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats
from codemaster.tools.utils.colors import ColorName


class DoorKey(ActorItem):
    """Represents a door key.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, door, name=None):
        self.door = door
        self.file_folder = BM_DOOR_KEYS_FOLDER
        self.file_name_key = 'im_door_keys'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.DOOR_KEY
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def use_key_in_door(self, door):
        if door is self.door:
            if self.color == self.door.color:
                self.player.sound_effects and self.player.door_unlock_sound.play()
                self.door.is_locked = False


class DoorKeyGreen(DoorKey):
    """Represents a green door key."""

    def __init__(self, x, y, game, door, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.DOOR_KEY_GREEN
        self.color = ColorName.GREEN.name
        self.key_type = 'G'
        super().__init__(x, y, game, door, name=name)


class DoorKeyBlue(DoorKey):
    """Represents a blue door key."""

    def __init__(self, x, y, game, door, name=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.DOOR_KEY_BLUE
        self.color = ColorName.BLUE.name
        self.key_type = 'B'
        super().__init__(x, y, game, door, name=name)


class DoorKeyAqua(DoorKey):
    """Represents an aqua door key."""

    def __init__(self, x, y, game, door, name=None):
        self.file_mid_prefix = '05'
        self.type = ActorType.DOOR_KEY_AQUA
        self.color = ColorName.AQUA.name
        self.key_type = 'A'
        super().__init__(x, y, game, door, name=name)


class DoorKeyYellow(DoorKey):
    """Represents a yellow door key."""

    def __init__(self, x, y, game, door, name=None):
        self.file_mid_prefix = '03'
        self.type = ActorType.DOOR_KEY_YELLOW
        self.color = ColorName.YELLOW.name
        self.key_type = 'Y'
        super().__init__(x, y, game, door, name=name)


class DoorKeyRed(DoorKey):
    """Represents a red door key."""

    def __init__(self, x, y, game, door, name=None):
        self.file_mid_prefix = '04'
        self.type = ActorType.DOOR_KEY_RED
        self.color = ColorName.RED.name
        self.key_type = 'R'
        super().__init__(x, y, game, door, name=name)


class DoorKeyMagenta(DoorKey):
    """Represents a magenta door key."""

    def __init__(self, x, y, game, door, name=None):
        self.file_mid_prefix = '06'
        self.type = ActorType.DOOR_KEY_MAGENTA
        self.color = ColorName.MAGENTA.name
        self.key_type = 'M'
        super().__init__(x, y, game, door, name=name)
