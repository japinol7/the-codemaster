"""Module level 14."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.npcs import (
    DragonGreen,
    DragonBlue,
    DragonRed,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorLeftGreen,
    DoorRightYellow,
    FilesDiskB,
    LifeRecoveryA,
    PotionPower,
    )
from codemaster.levels.level_base import Level
from codemaster.models.actors.text_msgs import TextMsg


class Level14(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(1)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def update_pc_enter_level(self):
        super().update_pc_enter_level()
        TextMsg.create("Dragons!\nSo beautiful\nand so dangerous!", self.game, time_in_secs=4)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[7, 620, 380, platforms.PLAT_TYPE_01],
                       [8, 1500, 300, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3, add_to_list=self.decors)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1240, 600, self.game,
            border_top=420, border_down=700, change_y=2, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(1930, 264, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(1984, 263, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(650, 334, self.game),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 40, 'random_max': 60}),
            ]
        self.dragons.add(DragonGreen(550, 640, self.game, border_left=500, border_right=2200,
                                     border_top=50, border_down=780, change_x=1, change_y=1,
                                     items_to_drop=items_to_drop))
        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=80, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 60, 'random_max': 75}),
            DropItem(LifeRecoveryA, ActorType.LIFE_RECOVERY, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=70),
            ]
        self.dragons.add(DragonBlue(760, 500, self.game, border_left=600, border_right=2820,
                                    border_top=50, border_down=780, change_x=1, change_y=1,
                                    items_to_drop=items_to_drop))
        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 80, 'random_max': 80}),
            DropItem(LifeRecoveryA, ActorType.LIFE_RECOVERY, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=70),
            ]
        self.dragons.add(DragonRed(2000, 700, self.game, border_left=1160, border_right=2950,
                                   border_top=50, border_down=780, change_x=1, change_y=1,
                                   items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=12, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(3640, 550, self.game, level_dest=14, door_dest_pos=DOOR_DEST_NL),
            ])
