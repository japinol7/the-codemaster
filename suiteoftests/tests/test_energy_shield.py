"""Module test_energy_shield.
Energy shields should protect actors from bullets.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.npcs import SkullYellow, TerminatorEyeRed
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[3], timeout=3)
def test_energy_shield_should_protect_pc_from_bullets(game):
    player = game.player
    player.rect.x, player.rect.y = 240, 620
    player.health, player.power = 22, 100
    game.player.lives = 1

    game.add_player_actions((
        ['acquire_energy_shield', 1],
        ['switch_energy_shield', 1],
        ))

    npc = TerminatorEyeRed(600, 650, game, change_x=0)
    npc.direction = DIRECTION_LEFT
    game.level.add_actors([npc])

    game.game_loop()

    game.assert_test_passed(
        condition=player.lives == 1 and len(player.stats['energy_shields_stock']) > 0,
        failed_msg="NPC killed the player, but they should be protected "
                   "by an energy shield.")

@game_test(levels=[5], timeout=3)
def test_energy_shield_should_protect_npc_from_bullets(game):
    game.player.rect.x, game.player.rect.y = 240, 630
    game.player.stats['bullets_t03'] = 10

    game.add_player_actions((
        ['shot_bullet_t3_photonic', 10],
        ))

    npc = SkullYellow(600, 674, game, change_x=0)
    npc.direction = DIRECTION_LEFT
    game.level.add_actors([npc])

    EnergyShield.actor_acquire_energy_shield(npc, game, health_total=200)
    npc.stats.energy_shield.activate()

    game.game_loop()

    game.assert_test_passed(
        condition=npc.alive(),
        failed_msg="Player killed NPC, but it should be protected by an energy shield.")
