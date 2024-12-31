"""Module level 4."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    BatBlue,
    BatBlack,
    DemonMale,
    SnakeBlue,
    VampireMale,
    VampireFemale,
    WolfManMale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeYellow,
    DoorRightBlue,
    DoorLeftYellow,
    DoorRightYellow,
    DoorKeyYellow,
    FilesDiskB,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level4(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 500, 408
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [5, 100, 460, platforms.PLAT_TYPE_01],
            [14, 300, 220, platforms.PLAT_TYPE_01],
            [4, 980, 580, platforms.PLAT_TYPE_01],
            [6, 1300, 120, platforms.PLAT_TYPE_01],
            [7, 500, 450, platforms.PLAT_TYPE_01],
            [2, 20, 340, platforms.PLAT_TYPE_01],
            [9, 1900, 110, platforms.PLAT_TYPE_01],
            [6, 2600, 10, platforms.PLAT_TYPE_01],
            [22, 1350, 460, platforms.PLAT_TYPE_01],
            [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=19, qty_depth=3)

        # Add grass blocks
        Grass.create_grass_sm(0, SCREEN_NEAR_EARTH , self.game, qty=112, qty_depth=4,
            actor_type=ActorType.PLAT_GRASS_F_SM)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 310, self.game,
            border_left=1350, border_right=2770, change_x=6, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(2410, 74, self.game),
            BatteryA(564, 415, self.game),
            BatteryA(614, 415, self.game),
            BatteryA(664, 415, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(2500, 74, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionHealth(2350, 72, self.game),
            PotionPower(1000, 182, self.game),
            ])

        # Add NPCs
        item_to_drop = DropItem(CartridgeYellow)
        self.npcs.add(VampireFemale(
            1400, 46, self.game, border_left=1310, border_right=1680,
            change_x=2, items_to_drop=[item_to_drop]))

        item_to_drop = DropItem(PotionPower, y_delta=37, **{'random_min': 65, 'random_max': 75})
        self.npcs.add(DemonMale(
            800, 146, self.game,
            border_left=690, border_right=1210, change_x=3, items_to_drop=[item_to_drop]))

        self.npcs.add([
            WolfManMale(2360, 37, self.game, border_left=2180, border_right=2500, change_x=3),
            VampireMale(1860, 14, self.game, border_left=1860, border_right=2240, change_x=2),
            BatBlack(510, 385, self.game, border_left=410, border_right=1100, change_x=3),
            BatBlack(760, 404, self.game, border_left=410, border_right=1100, change_x=3),
            WolfManMale(1900, 662, self.game, border_left=1900, border_right=2400, change_x=3),
            WolfManMale(2220, 662, self.game, border_left=1850, border_right=2250, change_x=2),
            BatBlue(2380, 346, self.game, border_left=1700, border_right=2450, change_x=3),
            BatBlue(2000, 365, self.game, border_left=1700, border_right=2450, change_x=3),
            ])

        item_to_drop = DropItem(BatBlack, **{'border_left': 1700, 'border_right': 2450, 'change_x': 3})
        self.npcs.add(BatBlue(
            2190, 384, self.game,
            border_left=1700, border_right=2450, change_x=3, items_to_drop=[item_to_drop]))

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 65, 'random_max': 75}),
            DropItem(CartridgeGreen, x_delta=170),
            ]
        self.snakes.add(SnakeBlue(2250, 220, self.game, border_left=1800, border_right=2750,
                                  border_top=120, border_down=850, change_x=1, change_y=1,
                                  items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorRightBlue(3500, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL),
            DoorLeftYellow(2, 550, self.game, level_dest=2, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(2854, -179, self.game, level_dest=4, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])

        # Add door keys
        self.door_keys.add([
            DoorKeyYellow(2800, 140, self.game, door=[door for door in self.doors if door.is_locked][0]),
            ])
