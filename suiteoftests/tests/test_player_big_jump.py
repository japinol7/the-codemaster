"""Module test_player_big_jump."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.config.constants import PLAYER_HEALTH_SUPER_HERO
from suiteoftests.test_suite.game_test import game_test


class TestPlayerBigJump:
    """Player should be able to reach some distance when he jumps."""

    @game_test(levels=[2], timeout=3)
    def test_big_jump_and_fetch_1_file_disk(self, game):
        game.player.rect.x, game.player.rect.y = 1420, 620
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.add_player_actions((
            ['go_left', 15],
            ['jump', 5],
            ['go_left', 45],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['files_disks'] == 1,
            failed_msg="Player did not fetch 1 disk.")

    @game_test(levels=[2], timeout=4)
    def test_big_jump_and_fetch_3_batteries_n_1_disk(self, game):
        game.player.rect.x, game.player.rect.y = 1500, 50
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.add_player_actions((
            ['go_right', 22],
            ['jump', 5],
            ['go_right', 192],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['batteries'] >= 3 and game.player.stats['files_disks'] >= 1,
            failed_msg="Player did not fetch at least 3 batteries and 1 disk.")

    @game_test(levels=[3], timeout=4)
    def test_big_jump_and_fetch_1_life_n_7_potions_power(self, game):
        def player_die_hard_mock():
            game.player.stats['lives'] -= 1
            game.player.stop()
            game.player_actions = []

        game.player.rect.x, game.player.rect.y = 3000, 500
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.player.die_hard = player_die_hard_mock

        game.add_player_actions((
            ['go_left', 22],
            ['jump', 5],
            ['go_left', 64],
            ['go_right', 12],
            ['jump', 5],
            ['go_right', 78],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['lives'] >= 4 and len(game.player.stats['potions_power']) == 7,
            failed_msg="Player did not fetch at least 1 life recovery and 7 potions_power.")

    @game_test(levels=[5], timeout=4)
    def test_big_jump_and_fetch_2_disks(self, game):
        def player_die_hard_mock():
            game.player.stats['lives'] -= 1
            game.player.stop()
            game.player_actions = []

        game.player.rect.x, game.player.rect.y = 1020, 600
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.player.die_hard = player_die_hard_mock

        game.add_player_actions((
            ['go_right', 10],
            ['jump', 5],
            ['go_right', 64],
            ['jump', 5],
            ['go_right', 60],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['files_disks'] == 2,
            failed_msg="Player did not fetch 2 disks.")

    @game_test(levels=[5], timeout=3)
    def test_big_jump_too_high_should_fail(self, game):
        def player_die_hard_mock():
            game.player.stats['lives'] -= 1
            game.player.stop()
            game.player_actions = []

        game.player.rect.x, game.player.rect.y = 1850, 400
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.player.die_hard = player_die_hard_mock

        game.add_player_actions((
            ['go_right', 10],
            ['jump', 5],
            ['go_right', 65],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['apples'] == 0,
            failed_msg="Player should not be able to jump that high. "
                       "Fetching the 2 apples should fail.")
