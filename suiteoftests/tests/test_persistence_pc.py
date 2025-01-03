"""Module test_persistence_pc.
Tests persistence of the game state regarding the player.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.items.doors import Door
from codemaster.models.actors.npcs import TerminatorEyeRed
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2], starting_level=1, timeout=2)
def test_persist_pc_go_to_another_level(game):
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=0, game=game, level_orig=1)[0]
    left_door.is_locked = False

    # Go to another level
    game.player.rect.x, game.player.rect.y = 250, 660
    game.add_player_actions((
        ['go_left', 50],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game
    game.persist_game_data()

    # Load previous game
    game.load_game_data()
    game.game_loop(timeout=1.5)

    game.assert_test_passed(
        condition=game.level.id == 1,
        failed_msg="Game loaded did not set the player to the correct level.")

@game_test(levels=[1, 2], starting_level=1, timeout=2)
def test_persist_pc_go_to_another_level_n_more(game):
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=0, game=game, level_orig=1)[0]
    left_door.is_locked = False

    # Go to another level
    game.player.rect.x, game.player.rect.y = 250, 660
    game.add_player_actions((
        ['go_left', 50],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game
    game.persist_game_data()

    # Go to the previous level without saving the game
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=1, game=game, level_orig=0)[0]
    left_door.is_locked = False
    game.add_player_actions((
        ['go_right', 50],
        ['stop', 1],
        ))
    game.game_loop()

    # Load previous game
    game.load_game_data()
    game.game_loop(timeout=1.5)

    game.assert_test_passed(
        condition=game.level.id == 1,
        failed_msg="Game loaded did not set the player to the correct level.")

@game_test(levels=[1, 2, 3], starting_level=1, timeout=2)
def test_persist_pc_basic_stats(game):
    """Tests persistence of basic stats.
    Loads three levels, the player visits two.
    """
    player = game.player
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=0, game=game, level_orig=1)[0]
    left_door.is_locked = False

    # Go to another level
    player.rect.x, player.rect.y = 250, 660
    player.lives = 2
    player.health = 70
    player.power = 60
    player.score = 6000
    player.stats['bullets_t01'] = 50
    player.stats['bullets_t02'] = 30
    player.stats['bullets_t03'] = 10
    player.stats['bullets_t04'] = 6
    game.add_player_actions((
        ['go_left', 50],
        ['stop', 1],
        ))
    game.game_loop()
    player_rect_x, player_rect_y = player.rect.x, player.rect.y

    # Save game
    game.persist_game_data()

    # Load previous game
    game.load_game_data()

    game.assert_test_passed(
        condition=game.level.id == 1
                  and player.rect.x == player_rect_x
                  and player.rect.y == player_rect_y
                  and player.direction == DIRECTION_LEFT
                  and player.lives == 2
                  and player.health == 70
                  and player.power == 60
                  and player.score == 6000
                  and player.stats['bullets_t01'] == 50
                  and player.stats['bullets_t02'] == 30
                  and player.stats['bullets_t03'] == 10
                  and player.stats['bullets_t04'] == 6
                  and sorted(list(player.stats['levels_visited'])) == [1, 2]
                  and sorted(list(game.level.levels_completed_ids(game))) == [],
        failed_msg="Game loaded did not set the player correct basic stats.")


@game_test(levels=[1, 2, 3], starting_level=2, timeout=3)
def test_persist_pc_energy_shield_health(game):
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

    # Save game and delete old variables
    game.persist_game_data()
    del npc

    # Load previous game
    game.load_game_data()

    pc_shields = player.stats['energy_shields_stock']
    pc_shield = pc_shields[0] if pc_shields else None
    game.assert_test_passed(
        condition=player.lives == 1
                  and pc_shield
                  and pc_shield.stats.health < pc_shield.stats.health_total - 10
                  and len(player.stats['energy_shields_stock']) > 0,
        failed_msg="Player's energy shield health not persisted.")
