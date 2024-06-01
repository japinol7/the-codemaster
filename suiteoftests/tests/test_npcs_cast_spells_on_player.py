"""Module test_npcs_cast_spells_on_player."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.npcs import DemonMale
from suiteoftests.test_suite.game_test import game_test


class TestNPCsCastSpellsOnPlayer:
    """NPCs should be able to kill a player life when they cast combat spells on them."""

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_enough_combat_spells_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = DemonMale(600, 664, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False
        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")
