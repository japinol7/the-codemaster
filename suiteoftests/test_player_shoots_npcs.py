"""Module test_player_shoots_npcs."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.config.constants import (
    PLAYER_HEALTH_SUPER_HERO,
    TestMethodWithSetupLevels,
    )
from suiteoftests.test_suite.game_test import GameTest
from codemaster.models.actors.actor_types import ActorType


class TestPlayerShootsNPCs(GameTest):
    """Player should be able to kill NPCs when he shoots them with enough bullets."""

    def add_tests(self, tests):
        tests = (
            TestMethodWithSetupLevels(
                self.test_bat_hit_with_enough_bullets_must_die_and_give_xp,
                level_name_nums=[3], starting_level_n=0, skip=False,
                ),
            )
        super().add_tests(tests)

    def test_bat_hit_with_enough_bullets_must_die_and_give_xp(self, game):
        game.player.rect.x = 240
        game.player.rect.y = 620
        game.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        game.init_clock_timer(time_in_secs=3)

        game.add_player_actions((
            ['shot_bullet_t3_photonic', 15],
            ))

        bat_black = [npc for npc in game.level.npcs if npc.type == ActorType.BAT_BLACK][0]

        game.game_loop()

        game.calc_test_result(
            failed_condition=bat_black.alive(),
            failed_msg="Player did not kill bat.")
