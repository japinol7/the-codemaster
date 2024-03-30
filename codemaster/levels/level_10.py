"""Module level 10."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    RobotA,
    RobotB,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorRightBlue,
    DoorLeftYellow,
    FilesDiskB,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level10(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 9
        self.name = '10'
        self.next_level_left = 8
        self.next_level_right = 10
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(3)).convert()
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
        level_plats = [[12, 620, 210, platforms.PLAT_TYPE_01],
                       [2, 1600, 335, platforms.PLAT_TYPE_01],
                       [2, 1780, 460, platforms.PLAT_TYPE_01],
                       [2, 1960, 585, platforms.PLAT_TYPE_01],
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

        # Add NPCs
        robots = [
            RobotA(1900, 665, self.game, border_left=1900, border_right=2400, change_x=3),
            RobotB(2220, 665, self.game, border_left=1850, border_right=2250, change_x=2),
            ]
        self.npcs.add(robots)

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=8, door_dest_pos=DOOR_DEST_NL),
            DoorRightBlue(3640, 550, self.game, level_dest=10, door_dest_pos=DOOR_DEST_NL),
            ])
