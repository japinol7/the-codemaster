"""Module level 11."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    DOOR_DEST_NL,
    DIRECTION_LEFT,
    SCREEN_NEAR_EARTH,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    MageFemaleA,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorKeyMagenta,
    DoorLeftBlue,
    DoorRightMagenta,
    FilesDiskB,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level11(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 10
        self.name = '11'
        self.next_level_left = 9
        self.next_level_right = 11
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(6)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = (220, 520)
        self.player_start_pos_right = (520, 520)
        self.player_start_pos_rtop = (250, -440)
        self.player_start_pos_ltop = (80, 100)
        self.player_start_pos_bottom = (300, 800)
        self.world_start_pos_left = (0, -758)
        self.world_start_pos_right = (self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758)
        self.world_start_pos_rtop = (self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900)
        self.world_start_pos_ltop = (0, -900)

        self._add_actors()
        self._sprites_all_add()

    def _add_actors(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[12, 420, 210, platforms.PLAT_TYPE_01],
                       [2, 1400, 200, platforms.PLAT_TYPE_01],
                       [2, 1580, 300, platforms.PLAT_TYPE_01],
                       [2, 1420, 575, platforms.PLAT_TYPE_01],
                       [21, 1640, 460, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3, add_to_list=self.decors)

        # Add batteries
        self.batteries.add([
            BatteryA(660, 174, self.game),
            BatteryA(720, 174, self.game),
            BatteryA(780, 174, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(900, 173, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(1000, 168, self.game),
            PotionHealth(1080, 168, self.game),
            ])

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=9, door_dest_pos=DOOR_DEST_NL),
            DoorRightMagenta(3640, 550, self.game, level_dest=11, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=14, **{'random_min': 68, 'random_max': 85}),
            DropItem(DoorKeyMagenta, ActorType.DOOR_KEY_MAGENTA, probability_to_drop=100,
                     add_to_list=self.door_keys, x_delta=20, y_delta=50,
                     door=[door for door in self.doors if door.is_locked][0]),
            ]
        mage = MageFemaleA(3570, 655, self.game, items_to_drop=items_to_drop)
        mage.direction = DIRECTION_LEFT
        self.npcs.add([mage])
