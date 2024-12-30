"""Module cutscene_111."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.clocks import ClockTimer
from codemaster.cutscenes.cutscene_base import CutsceneBase
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

        self.clock_kaede_talk_msg_1 = None

    def _kaede_talk_msg(self):
        TextMsg.create(
            "Have a nice trip, honey!", self.game,
            time_in_secs=8,
            delta_x=16, delta_y=2, owner=self.actor_kaede)

    def update_pc_enter_level(self):
        super().update_pc_enter_level()

        game = self.game

        if not self.actor_kaede:
            self.actor_kaede = self.level.get_npcs_filtered_by_actor_type(
                ActorType.KAEDE)[0]
            self.actor_kaede_ini_rect = self.actor_kaede.rect.copy()

        self.clock_kaede_talk_msg_1 = ClockTimer(
            game, 19, trigger_method=self._kaede_talk_msg)

        game.player.rect.x = 10

        game.add_player_actions((
            ['go_right_very_slow', 410],
            ['go_right_very_slow', 340],
            [":talk::msg:="
             "Kaede...!", 1],
            ['go_right_very_slow', 150],
            ['stop', 90],
            [":talk::msg:="
             "Good morning Kaede!"
             "::time_in_secs:=4", 1],
            ['go_right_slow', 130],
            ['stop', 250],
            [":talk::msg:="
             "I'm on my way to ask\n"
             "your father for your hand!\n: )"
             "::time_in_secs:=8", 1],
            ['stop', 540],
            ['go_right_slow', 180],
            ['stop', 36],
            ['go_right_slow', 200],
            [":talk::msg:="
             "Ok. Kaito's Kingdom is to \n"
             "the north-west!\nLet's go..."
             "::time_in_secs:=4", 1],
            ['go_right_slow', 450],
            ['leave_cutscene', 1],
            ))

    def update_pc_leave_level(self):
        super().update_pc_leave_level()

    def update(self):
        execute_pc_action(self.game)
        self.clock_kaede_talk_msg_1.tick()

        super().update()
