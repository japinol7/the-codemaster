"""Module level 5."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.npcs import (
    BatBlue,
    BatLilac,
    BatRed,
    BatBlack,
    TerminatorEyeBlue,
    TerminatorEyeYellow,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleYellow,
    AppleRed,
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    DoorLeftYellow,
    DoorRightRed,
    DoorKeyRed,
    FilesDiskB,
    LifeRecoveryA,
    MineCyan,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level5(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 4
        self.name = '05'
        self.next_level_left = 4
        self.next_level_right = 6
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(5)).convert()
        self.level_limit = -2700
        self.level_limit_top = -1000
        self.player_start_pos_left = (250, 480)
        self.player_start_pos_right = (600, 480)
        self.player_start_pos_rtop = (300, 100)
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
        level_plats = [[3, 300, 460, platforms.PLAT_TYPE_01],
                       [7, 500, 220, platforms.PLAT_TYPE_01],
                       [4, 980, 570, platforms.PLAT_TYPE_01],
                       [3, 800, 440, platforms.PLAT_TYPE_01],
                       [5, 1105, 260, platforms.PLAT_TYPE_01],
                       [9, 1900, 185, platforms.PLAT_TYPE_01],
                       [6, 2900, 185, platforms.PLAT_TYPE_01],
                       [8, 2580, 440, platforms.PLAT_TYPE_01],
                       [22, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       [30, 1700, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)
    
        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1640, 360, self.game,
            border_left=1510, border_right=2650, change_x=4, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(1410, 226, self.game),
            BatteryA(2200, 149, self.game),
            BatteryA(2275, 149, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(532, 184, self.game),
            FilesDiskB(3250, 149, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(572, 184, self.game),
            ])

        # Add apples
        self.apples.add([
            AppleGreen(2360, 160, self.game),
            AppleYellow(2420, 160, self.game),
            AppleRed(2500, 160, self.game),
            ])

        # Add NPCs. Several bats
        bat_classes_1 = [BatBlue, BatRed, BatLilac, BatBlack,
                         BatRed, BatBlue, BatBlack, BatLilac, BatBlack,
                         ]
        bat_classes_2 = [BatBlue, BatBlue, BatBlack, BatLilac,
                         BatRed, BatBlack, BatRed, BatBlue, BatBlack,
                         ]
        x, y, border_l_delta = 100, 590, 110
        for i, bat_classes in enumerate(zip(bat_classes_1, bat_classes_2, bat_classes_1)):
            self.npcs.add(bat_classes[0](
                x, y, self.game,
                border_left=94, border_right=1120, change_x=3))
            self.npcs.add(bat_classes[1](
                x + 110, y, self.game,
                border_left=94 + border_l_delta, border_right=1230, change_x=3))
            self.npcs.add(bat_classes[0](
                x + 220, y, self.game,
                border_left=94 + border_l_delta * 2, border_right=1340, change_x=3))
            x += 100
            y -= 70

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 58, 'random_max': 72}),
            DropItem(LifeRecoveryA, ActorType.LIFE_RECOVERY, probability_to_drop=25, add_to_list=self.life_recs,
                     x_delta=120),
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_GREEN, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=170),
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=80, add_to_list=self.cartridges,
                     x_delta=195),
            DropItem(BatLilac, ActorType.BAT_LILAC, probability_to_drop=100, add_to_list=self.npcs,
                     **{'border_left': 2890, 'border_right': 3300, 'change_x': 3}),
            ]
        self.npcs.add([
            TerminatorEyeYellow(2900, 92, self.game, border_left=2890, border_right=3300, change_x=3,
                                items_to_drop=items_to_drop),
            ])

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 40, 'random_max': 64}),
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=90, add_to_list=self.cartridges,
                     x_delta=195),
            ]
        self.npcs.add([
            TerminatorEyeBlue(1760, 644, self.game, border_left=1700, border_right=2150, change_x=2,
                              items_to_drop=items_to_drop),
            ])

        # Add mines
        x = 616
        for i in range(4):
            self.mines.add(MineCyan(x, 190, self.game))
            x += 28

        x = 616
        for i in range(4):
            self.mines.add(MineCyan(x, 160, self.game))
            x += 28

        # Add doors
        self.doors.add([
            DoorRightRed(3400, 550, self.game, level_dest=5, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorLeftYellow(2, 550, self.game, level_dest=3, door_dest_pos=DOOR_DEST_TR),
            ])

        # Add door keys
        self.door_keys.add([
            DoorKeyRed(2800, 360, self.game, door=[door for door in self.doors if door.is_locked][0]),
            ])
