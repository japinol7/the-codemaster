"""Module cutscene_112."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.cutscenes.cutscene_base import CutsceneBase
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.player_auto_actions import execute_pc_action


class Cutscene112(CutsceneBase):

    def __init__(self, level, game):
        self.game = game
        self.level = level
        self.name_short = 'Arbitrary test'

        # Define some actors
        self.actor_skull = None
        self.actor_skull_ini_rect = None

        super().__init__(level, game)

    def update_pc_enter_level(self):
        super().update_pc_enter_level()

        game = self.game

        if not self.actor_skull:
            self.actor_skull = game.level_cutscene.get_npcs_filtered_by_actor_type(
                ActorType.SKULL_YELLOW)[0]
            self.actor_skull_ini_rect = self.actor_skull.rect.copy()

        game.add_player_actions((
            ['go_right', 4],
            ['jump', 10],
            ['go_right', 30],
            ['jump', 10],
            ['go_right', 15],
            ['jump', 10],
            ['go_right', 20],
            ['jump', 10],
            ['go_right', 50],
            ['jump', 10],
            ['go_right', 30],
            ['stop', 1],
            ['go_right', 72],
            ['stop', 1],
            ))

    def update_pc_leave_level(self):
        super().update_pc_leave_level()

    def check_pc_leave_level_condition_hook(self):
        if self.actor_skull.rect.x - self.player.rect.x < 250:
            self.update_pc_leave_level()

    def update(self):
        execute_pc_action(self.game)

        super().update()
