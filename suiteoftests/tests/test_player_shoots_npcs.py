"""Module test_player_shoots_npcs."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actor_types import ActorType
from suiteoftests.config.constants import PLAYER_HEALTH_SUPER_HERO
from suiteoftests.test_suite.game_test import game_test


class TestPlayerShootsNPCs:
    """Player should be able to kill NPCs when he shoots them with enough bullets."""

    @game_test(levels=[4])
    def test_bat_hit_with_enough_bullets_must_die(self, game):
        game.player.rect.x = 240
        game.player.rect.y = 620
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.init_clock_timer(time_in_secs=3)

        game.add_player_actions((
            ['shot_bullet_t3_photonic', 15],
            ))

        bat_black = [npc for npc in game.level.npcs if npc.type == ActorType.BAT_BLACK][0]

        game.game_loop()

        game.assert_test_passed(
            pass_condition=not bat_black.alive(),
            failed_msg="Player did not kill bat.")