"""Module level 2."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_HEIGHT,
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    BatBlack,
    RobotA,
    GhostBlue,
    SkullGreen,
    SkullYellow,
    SkullRed,
    )
from codemaster.models.actors.items import (
    BatteryA,
    ClockA,
    DoorRightGreen,
    DoorLeftYellow,
    FilesDiskD,
    FilesDiskC,
    LifeRecoveryA,
    MineCyan,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level2(Level):

    def __init__(self, id_, game):
        self.level_limit = -2500
        self.background = pg.image.load(self.file_name_im_get(2)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 650, 408
        self.player_start_pos_rtop = 300, 100
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [5, 100, 460, platforms.PLAT_TYPE_01],
            [5, 300, 220, platforms.PLAT_TYPE_01],
            [4, 980, 500, platforms.PLAT_TYPE_01],
            [3, 700, 440, platforms.PLAT_TYPE_01],
            [3, 1100, 260, platforms.PLAT_TYPE_01],
            [9, 1900, 110, platforms.PLAT_TYPE_01],
            [4, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [16, 490, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [24, 1700, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 206, self.game, qty=19, qty_depth=3)

        # Add grass blocks
        Grass.create_grass_sm(
            0, SCREEN_NEAR_EARTH , self.game, qty=2, qty_depth=3,
            actor_type=ActorType.PLAT_GRASS_G_SM)
        Grass.create_grass_sm(
            490, SCREEN_NEAR_EARTH , self.game, qty=8, qty_depth=5,
            actor_type=ActorType.PLAT_GRASS_G_SM)
        Grass.create_grass_sm(
            1700, SCREEN_NEAR_EARTH , self.game, qty=12, qty_depth=5,
            actor_type=ActorType.PLAT_GRASS_G_SM)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1350, 620, self.game,
            border_left=1250, border_right=1650, change_x=2, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 360, self.game,
            border_left=1350, border_right=2650, change_x=7, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 950, 260, self.game,
            border_top=200, border_down=450, change_y=3, level=self))

        # Add sliding bands (n_blocs, x, y, type, velocity)
        level_plats = [
            [3, 280, SCREEN_HEIGHT - platforms.PLAT_TYPE_03_SLIDING_R_MID[3], platforms.PLAT_TYPE_03_SLIDING, -2],
            [3, 1300, 120, platforms.PLAT_TYPE_03_SLIDING, 3]
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3], velocity=platform[4])
        for platform in plats:
            block = platforms.SlidingBands(
                platform[0], platform[1], platform[2],
                self.game, velocity=platform[3], level=self)
            self.platforms.add(block)

        # Add clocks
        self.clocks.add([
            ClockA(540, 174, self.game, time_in_secs=30),
            ])

        # Add batteries
        self.batteries.add([
            BatteryA(410, 184, self.game),
            BatteryA(1400, 84, self.game),
            BatteryA(2200, 74, self.game),
            BatteryA(2300, 74, self.game),
            BatteryA(2380, 74, self.game),
            BatteryA(2390, 74, self.game),
            BatteryA(2400, 74, self.game),
            BatteryA(2410, 74, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskC(340, 184, self.game),
            FilesDiskD(1300, 84, self.game),
            ])

        # Add rec_potions
        self.potions.add([
            PotionHealth(340, 650, self.game),
            PotionPower(1140, 464, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(840, 260, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            GhostBlue(1200, 197, self.game, border_left=1070, border_right=1280, change_x=2),
            SkullGreen(2360, 47, self.game, border_left=2180, border_right=2500, change_x=3),
            SkullYellow(1860, 47, self.game, border_left=1860, border_right=2240, change_x=2),
            SkullRed(410, 600, self.game, border_left=410, border_right=800, change_x=2),
            SkullYellow(600, 600, self.game, border_left=410, border_right=800, change_x=2),
            BatBlack(1900, 640, self.game, border_left=1900, border_right=2400, change_x=3),
            BatBlack(2220, 640, self.game, border_left=1850, border_right=2250, change_x=2),
            RobotA(650, 650, self.game, border_left=620, border_right=920, change_x=2),
            RobotA(780, 650, self.game, border_left=620, border_right=920, change_x=2),
            ])

        # Add mines
        x = 600
        for i in range(16):
            self.mines.add(MineCyan(x, 711, self.game))
            x += 25

        # Add doors
        self.doors.add([
            DoorRightGreen(3150, 550, self.game, level_dest=2, door_dest_pos=DOOR_DEST_NL),
            DoorLeftYellow(0, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL),
            ])
