"""Module test_mines_and_explosions.
Mines and explosions of enough power should kill player and NPC lives.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.items import MineLilac
from codemaster.models.actors.npcs import SkullYellow
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[3], timeout=3)
def test_mine_explosion_should_kill_pc_and_npc(game):
    game.player.rect.x, game.player.rect.y = 380, 650
    game.player.health = 22
    game.player.lives = 1

    game.add_player_actions((
        ['go_right', 40],
        ['stop', 1],
        ))

    # Add mines
    mines = []
    x = 550
    for _ in range(5):
        y = 720
        for __ in range(2):
            mines.append(MineLilac(x, y, game))
            y += 22
        x += 25
    game.level.add_actors(mines)

    # Add NPCs
    npc = SkullYellow(600, 670, game, change_x=0)
    game.level.add_actors([npc])

    game.game_loop()

    game.assert_test_passed(
        condition=game.player.lives < 1 and not npc.alive(),
        failed_msg="Mines explosions did not kill the player and the NPC.")
