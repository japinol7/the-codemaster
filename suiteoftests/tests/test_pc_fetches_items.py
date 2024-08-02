"""Module test_pc_fetches_items."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.items import (
    AppleYellow,
    AppleRed,
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    LifeRecoveryA,
    )
from suiteoftests.test_suite.game_test import game_test


class TestPlayerFetchesItems:
    """Player should be able to fetch items."""

    @game_test(levels=[4], timeout=2)
    def test_pc_fetches_three_batteries(self, game):
        player = game.player
        player.rect.x, player.rect.y = 906, 640
        player.stats['batteries'] = 0

        game.add_player_actions((
            ['go_right', 60],
            ['stop', 1],
            ))

        game.level.add_actors((
            BatteryA(1042, 702, game),
            BatteryA(1082, 702, game),
            BatteryA(1122, 702, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=player.stats['batteries'] == 3,
            failed_msg="Player did not fetch 3 batteries.")

    @game_test(levels=[1], timeout=2)
    def test_pc_fetches_two_apples(self, game):
        player = game.player
        player.rect.x, player.rect.y = 706, 640
        player.stats['apples'] = 0

        game.add_player_actions((
            ['go_right', 60],
            ['stop', 1],
            ))

        game.level.add_actors((
            AppleYellow(842, 712, game),
            AppleRed(940, 712, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=player.stats['apples'] == 2 and len(player.stats['apples_stock']) == 2,
            failed_msg="Player did not fetch 2 apples.")

    @game_test(levels=[3], timeout=2)
    def test_pc_fetches_cartridge_with_bullets_t1(self, game):
        player = game.player
        player.rect.x, player.rect.y = 706, 640
        game.player.stats['bullets_t01'] = 5

        game.add_player_actions((
            ['go_right', 60],
            ['stop', 1],
            ))

        game.level.add_actors((
            CartridgeGreen(842, 702, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['bullets_t01'] > 5,
            failed_msg="Player did not fetch cartridge with bullets t1.")

    @game_test(levels=[3], timeout=2)
    def test_pc_fetches_cartridge_with_bullets_t2(self, game):
        player = game.player
        player.rect.x, player.rect.y = 706, 640
        game.player.stats['bullets_t02'] = 5

        game.add_player_actions((
            ['go_right', 60],
            ['stop', 1],
            ))

        game.level.add_actors((
            CartridgeBlue(842, 702, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['bullets_t02'] > 5,
            failed_msg="Player did not fetch cartridge with bullets t2.")

    @game_test(levels=[4], timeout=2)
    def test_pc_fetches_cartridge_with_bullets_t3(self, game):
        player = game.player
        player.rect.x, player.rect.y = 706, 640
        game.player.stats['bullets_t03'] = 5

        game.add_player_actions((
            ['go_right', 60],
            ['stop', 1],
            ))

        game.level.add_actors((
            CartridgeYellow(842, 702, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['bullets_t03'] > 5,
            failed_msg="Player did not fetch cartridge with bullets t3.")

    @game_test(levels=[3], timeout=2)
    def test_pc_fetches_cartridge_with_bullets_t4(self, game):
        player = game.player
        player.rect.x, player.rect.y = 706, 640
        game.player.stats['bullets_t04'] = 5

        game.add_player_actions((
            ['go_right', 60],
            ['stop', 1],
            ))

        game.level.add_actors((
            CartridgeRed(842, 702, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['bullets_t04'] > 5,
            failed_msg="Player did not fetch cartridge with bullets t4.")

    @game_test(levels=[1], timeout=2)
    def test_pc_fetches_life(self, game):
        player = game.player
        player.rect.x, player.rect.y = 110, 355
        game.player.lives = 1

        game.add_player_actions((
            ['go_right', 50],
            ['stop', 1],
            ))

        game.level.add_actors((
            LifeRecoveryA(250, 402, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.lives == 2,
            failed_msg="Player did not fetch a life.")
