"""Module cutscene_base."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.items import InvisibleHolderNarrator
from codemaster.models.clocks import ClockTimer
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.actors.text_msgs.text_msgs import TextMsgActorNarrator
from codemaster.tools.logger.logger import log


class CutsceneBase:

    def __init__(self, level, game):
        self.game = game
        self.level = level
        self.id = level.id
        self.player = game.player
        self.clock_timer = None
        self.current_stat = ''
        self.actor_msg_holder = None
        self.is_msg_screen = False
        self.msg_screen = ''
        self.msg_screen_obj = None
        self.msg_screen_clock = None

        if not getattr(self, 'name_short', None):
            self.name_short = self.game

        level.door_previous_pos_player = level.player_start_pos_left
        level.door_previous_pos_world = level.world_start_pos_left

        # Attributes to restore after cutscene
        self.old_game_is_magic_on = False
        self.old_player_invulnerable = False
        self.old_player_direction = None
        self.old_player_health = None
        self.old_player_score = None
        self.old_player_power = None
        self.old_player_bullets_t01 = None
        self.old_player_bullets_t02 = None
        self.old_player_bullets_t03 = None
        self.old_player_bullets_t04 = None
        self.old_player_bullets_t01_shot = None
        self.old_player_bullets_t02_shot = None
        self.old_player_bullets_t03_shot = None
        self.old_player_bullets_t04_shot = None

        self.old_npcs_stats = {}
        for npc in self.level.npcs:
            self.old_npcs_stats[npc.id] = {
                'obj': npc,
                'x': npc.rect.x,
                'y': npc.rect.y,
                'health': npc.health,
                'power': npc.power,
                }

    def update_pc_enter_level(self):
        game = self.game
        game.is_log_debug and log.debug(f"Initialize cutscene level: {self.id}")

        self.deactivate_msg_screen()

        # Add an actor that will hold cutscene msgs
        self.actor_msg_holder = InvisibleHolderNarrator(0, 0, game)
        self.level.add_actors([self.actor_msg_holder])

        self.player.reset_position()
        game.player.remove_pc_not_persistent_things()

        # Stats to recover after the cutscene ends
        self.old_game_is_magic_on = game.is_magic_on
        self.old_player_direction = self.player.direction
        self.old_player_invulnerable = self.player.invulnerable
        self.old_player_health = self.player.health
        self.old_player_power = self.player.power
        self.old_player_score = self.player.stats['score']
        self.old_player_bullets_t01 = self.player.stats['bullets_t01']
        self.old_player_bullets_t02 = self.player.stats['bullets_t02']
        self.old_player_bullets_t03 = self.player.stats['bullets_t03']
        self.old_player_bullets_t04 = self.player.stats['bullets_t04']
        self.old_player_bullets_t01_shot = self.player.stats['bullets_t01_shot']
        self.old_player_bullets_t02_shot = self.player.stats['bullets_t02_shot']
        self.old_player_bullets_t03_shot = self.player.stats['bullets_t03_shot']
        self.old_player_bullets_t04_shot = self.player.stats['bullets_t04_shot']

        game.is_magic_on = False
        self.player.invulnerable = True

        game.clean_actors_actions()

    def update_pc_leave_level(self):
        self.game.is_log_debug and log.debug(f"Leave cutscene level: {self.id}")
        self.level.done = True
        self.player.stop()
        self.game.update_state_counter = -2
        self.game.player.remove_pc_not_persistent_things()
        self.actor_msg_holder = None

        # Stats to recover after the cutscene ends
        self.game.is_magic_on = self.old_game_is_magic_on
        self.player.direction = self.old_player_direction
        self.player.invulnerable = self.old_player_invulnerable
        self.player.health = self.old_player_health
        self.player.power = self.old_player_power
        self.player.stats['score'] = self.old_player_score
        self.player.stats['bullets_t01'] = self.old_player_bullets_t01
        self.player.stats['bullets_t02'] = self.old_player_bullets_t02
        self.player.stats['bullets_t03'] = self.old_player_bullets_t03
        self.player.stats['bullets_t04'] = self.old_player_bullets_t04
        self.player.stats['bullets_t01_shot'] = self.old_player_bullets_t01_shot
        self.player.stats['bullets_t02_shot'] = self.old_player_bullets_t02_shot
        self.player.stats['bullets_t03_shot'] = self.old_player_bullets_t03_shot
        self.player.stats['bullets_t04_shot'] = self.old_player_bullets_t04_shot

        for npc_data in self.old_npcs_stats.values():
            npc_data['obj'].rect.x = npc_data['x'] - self.game.level.get_scroll_shift_delta()
            npc_data['obj'].rect.y = npc_data['y'] + self.game.level.get_scroll_shift_top_delta()
            npc_data['obj'].health = npc_data['health']
            npc_data['obj'].power = npc_data['power']

    def _check_pc_leave_level_condition(self):
        # Check this now and then, but skip the first four iterations
        if self.game.update_state_counter == 4:
            if self.check_pc_leave_level_condition():
                self.update_pc_leave_level()

    def check_pc_leave_level_condition(self):
        return False

    def _create_cutscene_msg_actor(self, msg, time_in_secs=6000):
        self.msg_screen_obj = TextMsg.create(
            "Narrator:\n"
            f"{msg}",
            game=self.game,
            owner=self.actor_msg_holder,
            delta_x=0, delta_y=-30,
            time_in_secs=time_in_secs,
            msg_class=TextMsgActorNarrator,
            balloon_lines_count=4,
            balloon_chars_for_line=52,
            )

    def activate_msg_screen(self, msg, time_in_secs=4):
        self.is_msg_screen = True
        self.msg_screen = msg
        self.game.screen_cutscene.background_screenshot.blit(self.game.screen, (0, 0))

        self._create_cutscene_msg_actor(msg, time_in_secs)
        self.msg_screen_clock = ClockTimer(
            self.game, time_in_secs, trigger_method=self.deactivate_msg_screen)

    def deactivate_msg_screen(self):
        self.is_msg_screen = False
        self.msg_screen = ''
        if self.msg_screen_obj:
            self.msg_screen_obj.die_hard()
        self.msg_screen_obj = None
        self.msg_screen_clock = None

    def update(self):
        self._check_pc_leave_level_condition()
