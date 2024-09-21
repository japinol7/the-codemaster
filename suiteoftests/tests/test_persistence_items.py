"""Module test_persistence_items.
Tests persistence of the game state regarding the items
present in each level when the game starts.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.items.doors import Door
from codemaster.models.actors.npcs import TerminatorEyeRed
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2, 3, 4], starting_level=3, timeout=3.6)
def test_persist_itens_2_levels_potions_n_get_life_rec(game):
    """Tests persistence of items for two visited levels:
    Some health potions, six power potions, and a life recovery.
    PC gets the life recovery.
    """
    player = game.player
    level_orig = game.levels[3]
    level_dest = game.levels[2]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=2, game=game, level_orig=3)[0]
    left_door.is_locked = False

    # Get orig data to assert
    life_recs_lev_4_count_orig = level_orig.count_actors_in_group_filtered_by_actor_type(
        ActorType.LIFE_RECOVERY, level_orig.life_recs)
    potion_health_lev_3_count_orig = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_HEALTH, level_dest.potions)
    potion_power_lev_3_count_orig = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_dest.potions)

    # Do actions, go to another level and save the game
    player.rect.x, player.rect.y = 250, 650
    player.lives = 2
    player.power = 100
    game.add_player_actions((
        ['go_right', 56],
        ['go_left', 84],
        ['stop', 1],
        ))
    game.game_loop()
    game.persist_game_data()

    # Load previous game
    game.load_game_data()

    # Get data to assert
    life_recs_lev_4_count = level_orig.count_actors_in_group_filtered_by_actor_type(
        ActorType.LIFE_RECOVERY, level_orig.life_recs)
    potion_health_lev_3_count = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_HEALTH, level_dest.potions)
    potion_power_lev_3_count = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_dest.potions)

    game.assert_test_passed(
        condition=game.level.id == 3
                  and life_recs_lev_4_count_orig > life_recs_lev_4_count == 0
                  and player.lives == 3
                  and potion_health_lev_3_count_orig == potion_health_lev_3_count == 2
                  and potion_power_lev_3_count_orig == potion_power_lev_3_count == 6,
        failed_msg="Game loaded did not set the correct state for the items tested.")

@game_test(levels=[1, 2, 3, 4], starting_level=3, timeout=2.5)
def test_persist_itens_2_levels_shot_n_get_1_potion(game):
    """Tests persistence of items for two visited levels:
    Some health potions, six power potions, a life recovery,
    and bullets t1 qnd t2.
    PC gets one health potion and the life recovery, and shots some t1 bullets.
    """
    player = game.player
    level_dest = game.levels[2]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=2, game=game, level_orig=3)[0]
    left_door.is_locked = False

    # Get orig data to assert
    potion_health_lev_3_count_orig = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_HEALTH, level_dest.potions)
    potion_power_lev_3_count_orig = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_dest.potions)

    # Do actions, go to another level and save the game
    player.rect.x, player.rect.y = 250, 650
    player.power = 100
    player.stats['bullets_t01'] = 14
    player.stats['bullets_t02'] = 5
    game.add_player_actions((
        ['shot_bullet_t1_laser1', 10],
        ['go_left', 48],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game and delete old variables
    game.persist_game_data()
    del player, level_dest

    # Load previous game
    game.load_game_data()
    player = game.player
    level_dest = game.levels[2]

    # Get data to assert
    potion_health_lev_3_count = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_HEALTH, level_dest.potions)
    potion_power_lev_3_count = level_dest.count_actors_in_group_filtered_by_actor_type(
        ActorType.POTION_POWER, level_dest.potions)

    game.assert_test_passed(
        condition=game.level.id == 3
                  and player.stats['bullets_t01'] == 4
                  and player.stats['bullets_t02'] == 5
                  and player.power < 100
                  and potion_health_lev_3_count_orig > potion_health_lev_3_count == 1
                  and potion_power_lev_3_count_orig == potion_power_lev_3_count == 6,
        failed_msg="Game loaded did not set the correct state for the items tested.")


@game_test(levels=[1, 2, 3], starting_level=2, timeout=3)
def test_persist_energy_shield_health_of_npc_not_init(game):
    player = game.player
    player.rect.x, player.rect.y = 240, 620
    player.health, player.power = 22, 100
    game.player.lives = 1

    game.add_player_actions((
        ['acquire_energy_shield', 1],
        ['switch_energy_shield', 1],
        ))

    npc = TerminatorEyeRed(600, 650, game, change_x=0)
    npc.direction = DIRECTION_LEFT
    game.level.add_actors([npc])

    game.game_loop()
    player.stats['level'] = 2

    # Save game
    game.persist_game_data()

    # Load previous game
    game.load_game_data()

    pc_shields = player.stats['energy_shields_stock']
    pc_shield = pc_shields[0] if pc_shields else None
    game.assert_test_passed(
        condition=player.lives == 1
                  and pc_shield
                  and pc_shield.stats.health < pc_shield.stats.health_total - 10
                  and len(player.stats['energy_shields_stock']) > 0,
        failed_msg="NPC killed the player, but they should be protected by an energy shield.")
