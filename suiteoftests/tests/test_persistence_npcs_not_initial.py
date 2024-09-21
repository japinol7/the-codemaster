"""Module test_persistence_npcs_not_initial.
Tests persistence of the game state regarding the NPCs
not present in each level when the game starts.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.npcs import (
    SkullRed,
    SkullYellow,
    SquirrelA,
    )
from codemaster.models.actors.items.doors import Door
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2, 3], starting_level=2, timeout=3.6)
def test_persist_npcs_not_init_2_levels(game):
    """Tests persistence of NPCs that are not initially present in the game,
    but added dynamically, for two visited levels:
    * One yellow skull.
    * Five squirrels and the player kills two.
    """
    player = game.player
    level_orig = game.levels[2]
    level_dest = game.levels[1]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=1, game=game, level_orig=2)[0]
    left_door.is_locked = False

    # Remove annoying demon from level dest
    level_dest.get_npcs_filtered_by_actor_type(ActorType.DEMON_MALE)[0].kill()

    # Add additional items in the levels
    squirrel1 = SquirrelA(560, 685, game, change_x=0)
    squirrel1.direction = DIRECTION_LEFT
    skull_yellow = SkullYellow(650, 672, game, change_x=0)
    skull_yellow.direction = DIRECTION_LEFT
    squirrel2 = SquirrelA(750, 685, game, change_x=0)
    squirrel2.direction = DIRECTION_LEFT

    level_orig.add_actors([
        skull_yellow,
        squirrel1,
        squirrel2,
        ])

    level_dest.add_actors([
        SquirrelA(2900, 685, game, change_x=0),
        SquirrelA(2960, 685, game, change_x=0),
        SquirrelA(3020, 685, game, change_x=0),
        ])

    # Get orig data to assert
    skulls_yellow_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SKULL_YELLOW)
    squirrels_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    squirrels_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.lives = 2
    player.stats['bullets_t04'] = 2
    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 1],
        ['go_right', 30],
        ['go_left', 60],
        ['shot_bullet_t4_neutronic', 1],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game and delete old variables
    game.persist_game_data()
    del skull_yellow, squirrel1, squirrel2

    # Load previous game
    game.load_game_data()

    # Get data to assert
    skulls_yellow_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SKULL_YELLOW)
    squirrels_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    squirrels_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)

    game.assert_test_passed(
        condition=game.level.id == 2
                  and skulls_yellow_lev_3_count_orig == skulls_yellow_lev_3_count == 1
                  and squirrels_lev_3_count_orig > squirrels_lev_3_count == 1
                  and squirrels_lev_2_count_orig > squirrels_lev_2_count == 2,
        failed_msg="Game loaded did not set the correct state for the "
                   "NPCs tested that were not initially present in the game.")

@game_test(levels=[1, 2, 3], starting_level=2, timeout=3.6)
def test_persist_npcs_dropped_2_levels_skulls(game):
    """Tests persistence of NPCs that are not initially present in the game,
    but added dynamically when dropped by other NPCs,
    for two visited levels:
    * Five squirrels and the player kills two.
    * The two killed squirrels drop one skull each one.
    """
    player = game.player
    level_orig = game.levels[2]
    level_dest = game.levels[1]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=1, game=game, level_orig=2)[0]
    left_door.is_locked = False

    # Remove annoying demon from level dest
    level_dest.get_npcs_filtered_by_actor_type(ActorType.DEMON_MALE)[0].kill()

    # Add additional items in the levels
    items_to_drop = [
        DropItem(SkullRed, y_delta=-16,
                 **{'border_left': 550, 'border_right': 620, 'change_x': 1}),
        ]
    squirrel1 = SquirrelA(560, 685, game, change_x=0, items_to_drop=items_to_drop)
    squirrel1.direction = DIRECTION_LEFT
    squirrel2 = SquirrelA(750, 685, game, change_x=0)
    squirrel2.direction = DIRECTION_LEFT

    level_orig.add_actors([
        squirrel1,
        squirrel2,
        ])

    items_to_drop = [
        DropItem(SkullRed, y_delta=-16,
                 **{'border_left': 2990, 'border_right': 3100, 'change_x': 1}),
        ]
    squirrel3 = SquirrelA(3020, 685, game,change_x=0, items_to_drop=items_to_drop)

    level_dest.add_actors([
        SquirrelA(2900, 685, game, change_x=0),
        SquirrelA(2960, 685, game, change_x=0),
        squirrel3,
        ])

    # Get orig data to assert
    squirrels_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    skulls_red_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SKULL_RED)
    squirrels_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    skulls_red_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SKULL_RED)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.lives = 2
    player.stats['bullets_t04'] = 2
    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 1],
        ['go_right', 30],
        ['go_left', 60],
        ['shot_bullet_t4_neutronic', 1],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game and delete old variables
    game.persist_game_data()
    del squirrel1, squirrel2, squirrel3

    # Load previous game
    game.load_game_data()

    # Get data to assert
    squirrels_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    skulls_red_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SKULL_RED)
    squirrels_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    skulls_red_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SKULL_RED)

    game.assert_test_passed(
        condition=game.level.id == 2
                  and skulls_red_lev_3_count_orig == 0 and skulls_red_lev_3_count == 1
                  and skulls_red_lev_2_count_orig == 0 and skulls_red_lev_2_count == 1
                  and squirrels_lev_3_count_orig > squirrels_lev_3_count == 1
                  and squirrels_lev_2_count_orig > squirrels_lev_2_count == 2,
        failed_msg="Game loaded did not set the correct state for the "
                   "NPCs tested that were dropped in the game.")


@game_test(levels=[1, 2, 3], starting_level=2, timeout=3)
def test_persist_npc_energy_shield_health_not_init(game):
    game.player.rect.x, game.player.rect.y = 240, 620
    game.player.stats['bullets_t03'] = 10

    npc = SkullRed(600, 670, game, change_x=0)
    npc.direction = DIRECTION_LEFT
    game.level.add_actors([npc])

    EnergyShield.actor_acquire_energy_shield(npc, game, health_total=280)
    npc.stats.energy_shield.activate()

    game.add_player_actions((
        ['shot_bullet_t3_photonic', 10],
        ))

    game.game_loop()

    # Save game and delete old variables
    game.persist_game_data()
    del npc

    # Load previous game
    game.load_game_data()

    npc = game.level.get_npcs_filtered_by_actor_type(ActorType.SKULL_RED)[0]
    npc_shield = npc.stats.energy_shield
    game.assert_test_passed(
        condition=npc.alive()
                  and npc_shield
                  and npc_shield.stats.health_total == 280
                  and npc_shield.stats.health < npc_shield.stats.health_total - 50,
        failed_msg="NPC's energy shield health not persisted.")
