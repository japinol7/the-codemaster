"""Module test_npcs_shoot_player."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.npcs import TerminatorEyeRed
from suiteoftests.test_suite.game_test import game_test


class TestNPCsShootPlayer:
    """NPCs should be able to kill a player life when they shoot them with enough bullets."""

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_enough_bullets_must_die(self, game):
        game.player.rect.x, game.player.rect.y = 260, 620
        game.player.health = 22
        game.player.lives = 1

        npc = TerminatorEyeRed(600, 650, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.lives < 1,
            failed_msg="NPC did not kill the player.")
