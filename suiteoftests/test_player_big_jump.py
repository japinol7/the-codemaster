"""Module test_player_big_jump."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.tools.utils.queue import Queue
from suiteoftests.config.constants import (
    PLAYER_HEALTH_SUPER_HERO,
    TestMethodWithSetupLevels,
    )
from suiteoftests.test_suite.game_test import GameTest


class TestPlayerBigJump(GameTest):
    """Player should be able to reach some distance when he jumps."""

    def add_tests(self, tests):
        tests = (
            TestMethodWithSetupLevels(
                self.test_big_jump_and_fetch_1_file_disk,
                level_name_nums=[1], starting_level_n=0, skip=False,
                ),
            TestMethodWithSetupLevels(
                self.test_big_jump_and_fetch_3_batteries_n_1_disk,
                level_name_nums=[1], starting_level_n=0, skip=False,
                ),
            TestMethodWithSetupLevels(
                self.test_big_jump_and_fetch_1_life_n_7_potions_power,
                level_name_nums=[2], starting_level_n=0, skip=False,
                ),
            )
        super().add_tests(tests)

    def test_big_jump_and_fetch_1_file_disk(self, game):
        game.player.rect.x = 1420
        game.player.rect.y = 620
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.init_clock_timer(time_in_secs=4)

        game.player_actions = Queue((
            ['go_left', 15],
            ['jump', 5],
            ['go_left', 45],
            ['stop', 1],
            ))

        game._game_loop()

        game.calc_test_result(
            failed_condition=game.player.stats['files_disks'] != 1,
            failed_msg="Test FAILED: Player did not fetch 1 disk.",
            test_name=game.current_test.__name__)

    def test_big_jump_and_fetch_3_batteries_n_1_disk(self, game):
        game.player.rect.x = 1500
        game.player.rect.y = 50
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.init_clock_timer(time_in_secs=5)

        game.player_actions = Queue((
            ['go_right', 22],
            ['jump', 5],
            ['go_right', 192],
            ['stop', 1],
            ))

        game._game_loop()

        game.calc_test_result(
            failed_condition=game.player.stats['batteries'] < 3 or game.player.stats['files_disks'] < 1,
            failed_msg="Test FAILED: Player did not fetch at least 3 batteries and 1 disk.",
            test_name=game.current_test.__name__)

    def test_big_jump_and_fetch_1_life_n_7_potions_power(self, game):
        def player_die_hard_mock():
            game.player.stats['lives'] -= 1
            game.player.stop()
            game.player_actions = []

        game.player.rect.x = 3000
        game.player.rect.y = 500
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO
        game.player.stats['lives'] = 3

        game.player.die_hard = player_die_hard_mock

        game.init_clock_timer(time_in_secs=4)

        game.player_actions = Queue((
            ['go_left', 22],
            ['jump', 5],
            ['go_left', 64],
            ['go_right', 12],
            ['jump', 5],
            ['go_right', 78],
            ['stop', 1],
            ))

        game._game_loop()

        game.calc_test_result(
            failed_condition=game.player.stats['lives'] < 4 or len(game.player.stats['potions_power']) < 7,
            failed_msg="Test FAILED: Player did not fetch at least 1 life recovery and 7 potions_power.",
            test_name=game.current_test.__name__)
