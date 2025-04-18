"""Module test_npcs_drop_items.
NPCs should drop items when killed.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import (
    CartridgeGreen,
    CartridgeYellow,
    CartridgeRed,
    )
from codemaster.models.actors.npcs import (
    BatBlack,
    PumpkinHeadA,
    PumpkinZombieA,
    SkullRed,
    WolfManMale,
    )
from suiteoftests.config.constants import PLAYER_HEALTH_SUPER_HERO
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[3], timeout=3)
def test_npc_drops_green_cartridge_when_dies(game):
    level = game.level
    player = game.player
    player.rect.x, player.rect.y = 260, 620
    player.health = PLAYER_HEALTH_SUPER_HERO
    player.power = 100
    player.stats['bullets_t04'] = 7

    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 7],
        ))

    item_to_drop = DropItem(CartridgeGreen)
    npc = WolfManMale(600, 665, game, change_x=0, items_to_drop=[item_to_drop])
    npc.direction = DIRECTION_LEFT
    level.add_actors([npc])

    game.game_loop()

    cartridge_count = level.count_items_filtered_by_actor_type(ActorType.CARTRIDGE_GREEN)

    game.assert_test_passed(
        condition=cartridge_count == 1,
        failed_msg="NPC must drop a green cartridge.")

@game_test(levels=[1], timeout=3)
def test_npc_drops_2_red_cartridges_when_dies(game):
    level = game.level
    player = game.player
    player.rect.x, player.rect.y = 260, 632
    player.health = PLAYER_HEALTH_SUPER_HERO
    player.power = 100
    player.stats['bullets_t04'] = 6

    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 6],
        ))

    items_to_drop = [
        DropItem(CartridgeRed, y_delta=-4),
        DropItem(CartridgeRed, y_delta=36),
        ]
    npc = SkullRed(600, 668, game, change_x=0, items_to_drop=items_to_drop)
    npc.direction = DIRECTION_LEFT
    level.add_actors([npc])

    game.game_loop()

    cartridge_count = level.count_items_filtered_by_actor_type(ActorType.CARTRIDGE_RED)

    game.assert_test_passed(
        condition=cartridge_count == 2,
        failed_msg="NPC must drop 2 red cartridges.")

@game_test(levels=[3], timeout=3)
def test_npc_drops_pumpkin_n_yellow_cartridge_when_dies(game):
    level = game.level
    player = game.player
    player.rect.x, player.rect.y = 260, 620
    player.health = PLAYER_HEALTH_SUPER_HERO
    player.power = 100
    player.stats['bullets_t04'] = 8

    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 8],
        ))

    items_to_drop = [
        DropItem(CartridgeYellow, x_delta=26, y_delta=-35),
        DropItem(PumpkinHeadA, y_delta=15),
        ]
    npc = PumpkinZombieA(600, 648, game, change_x=0, items_to_drop=items_to_drop)
    npc.direction = DIRECTION_LEFT
    npc.can_shot = False
    npc.can_cast_spells = False

    level.add_actors([npc])

    game.game_loop()

    pumpkin_count = level.count_npcs_filtered_by_actor_type(ActorType.PUMPKIN_HEAD_A)
    cartridge_count = level.count_items_filtered_by_actor_type(ActorType.CARTRIDGE_YELLOW)

    game.assert_test_passed(
        condition=pumpkin_count == 1 and cartridge_count == 1,
        failed_msg="NPC must drop a pumpkin head and a yellow cartridge.")

@game_test(levels=[3], timeout=3)
def test_npc_drops_npc_that_drops_black_bat_when_dies(game):
    level = game.level
    player = game.player
    player.rect.x, player.rect.y = 260, 620
    player.health = PLAYER_HEALTH_SUPER_HERO
    player.power = 200
    player.stats['bullets_t04'] = 16

    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 8],
        ['stop', 22],
        ['shot_bullet_t4_neutronic', 3],
        ['stop', 20],
        ['shot_bullet_t4_neutronic', 4],
        ))

    item_to_drop = DropItem(BatBlack, x_delta=-8, y_delta=5)
    items_to_drop = [
        DropItem(CartridgeYellow, x_delta=26, y_delta=-35),
        DropItem(PumpkinHeadA, y_delta=15, items_to_drop=[item_to_drop]),
        ]
    npc = PumpkinZombieA(600, 648, game, change_x=0, items_to_drop=items_to_drop)
    npc.direction = DIRECTION_LEFT
    npc.can_shot = False
    npc.can_cast_spells = False

    level.add_actors([npc])

    game.game_loop()

    pumpkin_count = level.count_npcs_filtered_by_actor_type(ActorType.PUMPKIN_HEAD_A)
    black_bat_count = level.count_npcs_filtered_by_actor_type(ActorType.BAT_BLACK)
    cartridge_count = level.count_items_filtered_by_actor_type(ActorType.CARTRIDGE_YELLOW)

    game.assert_test_passed(
        condition=pumpkin_count == 0
                  and cartridge_count == 1
                  and black_bat_count == 1,
        failed_msg="NPC must drop a pumpkin head and a yellow cartridge. "
                   "Also, the pumpkin head must drop a black bat.")
