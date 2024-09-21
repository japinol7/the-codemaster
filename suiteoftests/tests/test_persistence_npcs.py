"""Module test_persistence_npcs.
Tests persistence of the game state regarding the items
present in each level when the game starts.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.items.doors import Door
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2, 3, 4], starting_level=3, timeout=3.6)
def test_persist_npcs_2_levels_kill_bat(game):
    """Tests persistence of NPCs for two visited levels:
    PC shoots a bat to death.
    """
    player = game.player
    level_orig = game.levels[3]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=2, game=game, level_orig=3)[0]
    left_door.is_locked = False

    # Get orig data to assert
    bat_blacks_lev_4_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.BAT_BLACK)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.power = 100
    player.stats['bullets_t04'] = 12
    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 12],
        ['go_right', 20],
        ['go_left', 45],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game
    game.persist_game_data()

    # Load previous game
    game.load_game_data()

    # Get data to assert
    bat_blacks_lev_4_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.BAT_BLACK)

    game.assert_test_passed(
        condition=game.level.id == 3
                  and bat_blacks_lev_4_count_orig > bat_blacks_lev_4_count == 0,
        failed_msg="Game loaded did not set the correct state for the NPCs tested.")

@game_test(levels=[1, 2, 3, 4], starting_level=3, timeout=3.6)
def test_persist_npcs_2_levels_hurt_bat(game):
    """Tests persistence of NPCs for two visited levels:
    PC shoots a bat, but only hurts it.
    """
    player = game.player
    level_orig = game.levels[3]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=2, game=game, level_orig=3)[0]
    left_door.is_locked = False

    # Get orig data to assert
    bat_blacks_lev_4_orig = level_orig.get_npcs_filtered_by_actor_type(
        ActorType.BAT_BLACK)
    bat_blacks_lev_4_count_orig = len(bat_blacks_lev_4_orig)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.power = 100
    player.stats['bullets_t01'] = 10
    game.add_player_actions((
        ['shot_bullet_t1_laser1', 10],
        ['go_right', 20],
        ['go_left', 45],
        ['stop', 1],
        ))
    game.game_loop()
    bat_black_orig_health_after_shoot = bat_blacks_lev_4_orig[0].health

    # Save game
    game.persist_game_data()

    # Load previous game
    game.load_game_data()

    # Get data to assert
    bat_blacks_lev_4 = level_orig.get_npcs_filtered_by_actor_type(
        ActorType.BAT_BLACK)
    bat_blacks_lev_4_count = len(bat_blacks_lev_4)

    game.assert_test_passed(
        condition=game.level.id == 3
                  and bat_black_orig_health_after_shoot == bat_blacks_lev_4[0].health
                  and bat_blacks_lev_4[0].health < bat_blacks_lev_4[0].stats.health_total
                  and bat_blacks_lev_4_count_orig == bat_blacks_lev_4_count == 1,
        failed_msg="Game loaded did not set the correct state for the NPCs tested.")
