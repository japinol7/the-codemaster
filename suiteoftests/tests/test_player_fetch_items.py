"""Module test_player_fetch_items."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.test_suite.game_test import game_test


class TestPlayerFetchItems:
    """Player should be able to fetch items."""

    @game_test(levels=[1], timeout=4)
    def test_fetch_two_apples(self, game):
        game.player.rect.x, game.player.rect.y = 240, 620

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
            condition=game.player.stats['apples'] == 2,
            failed_msg="Player did not fetch 2 apples.")
