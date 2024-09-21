"""Module test_pc_casts_co_spells_on_npcs.
The player should be able to kill NPCs when he casts
combat spells on them.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actor_types import ActorType
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[8], timeout=3)
def test_bat_hit_with_lightning_bolt_must_die(game):
    game.player.rect.x, game.player.rect.y = 240, 660
    game.is_magic_on = True

    game.add_player_actions((
        ['cast_lightning_bolt', 1],
        ))

    bat_black = game.level.get_npcs_filtered_by_actor_type(ActorType.BAT_BLACK)[0]
    game.test_spell_target = bat_black

    game.game_loop()

    game.assert_test_passed(
        condition=not bat_black.alive(),
        failed_msg="Player did not kill bat.")

@game_test(levels=[8], timeout=6)
def test_bat_hit_with_doom_bolt_must_die(game):
    game.player.rect.x, game.player.rect.y = 240, 660
    game.is_magic_on = True

    game.add_player_actions((
        ['cast_doom_bolt_a', 1],
        ['cast_doom_bolt_b', 1],
        ))

    bat_black = game.level.get_npcs_filtered_by_actor_type(ActorType.BAT_BLACK)[0]
    game.test_spell_target = bat_black

    game.game_loop()

    game.assert_test_passed(
        condition=not bat_black.alive(),
        failed_msg="Player did not kill bat.")

@game_test(levels=[8], timeout=6)
def test_bat_hit_with_vortex_of_doom_must_die(game):
    game.player.rect.x, game.player.rect.y = 240, 660
    game.is_magic_on = True

    game.add_player_actions((
        ['cast_vortex_of_doom_a', 1],
        ['cast_vortex_of_doom_b', 1],
        ))

    bat_black = game.level.get_npcs_filtered_by_actor_type(ActorType.BAT_BLACK)[0]
    game.test_spell_target = bat_black

    game.game_loop()

    game.assert_test_passed(
        condition=not bat_black.alive(),
        failed_msg="Player did not kill bat.")
