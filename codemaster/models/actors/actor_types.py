"""Module actor types."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum

NPC_STD_WIDTH = 61
NPC_STD_HEIGHT = 61
NPC_STRENGTH_BASE = 35


class ActorBaseType(Enum):
    """Actor base types."""
    NONE = 0
    PLATFORM = 1
    PC = 11
    NPC = 21
    ITEM = 51
    SNAKE_BODY_PART = 101


class ActorCategoryType(Enum):
    """Actor base types."""
    NONE = 0
    BATTERY = 1
    LIFE_RECOVERY = 2
    POTION = 3
    CARTRIDGE = 4
    COMPUTER = 5
    FILES_DISK = 6
    DOOR = 7
    DOOR_KEY = 8
    APPLE = 9
    MINE = 10
    EXPLOSION = 11
    PC = 51
    NPC = 61
    SNAKE = 65
    SNAKE_BODY_PART = 67


class ActorType(Enum):
    """Actor types."""
    NONE = 0
    PLAYER = 1
    BULLET = 121
    # Objects
    BATTERY_A = 301
    # Life recoveries
    LIFE_RECOVERY = 321
    # Potions
    POTION_HEALTH = 331
    POTION_POWER = 332
    # Cartridges
    CARTRIDGE_GREEN = 452
    CARTRIDGE_BLUE = 453
    CARTRIDGE_YELLOW = 454
    CARTRIDGE_RED = 455
    # Computers
    COMPUTER_01 = 501
    FILES_DISK_A = 521
    FILES_DISK_B = 522
    FILES_DISK_C = 523
    FILES_DISK_D = 524
    # Doors
    DOOR_LEFT_GREEN = 611
    DOOR_LEFT_BLUE = 612
    DOOR_LEFT_YELLOW = 613
    DOOR_LEFT_AQUA = 614
    DOOR_LEFT_WHITE = 615
    DOOR_LEFT_GOLD = 616
    DOOR_LEFT_RED = 617
    DOOR_RIGHT_GREEN = 651
    DOOR_RIGHT_BLUE = 652
    DOOR_RIGHT_YELLOW = 653
    DOOR_RIGHT_AQUA = 654
    DOOR_RIGHT_WHITE = 655
    DOOR_RIGHT_GOLD = 656
    DOOR_RIGHT_RED = 657
    # Doors
    DOOR_KEY_GREEN = 711
    DOOR_KEY_BLUE = 712
    DOOR_KEY_YELLOW = 713
    DOOR_KEY_AQUA = 714
    DOOR_KEY_WHITE = 715
    DOOR_KEY_GOLD = 716
    DOOR_KEY_RED = 717
    # Water
    PLAT_WATER_A = 851
    PLAT_WATER_A_DEEP = 852
    # Platforms
    PLATFORM_A = 4001
    PLAT_MOVING = 4002
    PLAT_SLIDING = 4003
    # Apples
    APPLE_GREEN = 5031
    APPLE_YELLOW = 5032
    APPLE_RED = 5033
    # Mines
    MINE_CYAN = 5041
    MINE_LILAC = 5042
    # Explosions
    EXPLOSION_A = 5051
    EXPLOSION_B = 5052
    # Skulls
    SKULL_GREEN = 1201
    SKULL_BLUE = 1202
    SKULL_YELLOW = 1203
    SKULL_RED = 1204
    # Ghosts
    GHOST_GREEN = 1221
    GHOST_BLUE = 1222
    GHOST_YELLOW = 1223
    GHOST_RED = 1224
    # Bats
    BAT_BLUE = 1331
    BAT_LILAC = 1332
    BAT_RED = 1333
    BAT_BLACK = 1334
    # Wolfmen
    WOLFMAN_MALE = 1351
    # Vampires
    VAMPIRE_MALE = 1371
    VAMPIRE_FEMALE = 1372
    # Demons
    DEMON_MALE = 1391
    # Snakes
    SNAKE_BODY_PART_A = 1400
    SNAKE_GREEN = 1401
    SNAKE_BLUE = 1402
    SNAKE_YELLOW = 1403
    SNAKE_RED = 1404
    # Terminator Eyes
    TERMINATOR_EYE_GREEN = 1601
    TERMINATOR_EYE_BLUE = 1602
    TERMINATOR_EYE_YELLOW = 1603
    TERMINATOR_EYE_RED = 1604
    # Terminator Big Eyes
    TERMINATOR_BIG_EYE_GREEN = 1611
    TERMINATOR_BIG_EYE_BLUE = 1612
    TERMINATOR_BIG_EYE_YELLOW = 1613
    TERMINATOR_BIG_EYE_RED = 1614
