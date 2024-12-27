"""Module cutscene_111."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.cutscenes.cutscene_base import CutsceneBase
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.player_auto_actions import execute_pc_action


class Cutscene111(CutsceneBase):

    def __init__(self, level, game):
        self.game = game
        self.level = level
        self.name_short = 'Good morning Kaede'

        # Define some actors
        self.actor_kaede = None
        self.actor_kaede_ini_rect = None

        super().__init__(level, game)

    def update_pc_enter_level(self):
        super().update_pc_enter_level()

        game = self.game

        if not self.actor_kaede:
            self.actor_kaede = game.level_cutscene.get_npcs_filtered_by_actor_type(
                ActorType.KAEDE)[0]
            self.actor_kaede_ini_rect = self.actor_kaede.rect.copy()

        game.player.rect.x = 10
        self.actor_kaede.stats.health_total = self.actor_kaede.health = 310

        game.add_player_actions((
            ['go_right_very_slow', 400],
            ['go_right_very_slow', 520],
            ['stop', 80],
            ['go_right_slow', 130],
            ['stop', 1],
            ['stop', 90],
            ['shot_bullet_t2_laser2', 2],
            ['stop', 90],
            [f':set_magic_target:{self.actor_kaede.id}', 1],
            ['cast_vortex_of_doom_a', 1],
            ['set_magic_off', 1],
            ['go_right_slow', 180],
            ['stop', 1],
            ))

    def update_pc_leave_level(self):
        super().update_pc_leave_level()

        # self.actor_kaede.rect = self.actor_kaede_ini_rect

    def check_pc_leave_level_condition_hook(self):
        if self.actor_kaede.health < self.actor_kaede.stats.health_total / 3:
            self.update_pc_leave_level()

    def update(self):
        execute_pc_action(self.game)

        super().update()
