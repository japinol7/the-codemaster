"""Module test_npcs_cast_spells_on_pc."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
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
    def test_pc_hit_with_fire_breath_spell_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = DemonMale(600, 664, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False

        npc.spell_2_name = ActorType.FIRE_BREATH_A.name
        npc.probability_to_cast_spell_1 = 0
        npc.probability_to_cast_spell_2 = 100
        npc.probability_to_cast_spell_3 = 0

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=3)
    def test_pc_hit_with_neutrinos_bolt_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = TethlorienRed(600, 660, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False

        npc.spell_1_name = ActorType.NEUTRINOS_BOLT_A.name
        npc.probability_to_cast_spell_1 = 100
        npc.probability_to_cast_spell_2 = 0
        npc.probability_to_cast_spell_3 = 0

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=3)
    def test_pc_hit_with_samutrinos_bolt_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = SamuraiMale(600, 654, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False

        npc.spell_1_name = ActorType.SAMUTRINOS_BOLT_A.name
        npc.probability_to_cast_spell_1 = 100
        npc.probability_to_cast_spell_2 = 0
        npc.probability_to_cast_spell_3 = 0
        npc.stats.time_between_spell_casting = 820

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=6)
    def test_pc_hit_with_vortex_doom_spell_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = DemonMale(600, 664, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False

        npc.spell_1_name = ActorType.VORTEX_OF_DOOM_A.name
        npc.probability_to_cast_spell_1 = 100
        npc.probability_to_cast_spell_2 = 0
        npc.probability_to_cast_spell_3 = 0

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=6)
    def test_pc_hit_with_doom_bold_spell_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = DemonMale(600, 664, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False

        npc.spell_1_name = ActorType.DOOM_BOLT_B.name
        npc.probability_to_cast_spell_1 = 100
        npc.probability_to_cast_spell_2 = 0
        npc.probability_to_cast_spell_3 = 0

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")

    @game_test(levels=[3], timeout=3)
    def test_pc_hit_with_enough_drain_life_spells_must_die(self, game):
        player = game.player
        player.rect.x, player.rect.y = 260, 620
        player.health = 22
        player.lives = 1

        npc = PumpkinHeadA(600, 662, game, change_x=0)
        npc.direction = DIRECTION_LEFT
        npc.can_shot = False

        npc.spell_2_name = ActorType.DRAIN_LIFE_A.name
        npc.probability_to_cast_spell_1 = 0
        npc.probability_to_cast_spell_2 = 100
        npc.probability_to_cast_spell_3 = 0
        npc.stats.time_between_spell_casting = 180

        game.level.add_actors([npc])

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="NPC did not kill the player.")
