"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

import os
import sys

SCREEN_WIDTH = 1160
SCREEN_HEIGHT = 778
# Screen Scale. Strongly recommended 1.  Other values: 1.1, 1.15, 1.2, 1.25
# It does not scale sprites on loading time, but the entire screen on each frame
SCREEN_SCALE = 1

SCROLL_NEAR_LEFT_SIDE = 380
SCROLL_NEAR_RIGHT_SIDE = SCREEN_WIDTH - SCROLL_NEAR_LEFT_SIDE
NEAR_LEFT_SIDE = 25

SCROLL_NEAR_TOP = 300
SCROLL_NEAR_BOTTOM = SCREEN_HEIGHT - SCROLL_NEAR_TOP

NEAR_TOP = 40
NEAR_BOTTOM = SCREEN_HEIGHT - NEAR_TOP
NEAR_EARTH = 40
SCREEN_NEAR_EARTH = SCREEN_HEIGHT - NEAR_EARTH
NEAR_BOTTOM_WHEN_PLATFORM = SCREEN_HEIGHT - NEAR_EARTH

NEAR_RIGHT_SIDE = SCREEN_WIDTH - NEAR_LEFT_SIDE

SCREEN_BAR_NEAR_TOP = 10
SCREEN_BAR_NEAR_BOTTOM = SCREEN_HEIGHT - 25


# Directions for moving actors. They are also used for sprite images frame index
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4
DIRECTION_UP_LEFT = 5
DIRECTION_UP_RIGHT = 6
DIRECTION_DOWN_LEFT = 7
DIRECTION_DOWN_RIGHT = 8

FACE_DIRECTION = DIRECTION_RIGHT
DIRECTION_RIP = 5    # Special direction to use when a player character is dead

DOOR_STD_WIDTH = 130
DOOR_STD_HEIGHT = 188
DOOR_POSITION_L = 0
DOOR_POSITION_R = 1

DOOR_DEST_NL = 2        # Normal  (reverse of DOOR_POSITION_x)
DOOR_DEST_TL = 3        # Top Left
DOOR_DEST_TR = 4        # Top Right
DOOR_DEST_TC = 5        # Top Center

VELOCITY_DEFAULT = 2
POS_SCREEN_RATIO = 30

CELL_SIZE_MIN_FOR_IM_MD = 19       # Minimum cell size for image in medium resolution

MAX_APPLES_ON_BOARD = 18
MAX_MINES_ON_BOARD = 30
MAX_BATS_ON_BOARD = 7
MAX_DIVIDER_APPLES_ON_BOARD = 186
MAX_DIVIDER_MINES_ON_BOARD = 130


LOG_FILE = os.path.join('files', 'log.txt')
SCORES_FILE = os.path.join('files', 'scores.txt')

SOUND_FORMAT = 'ogg'
MUSIC_FORMAT = 'ogg'

# If the code is frozen, use this path:
if getattr(sys, 'frozen', False):
    CURRENT_PATH = sys._MEIPASS
    BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
    SOUNDS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'snd', SOUND_FORMAT)
    MUSIC_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'music')
    FONT_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'data')
    FONT_DEFAULT_NAME = os.path.join(FONT_FOLDER, 'sans.ttf')
else:
    CURRENT_PATH = '.'
    # CURRENT_PATH = os.path.join(CURRENT_PATH, '..')
    BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
    SOUNDS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'snd', SOUND_FORMAT)
    MUSIC_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'music')
    FONT_DEFAULT_NAME = os.path.join(CURRENT_PATH, 'assets', 'data', 'sans.ttf')

BM_BACKGROUNDS_FOLDER = os.path.join(BITMAPS_FOLDER, 'backgrounds')
BM_CLOCKS_FOLDER = os.path.join(BITMAPS_FOLDER, 'clocks')
BM_BATTERIES_FOLDER = os.path.join(BITMAPS_FOLDER, 'batteries')
BM_BULLETS_FOLDER = os.path.join(BITMAPS_FOLDER, 'bullets')
BM_CARTRIDGES_FOLDER = os.path.join(BITMAPS_FOLDER, 'cartridges')
BM_DOORS_FOLDER = os.path.join(BITMAPS_FOLDER, 'doors')
BM_DOOR_KEYS_FOLDER = os.path.join(BITMAPS_FOLDER, 'door_keys')
BM_DECORATIONS = os.path.join(BITMAPS_FOLDER, 'decorations')
BM_PLAT_WATER = os.path.join(BM_DECORATIONS, 'water')
BM_FILE_DISKS_FOLDER = os.path.join(BITMAPS_FOLDER, 'files_disks')
BM_COMPUTERS_FOLDER = os.path.join(BITMAPS_FOLDER, 'computers')
BM_LIVES_BASE_FOLDER = os.path.join(BITMAPS_FOLDER, 'lives')
BM_LIVES_FOLDER = os.path.join(BM_LIVES_BASE_FOLDER, 'pac_lives')
BM_LOGOS_FOLDER = os.path.join(BITMAPS_FOLDER, 'logos')
BM_MINES_FOLDER = os.path.join(BITMAPS_FOLDER, 'mines')
BM_EXPLOSIONS_FOLDER = os.path.join(BITMAPS_FOLDER, 'explosions')
BM_APPLES_FOLDER = os.path.join(BITMAPS_FOLDER, 'apples')
BM_POTIONS_FOLDER = os.path.join(BITMAPS_FOLDER, 'potions')
BM_POTION_HEALTH_FOLDER = os.path.join(BM_POTIONS_FOLDER, 'health')
BM_POTION_POWER_FOLDER = os.path.join(BM_POTIONS_FOLDER, 'power')
BM_ENERGY_SHIELD_FOLDER = os.path.join(BITMAPS_FOLDER, 'energy_shields')
BM_PCS_FOLDER = os.path.join(BITMAPS_FOLDER, 'PCs')
BM_PC_PAC_FOLDER = os.path.join(BM_PCS_FOLDER, 'Pac')
BM_NPCS_FOLDER = os.path.join(BITMAPS_FOLDER, 'NPCs')
BM_TERMINATOR_EYES_FOLDER = os.path.join(BM_NPCS_FOLDER, 'terminator_eyes')
BM_SNAKES_FOLDER = os.path.join(BM_NPCS_FOLDER, 'snakes')
BM_BATS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'bats')
BM_SKULLS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'skulls')
BM_GHOSTS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'ghosts')
BM_LEVELS_FOLDER = os.path.join(BITMAPS_FOLDER, 'levels')

