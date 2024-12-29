"""Module cutscene_manager."""
__author__ = 'Joan A. Pinol  (japinol)'


def start_cutscene(cutscene_num, game):
    if game.level_tutorial:
        return

    game.level_cutscene = game.cutscene_levels[cutscene_num]
    game.level_cutscene.level_to_return = game.level
    game.level_cutscene.level_to_return_door = game.level.previous_door_crossed
    game.level = game.level_cutscene
    game.player.level = game.level_cutscene
    game.level_no = game.level_cutscene.id
    game.level.update_pc_enter_level()
    game.is_cutscene_screen = True
