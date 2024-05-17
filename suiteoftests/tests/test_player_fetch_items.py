"""Module test_player_fetch_items."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.config.constants import PLAYER_HEALTH_SUPER_HERO
from suiteoftests.test_suite.game_test import game_test


class TestPlayerFetchItems:
    """Player should be able to fetch items."""

    @game_test(levels=[1])
    def test_fetch_two_apples(self, game):
        game.player.rect.x = 240
        game.player.rect.y = 620
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.init_clock_timer(time_in_secs=4)

        game.add_player_actions((
            ['go_right', 34],
            ['jump', 5],
            ['go_right', 148],
            ['stop', 1],
            ['go_left', 4],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            pass_condition=game.player.stats['apples'] == 2,
            failed_msg="Player did not fetch 2 apples.")