INIT_OPTIONS_FOLDER = os.path.join(CURRENT_PATH, 'extra')
INIT_OPTIONS_FILE = os.path.join(INIT_OPTIONS_FOLDER, 'init_options.cfg')

MUSIC_BOX = (
    f'action_song__192b.{MUSIC_FORMAT}',
    )

FILE_NAMES = {
    'im_tiles_spritesheet': ('tiles_spritesheet', 'png'),
    'im_backgrounds': ('background', 'png'),
    'seal_just_a_demo': ('seal_just_a_demo', 'png'),
    'im_pj_spritesheet': ('pj_spritesheet_01_walk', 'png'),
    'im_pc_pac': ('Pac_01_walk', 'png'),
    'im_pj_rip': ('rip_player_ld', 'png'),
    'im_batteries': ('battery', 'png'),
    'life_recoveries': ('life', 'png'),
    'life_heart': ('heart', 'png'),
    'im_snakes': ('im_snake', 'png'),
    'im_snake_head': ('im_snake_head', 'png'),
    'im_snake_head_u_r': ('im_snake_head_u_r', 'png'),
    'im_snake_head_d_r': ('im_snake_head_d_r', 'png'),
    'im_snake_body': ('im_snake_body', 'png'),
    'im_snake_tail': ('im_snake_tail', 'png'),
    'im_door_keys': ('door_key', 'png'),
    'im_en_ghosts': ('ghost', 'png'),
    'im_en_skulls': ('skull', 'png'),
    'im_en_bats': ('im_bat', 'png'),
    'im_en_wolfmen': ('wolfman', 'png'),
    'im_en_vampires': ('vampire', 'png'),
    'im_en_demons': ('demon', 'png'),
    'im_terminator_eyes': ('terminator_eye', 'png'),
    'im_files_disks': ('files_disk', 'png'),
    'im_computer': ('computer', 'png'),
    'im_apples': ('im_apple', 'png'),
    'im_mines': ('im_mine', 'png'),
    'explosions': ('explosion', 'png'),
    'im_doors': ('level_door', 'png'),
    'im_bullet_t1': ('im_bullet_t1', 'png'),
    'im_bullet_t2': ('im_bullet_t2', 'png'),
    'im_bullet_t3': ('im_bullet_t3', 'png'),
    'im_bullet_t4': ('im_bullet_t4', 'png'),
    'im_cartridges': ('im_cartridge', 'png'),
    'im_water': ('im_water', 'png'),
    'im_potion_health': ('health_rec', 'png'),
    'im_potion_power': ('power_rec', 'png'),
    'im_clocks': ('clock', 'png'),
    'im_energy_shields': ('energy_shield', 'png'),
    'im_bg_start_game': ('bg_start_game', 'png'),
    'im_bg_start_game_vertical': ('bg_start_game_vert', 'png'),
    'im_background': ('background', 'png'),
    'im_bg_score_bar': ('bg_score_bar', 'png'),
    'im_bg_score_bar2': ('bg_score_bar2', 'png'),
    'im_screen_help': ('screen_help', 'png'),
    'im_screen_help_vertical': ('screen_help_vert', 'png'),
    'im_logo_japinol': ('logo_japinol_ld', 'png'),
    'im_help_key': ('help_key', 'png'),
    'bg_blue_t1_big_logo': ('bg_blue_t1_big_logo', 'png'),
    'im_bg_blue_t1': ('bg_blue_t1', 'png'),
    'im_bg_blue_t2': ('bg_blue_t2', 'png'),
    'im_bg_black_t1': ('bg_black_t1', 'png'),
    'im_level_completed':  ('level_completed', 'png'),
    'snd_death_pl': ('death_pl_02',  SOUND_FORMAT),
    'snd_apple_hit': ('apple_found', SOUND_FORMAT),
    'snd_pl_battery_found': ('battery_found_j01', SOUND_FORMAT),
    'snd_en_hit': ('enemy_j02', SOUND_FORMAT),
    'snd_collission': ('collision', SOUND_FORMAT),
    'snd_bat_hit': ('enemy_j02', SOUND_FORMAT),
    'snd_bat_scream': ('scream', SOUND_FORMAT),
    'snd_bullet_t1': ('bullet_t1', SOUND_FORMAT),
    'snd_bullet_t2': ('bullet_t2', SOUND_FORMAT),
    'snd_bullet_t3': ('bullet_t3', SOUND_FORMAT),
    'snd_bullet_t4': ('bullet_t4', SOUND_FORMAT),
    'snd_weapon_empty': ('weapon_empty', SOUND_FORMAT),
    'snd_explosion': ('explosion', SOUND_FORMAT),
    'snd_mine_hit': ('torpedo', SOUND_FORMAT),
    'snd_npc_killed': ('explosion', SOUND_FORMAT),
    'snd_door_unlock': ('door_unlock', SOUND_FORMAT),
    }
