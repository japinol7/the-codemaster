"""Module test_pc_enters_door_level.
The player should be able to enter a door to go to another level
only if the door is open.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actor_types import ActorType
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2], starting_level=1, timeout=2)
def test_pc_enters_door_to_another_level(game):
    game.player.rect.x, game.player.rect.y = 250, 660

    game.add_player_actions((
        ['go_left', 50],
        ['stop', 1],
        ))

    left_door = [door for door in game.level.doors
                 if door.type == ActorType.DOOR_LEFT_GREEN][0]
    left_door.is_locked = False

    game.game_loop()

    game.assert_test_passed(
        condition=game.level.id == 1,
        failed_msg="Player did not go to another level through an open door.")

@game_test(levels=[1, 2], starting_level=1, timeout=2)
def test_pc_cannot_enter_locked_door_to_another_level(game):
    game.player.rect.x, game.player.rect.y = 250, 660

    game.add_player_actions((
        ['go_left', 50],
        ['stop', 1],
        ))

    left_door = [door for door in game.level.doors
                 if door.type == ActorType.DOOR_LEFT_GREEN][0]
    left_door.is_locked = True

    game.game_loop()

    game.assert_test_passed(
        condition=game.level.id == 2,
        failed_msg="Player did go to another level through a locked door.")
