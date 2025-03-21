"""Module level test 2."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

import pygame as pg

from codemaster.config.constants import (
    SCREEN_HEIGHT,
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    BatBlack,
    BatLilac,
    DemonMale,
    SkullBlue,
    SkullYellow,
    TerminatorEyeGreen,
    TerminatorEyeYellow,
    VampireMale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    ComputerA,
    DoorLeftGreen,
    DoorRightYellow,
    FilesDiskD,
    PotionHealth,
    )
from codemaster.levels.level_base import Level


class LevelTest2(Level):

    def __init__(self, id_, game):
        self.level_limit = -2700
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
        self.player_start_pos_left = 250, 480
        self.player_start_pos_right = 600, 470
        self.player_start_pos_rtop = 300, 100
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 100, 460, platforms.PLAT_TYPE_01],
                       [5, 300, 220, platforms.PLAT_TYPE_01],
                       [4, 980, 562, platforms.PLAT_TYPE_01],
                       [3, 1100, 260, platforms.PLAT_TYPE_01],
                       [9, 1906, 110, platforms.PLAT_TYPE_01],
                       [3, 1300, 120, platforms.PLAT_TYPE_01],
                       [8, 2580, 440, platforms.PLAT_TYPE_01],
                       [4, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [44, 630, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 206, self.game, qty=19, qty_depth=3)

        # Add grass blocks
        Grass.create_grass_sm(
            0, SCREEN_NEAR_EARTH , self.game, qty=2, qty_depth=4,
            actor_type=ActorType.PLAT_GRASS_F_SM)
        Grass.create_grass_sm(
            630, SCREEN_NEAR_EARTH , self.game, qty=22, qty_depth=4,
            actor_type=ActorType.PLAT_GRASS_F_SM)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1350, 510, self.game,
            border_left=1250, border_right=1650, change_x=2, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 360, self.game,
            border_left=1350, border_right=2650, change_x=7, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 950, 260, self.game,
            border_top=200, border_down=450, change_y=3, level=self))

        # Add sliding bands (n_blocs, x, y, type, velocity)
        level_plats = [[5, 280, SCREEN_HEIGHT - platforms.PLAT_TYPE_03_SLIDING_R_MID[3], platforms.PLAT_TYPE_03_SLIDING, -2],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3], velocity=platform[4])
        for platform in plats:
            block = platforms.SlidingBands(platform[0], platform[1], platform[2],
                                           self.game, velocity=platform[3], level=self)
            self.platforms.add(block)

        # Add batteries
        self.batteries.add([
            BatteryA(2360, 74, self.game),
            BatteryA(2400, 74, self.game),
            BatteryA(2440, 74, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskD(1040, 526, self.game),
            FilesDiskD(2200, 74, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(2960, 336, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullYellow(2360, 47, self.game, border_left=2180, border_right=2500, change_x=3),
            VampireMale(1880, 14, self.game, border_left=1865, border_right=2245, change_x=2),
            ])

        self.npcs.add([
            BatBlack(1900, 550, self.game, border_left=1780, border_right=2600, change_x=4),
            BatBlack(2120, 620, self.game, border_left=1780, border_right=2600, change_x=5),
            BatLilac(2250, 570, self.game, border_left=1780, border_right=2600, change_x=4),
            ])

        self.npcs.add([
            TerminatorEyeYellow(1700, 650, self.game, border_left=1680, border_right=2370,
                                change_x=3),
            ])

        items_to_drop = [
            DropItem(PotionHealth, x_delta=16, **{'random_min': 58, 'random_max': 72}),
            ]
        self.npcs.add([
            DemonMale(2280, 662, self.game, border_left=1680, border_right=2370,
                      change_x=3, items_to_drop=items_to_drop),
            ])

        self.npcs.add(SkullBlue(
            320 + randint(15, 200), 145, self.game,
            border_left=310, border_right=600, change_x=randint(3, 7)))

        self.npcs.add([
            TerminatorEyeGreen(3000, 355, self.game, border_left=2660, border_right=3200, change_x=2),
            ])

        # Add doors
        self.doors.add([
            DoorLeftGreen(0, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorRightYellow(3400, 550, self.game, level_dest=2, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
