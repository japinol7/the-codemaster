"""Module test_npcs_shoot_player."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.npcs import TerminatorEyeRed
from codemaster.models.actors.text_msgs import TextMsg
from suiteoftests.test_suite.game_test import game_test


class TestNPCsShootPlayer:
    """NPCs should be able to kill a player life when they shoot them with enough bullets."""

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_enough_bullets_must_die(self, game):
        def player_die_hard_mock():
            if game.player.stats['lives'] < 1:
                return
            game.player.stats['lives'] -= 1
            TextMsg.create("Player DIED! RIP", game, time_in_secs=5)

        game.player.rect.x, game.player.rect.y = 260, 620
        game.player.stats['health'] = 24
        game.player.stats['lives'] = 1

        game.player.die_hard = player_die_hard_mock

        game.add_player_actions((
            ['stop', 1],
            ))

        npc = TerminatorEyeRed(
                600, 650, game, border_left=590, border_right=610,
                change_x=0, items_to_drop=None)
        npc.direction = DIRECTION_LEFT
        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=game.player.stats['lives'] < 1,
            failed_msg="NPC did not kill the player.")