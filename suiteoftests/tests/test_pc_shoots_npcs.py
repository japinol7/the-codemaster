"""Module test_pc_shoots_npcs.
The player should be able to kill NPCs when he shoots them
with enough bullets.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import SquirrelA
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[3], timeout=2)
def test_pc_must_spend_power_and_bullets_to_shoot(game):
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

@game_test(levels=[8], timeout=3)
def test_bat_hit_with_enough_bullets_must_die(game):
    player = game.player
    player.rect.x, player.rect.y = 240, 620
    player.power = 100
    player.stats['bullets_t03'] = 16

    game.add_player_actions(('shot_bullet_t3_photonic', 8) for _ in range(2))

    bat_black = [npc for npc in game.level.npcs if npc.type == ActorType.BAT_BLACK][0]

    game.game_loop()

    game.assert_test_passed(
        condition=not bat_black.alive(),
        failed_msg="Player did not kill bat.")

@game_test(levels=[3], timeout=2)
def test_squirrel_hit_with_enough_bullets_must_die(game):
    player = game.player
    player.rect.x, player.rect.y = 240, 662
    player.power = 100
    player.stats['bullets_t02'] = 2

    npc = SquirrelA(600, 686, game, change_x=0)
    npc.direction = DIRECTION_LEFT
    game.level.add_actors([npc])

    game.add_player_actions((
        ['shot_bullet_t2_laser2', 2],
        ))

    game.game_loop()

    game.assert_test_passed(
        condition=not npc.alive(),
        failed_msg="Player did not kill squirrel.")
