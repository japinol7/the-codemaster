"""Module test_player_shoots_npcs."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actor_types import ActorType
from suiteoftests.test_suite.game_test import game_test


class TestPlayerShootsNPCs:
    """Player should be able to kill NPCs when he shoots them with enough bullets."""

    @game_test(levels=[3], timeout=2)
    def test_pc_must_spend_power_and_bullets_to_shoot(self, game):
        player = game.player
        player.rect.x, player.rect.y = 240, 620
        player.power = 100
        player.stats['bullets_t03'] = 15

        game.add_player_actions((
            ['shot_bullet_t3_photonic', 15],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=player.power < 100 and player.stats['bullets_t03'] == 0,
            failed_msg="Player must spend power and bullets to shoot bullets.")

    @game_test(levels=[4], timeout=3)
    def test_bat_hit_with_enough_bullets_must_die(self, game):
        game.player.rect.x, game.player.rect.y = 240, 620

        game.add_player_actions((
            ['shot_bullet_t3_photonic', 15],
            ))

        bat_black = [npc for npc in game.level.npcs if npc.type == ActorType.BAT_BLACK][0]

        game.game_loop()

        game.assert_test_passed(
            condition=not bat_black.alive(),
            failed_msg="Player did not kill bat.")
