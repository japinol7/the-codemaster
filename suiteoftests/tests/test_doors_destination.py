"""Module test_doors_destination.
Doors in game levels and test levels must have valid destinations.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[])
def test_doors_in_game_levels_must_have_valid_destinations(game):
    # Load the game levels instead of the test levels
    game.load_game_levels()

    error_msgs = []
    for level in game.levels:
        for door in level.doors:
            if not (0 <= door.level_dest < len(game.levels)):
                error_msgs += [
                    f"list index out of range for door {door.id} in game level {level.id}. "
                    f"Destination level index: {door.level_dest}"
                    ]

    game.assert_test_passed(
        condition=not error_msgs,
        failed_msg=f"Doors in game levels must have valid destinations: {error_msgs}")


@game_test(levels=[1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_doors_in_test_levels_must_have_valid_destinations(game):
    error_msgs = []
    for level in game.levels:
        for door in level.doors:
            if not (0 <= door.level_dest < len(game.levels)):
                error_msgs += [
                    f"list index out of range for door {door.id} in test level {level.id}. "
                    f"Destination level index: {door.level_dest}"
                    ]

    game.assert_test_passed(
        condition=not error_msgs,
        failed_msg=f"Doors in test levels must have valid destinations: {error_msgs}")
