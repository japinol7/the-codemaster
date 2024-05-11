"""Module test_player_fetch_items."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.tools.utils.queue import Queue
from suiteoftests.config.constants import (
    PLAYER_HEALTH_SUPER_HERO,
    TestMethodWithSetupLevels,
    )
from suiteoftests.test_suite.game_test import GameTest


class TestPlayerFetchItems(GameTest):
    """Player should be able to fetch items."""

    def add_tests(self, tests):
        tests = (
            TestMethodWithSetupLevels(
                self.test_fetch_two_apples,
                level_name_nums=[1], starting_level_n=0, skip=False,
                ),
            )
        super().add_tests(tests)

    def test_fetch_two_apples(self, game):
        game.player.rect.x = 240
        game.player.rect.y = 620
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.init_clock_timer(time_in_secs=4)

        game.player_actions = Queue((
            ['go_right', 34],
            ['jump', 5],
            ['go_right', 148],
            ['stop', 1],
            ['go_left', 4],
            ['stop', 1],
            ))

        game._game_loop()

        game.calc_test_result(
            failed_condition=game.player.stats['apples'] != 2,
            failed_msg="Test FAILED: Player did not fetch 2 apples.",
            test_name=game.current_test.__name__)
