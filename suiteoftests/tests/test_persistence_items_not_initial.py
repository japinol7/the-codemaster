"""Module test_persistence_items_not_initial.
Tests persistence of the game state regarding the items
not present in each level when the game starts.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import (
    LifeRecoveryA,
    PotionHealth,
    PotionPower,
    )
from codemaster.models.actors.npcs import (
    SquirrelA,
    )
from codemaster.models.actors.items.doors import Door
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2, 3], starting_level=2, timeout=3.6)
def test_persist_itens_not_init_2_levels(game):
    """Tests persistence of items that are not initially present in the game,
    but added dynamically, for two visited levels:
    * Two health potions and the player takes one.
    * Two life recovery items and the player takes one.
    """
    player = game.player
    level_orig = game.levels[2]
    level_dest = game.levels[1]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=1, game=game, level_orig=2)[0]
    left_door.is_locked = False

    # Add additional items in the levels
    level_orig.add_actors([
        LifeRecoveryA(560, 692, game),
        LifeRecoveryA(720, 692, game),
        ])
    level_dest.add_actors([
        PotionHealth(3045, 700, game),
        PotionHealth(3150, 700, game),
        ])

    # Remove annoying demon from level dest
    level_dest.get_npcs_filtered_by_actor_type(ActorType.DEMON_MALE)[0].kill()

    # Get orig data to assert
    life_recs_lev_3_count_orig = level_orig.count_actors_in_group_filtered_by_actor_type(
        ActorType.LIFE_RECOVERY, level_orig.life_recs)
    potion_health_lev_2_count_orig = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_HEALTH, level_dest.potions)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.lives = 2
    game.add_player_actions((
        ['go_right', 54],
        ['go_left', 102],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game
    game.persist_game_data()

    # Load previous game
    game.load_game_data()

    # Get data to assert
    life_recs_lev_3_count = level_orig.count_actors_in_group_filtered_by_actor_type(
        ActorType.LIFE_RECOVERY, level_orig.life_recs)
    potion_health_lev_2_count = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_HEALTH, level_dest.potions)

    game.assert_test_passed(
        condition=game.level.id == 2
                  and life_recs_lev_3_count_orig > life_recs_lev_3_count == 2
                  and player.lives == 3
                  and potion_health_lev_2_count_orig > potion_health_lev_2_count == 1,
        failed_msg="Game loaded did not set the correct state for the "
                   "items tested that were not initially present in the game.")

@game_test(levels=[1, 2, 3], starting_level=2, timeout=3.2)
def test_persist_items_dropped_2_levels_potions(game):
    """Tests persistence of items that are not initially present in the game,
    but added dynamically when dropped by other NPCs,
    for two visited levels:
    * Five squirrels and the player kills two.
    * The two killed squirrels drop one potion of power each one.
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
        DropItem(PotionPower, y_delta=15, **{'random_min': 50, 'random_max': 50}),
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
        DropItem(PotionPower, y_delta=15, **{'random_min': 50, 'random_max': 50}),
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
    potion_power_lev_3_count_orig = level_orig.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_orig.potions)
    squirrels_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    potion_power_lev_2_count_orig = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_dest.potions)

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
    potion_power_lev_3_count = level_orig.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_orig.potions)
    squirrels_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    potion_power_lev_2_count = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_dest.potions)

    game.assert_test_passed(
        condition=game.level.id == 2
                  and potion_power_lev_3_count_orig == 6 and potion_power_lev_3_count == 7
                  and potion_power_lev_2_count_orig == 0 and potion_power_lev_2_count == 1
                  and squirrels_lev_3_count_orig > squirrels_lev_3_count == 1
                  and squirrels_lev_2_count_orig > squirrels_lev_2_count == 2,
        failed_msg="Game loaded did not set the correct state for the "
                   "items tested that were dropped in the game.")
