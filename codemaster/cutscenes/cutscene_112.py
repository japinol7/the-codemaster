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
        self.actor_fighter = None
        self.actor_fighter_ini_rect = None

        super().__init__(level, game)

    def update_pc_enter_level(self):
        super().update_pc_enter_level()

        game = self.game

        if not self.actor_fighter:
            self.actor_fighter = game.level_cutscene.get_npcs_filtered_by_actor_type(
                ActorType.KUNG_FU_FIGHTER_MALE)[0]
            self.actor_fighter_ini_rect = self.actor_fighter.rect.copy()

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
            ['stop', 40],
            ['shot_bullet_t1_laser1', 1],
            ['shot_bullet_t2_laser2', 2],
            ['stop', 90],
            [f':set_magic_target::target_id:={self.actor_fighter.id}', 1],
            ['cast_vortex_of_doom_a', 1],
            ['set_magic_off', 1],
            ['stop', 1],
            ))

    def update_pc_leave_level(self):
        super().update_pc_leave_level()

    def check_pc_leave_level_condition(self):
        if self.actor_fighter.health < self.actor_fighter.stats.health_total / 2:
            return True
        return False

    def update(self):
        execute_pc_action(self.game)

        super().update()
