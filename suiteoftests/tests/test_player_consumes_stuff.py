"""Module test_player_consumes_stuff."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.items import (
    AppleRed,
    PotionHealth,
    PotionPower,
    )
from suiteoftests.test_suite.game_test import game_test


class TestPlayerConsumesStuff:
    """Player should be able to consume items and receiving the items' perks."""

    @game_test(levels=[2], timeout=2)
    def test_player_drinks_health_potion(self, game):
        game.player.rect.x, game.player.rect.y = 760, 640
        game.player.health = 10

        game.add_player_actions((
            ['go_right', 20],
            ['drink_potion_health', 1],
            ['stop', 1],
            ))

        game.level.add_actors((
            PotionHealth(880, 708, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.health > 10,
            failed_msg="Player did not get health after fetching and drinking a health potion.")

    @game_test(levels=[2], timeout=2)
    def test_player_drinks_power_potion(self, game):
        game.player.rect.x, game.player.rect.y = 760, 640
        game.player.power = 10

        game.add_player_actions((
            ['go_right', 20],
            ['drink_potion_power', 1],
            ['stop', 1],
            ))

        game.level.add_actors((
            PotionPower(880, 708, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.power > 10,
            failed_msg="Player did not get power after fetching and drinking a power potion.")

    @game_test(levels=[1], timeout=2)
    def test_player_eats_apple(self, game):
        game.player.rect.x, game.player.rect.y = 790, 640
        game.player.health = 10

        game.add_player_actions((
            ['go_right', 26],
            ['eat_apple', 1],
            ['stop', 1],
            ))

        game.level.add_actors((
            AppleRed(880, 712, game),
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.health > 10,
            failed_msg="Player must fetch an apple, eat it and recover some health.")
