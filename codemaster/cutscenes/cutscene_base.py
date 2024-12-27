"""Module cutscene_base."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.items import (
    InvisibleHolderA,
    )
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

        if not getattr(self, 'name_short', None):
            self.name_short = self.game

        level.door_previous_pos_player = level.player_start_pos_left
        level.door_previous_pos_world = level.world_start_pos_left

        # Atributes to restore after cutscene
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

        self.old_npc_stats = {}
        for npc in self.level.npcs:
            self.old_npc_stats[npc.id] = {
                'obj': npc,
                'x': npc.rect.x,
                'y': npc.rect.y,
                'health': npc.health,
                'power': npc.power,
                }

    def update_pc_enter_level(self):
        game = self.game
        game.is_log_debug and log.debug(f"Initialize cutscene level: {self.id}")

        # Add an actor that will hold cutscene msgs
        self.actor_msg_holder = InvisibleHolderA(5, 390, game)
        self.level.add_actors([self.actor_msg_holder])

        self.player.reset_position()

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

        for npc_data in self.old_npc_stats.values():
            npc_data['obj'].rect.x = npc_data['x'] - self.game.level.get_scroll_shift_delta()
            npc_data['obj'].rect.y = npc_data['y'] + self.game.level.get_scroll_shift_top_delta()
            npc_data['obj'].health = npc_data['health']
            npc_data['obj'].power = npc_data['power']

    def check_pc_leave_level_condition(self):
        # Check this now and then, but skip the first four iterations
        if self.game.update_state_counter == 4:
            self.check_pc_leave_level_condition_hook()

    def check_pc_leave_level_condition_hook(self):
        pass

    def update(self):
        self.check_pc_leave_level_condition()
