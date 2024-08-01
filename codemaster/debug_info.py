"""Module debug info."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime
from collections import OrderedDict

from codemaster.tools.logger.logger import log
from codemaster.tools.utils.utils import pretty_dict_to_string, write_list_to_file
from codemaster.config.constants import MUSIC_BOX, DIRECTION_RIGHT
from codemaster.models.actors.items.bullets import BULLET_MAX_QTY
from codemaster.levels import Level


class DebugInfo:

    def __init__(self, player, game):
        self.player = player
        self.game = game

    def print_help_keys(self):
        print('  ^ numpad_divide: \t interactive debug output\n'
              '  ^n: \t print a list of all NPCs in the current level\n'
              '  ^ Shift + n: \t print a list of all NPCs in all levels, ordered by level\n'
              '  ^ Alt + Shift + n: \t print a list of all NPCs in all levels, ordered by NPC name\n'
              '  Alt + n: \t print a list of all items in the current level\n'
              '  Alt + Shift + n: \t print a list of all items in all levels, ordered by level\n'
              '  ^ Alt + n: \t print a list of all items in all levels, ordered by item name\n'
              '  ^d: \t print debug information to console\n'
              '  ^l: \t write debug information to a log file\n'
              )

    def print_supercheat_keys(self):
        print('  ^i: \t put the player above it\'s current position  (cheat)\n'
              '  ^ numpad_minus: \t great advantage superhero (cheat)\n'
              '  ^ numpad_multiply: \t superhero invulnerability flag (cheat)\n'
              )

    def print_debug_info(self, to_log_file=False):
        debug_dict = OrderedDict([
            ('time', str(datetime.now())),
            # ('full screen', self.game.full_screen),
            ('screen size', self.game.size),
            ('fps', self.game.is_paused and '\t ---- (The game is paused)'
             or "\t {:.2f}".format(self.game.clock.get_fps())),
            ('current song', MUSIC_BOX[self.game.current_song]),
            ('music playing', not self.game.is_music_paused),
            ('sound effects', self.game.sound_effects),
            ('game paused', self.game.is_paused or self.game.is_help_screen or self.game.is_exit_curr_game_confirm),
            ('level', self.game.level_no + 1),
            ('platforms', self.player.level.platforms),
            ('doors', self.player.level.doors),
            ('locked doors', len([door for door in self.player.level.doors if door.is_locked])),
            ('door keys', self.player.level.door_keys),
            ('batteries left', self.player.level.batteries),
            ('files_disks left', self.player.level.files_disks),
            ('computers', self.player.level.computers),
            ('NPCs', self.player.level.npcs),
            ('bullets', self.player.level.bullets),
            ('player', OrderedDict([
                ('position (x, y)', (self.player.rect.x, self.player.rect.y)),
                ('position (bottom)', self.player.rect.bottom),
                ('direction', self.player.direction == DIRECTION_RIGHT and "R" or "L"),
                ('change position (x, y)', (self.player.change_x, "%.3f" % self.player.change_y)),
                ('invulnerable', self.player.invulnerable),
                ('stats', OrderedDict([
                    ('PC_level', self.player.stats['level']),
                    ('lives', self.player.stats['lives']),
                    ('health', self.player.stats['health']),
                    ('power', round(self.player.stats['power'],4)),
                    ('speed', self.player.stats['speed']),
                    ('score', self.player.stats['score']),
                    ('batteries', self.player.stats['batteries']),
                    ('files disks', self.player.stats['files_disks']),
                    ('files disks types', self.player.stats['files_disks_type']),
                    ('potions_health', len(self.player.stats['potions_health'])),
                    ('potions_power', len(self.player.stats['potions_power'])),
                    ('apples', self.player.stats['apples']),
                    ('apples_type', self.player.stats['apples_type']),
                    ('door_keys', self.player.stats['door_keys']),
                    ('door_keys_type', self.player.stats['door_keys_type']),
                    ('bullets_t01', self.player.stats['bullets_t01']),
                    ('bullets_t02', self.player.stats['bullets_t02']),
                    ('bullets_t03', self.player.stats['bullets_t03']),
                    ('bullets_t04', self.player.stats['bullets_t04']),
                ])
                 ),
                ('levels completed: ', Level.levels_completed_ids(self.game)),
            ])
             )
        ])
        debug_info_title = 'Current game stats'
        debug_info = f"\n\n\n{'-' * 36}{debug_info_title}{'-' * 36}\n"

        debug_info = f"{debug_info}{pretty_dict_to_string(debug_dict, with_last_new_line=True)}" \
                     f"{'-' * (36 + len(debug_info_title) + 36)}\n"
        if to_log_file:
            log.info(debug_info)
        else:
            print(debug_info)

    def super_cheat_superhero(self):
        self.player.stats['score'] = 3700 if self.player.stats['score'] < 3700 else self.player.stats['score']
        self.player.lives = 20
        self.player.health = 100
        self.player.power = 100
        self.player.stats['bullets_t01'] = BULLET_MAX_QTY
        self.player.stats['bullets_t02'] = BULLET_MAX_QTY
        self.player.stats['bullets_t03'] = BULLET_MAX_QTY
        self.player.stats['bullets_t04'] = BULLET_MAX_QTY

    def super_cheat_superhero_minor(self):
        if self.player.health < 66:
            self.player.health += 22
        if self.player.power < 66:
            self.player.power += 25
