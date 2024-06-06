"""Module test_npcs_cast_spells_on_player."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.npcs import (
    DemonMale,
    PumpkinHeadA,
    SamuraiMale,
    TethlorienRed,
    )
from suiteoftests.test_suite.game_test import game_test


class TestNPCsCastSpellsOnPlayer:
    """NPCs should be able to kill a player life when they cast combat spells on them."""

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_fire_breath_spell_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = DemonMale(600, 664, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False
        npc.probability_to_cast_vortex_b = 0
        npc.probability_to_cast_fire_breath_a = 100
        npc.probability_to_cast_fire_breath_b = 0
        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_neutrinos_bolt_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = TethlorienRed(600, 660, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False
        npc.probability_to_cast_neutrinos_bolt_a = 100
        npc.probability_to_cast_neutrinos_bolt_b = 0
        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_samutrinos_bolt_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = SamuraiMale(600, 654, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False
        npc.probability_to_cast_samutrinos_bolt_a = 100
        npc.probability_to_cast_samutrinos_bolt_b = 0
        npc.stats.time_between_spell_casting = 820

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=6)
    def test_player_hit_with_vortex_doom_spell_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = DemonMale(600, 664, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False
        npc.probability_to_cast_vortex_b = 100
        npc.probability_to_cast_fire_breath_a = 0
        npc.probability_to_cast_fire_breath_b = 0

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=3)
    def test_player_hit_with_enough_drain_life_spells_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = PumpkinHeadA(600, 660, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False
        npc.probability_to_cast_vortex_b = 0
        npc.probability_to_cast_drain_life_a = 100
        npc.probability_to_cast_drain_life_b = 0
        npc.stats.time_between_spell_casting = 180

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")
