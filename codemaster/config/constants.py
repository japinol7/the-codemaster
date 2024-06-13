"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime
import os
import sys

from codemaster.version import version

N_LEVELS = 24

SCREEN_WIDTH = 1160
SCREEN_HEIGHT = 778

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

MSG_PC_DURATION = 3  # in secs
MSG_PC_DUR_SHORT = 2
MSG_PC_DELTA_X = 14
MSG_PC_DELTA_Y = 35

MSG_NPC_DURATION = 3
MSG_NPC_DUR_SHORT = 2
MSG_NPC_DURATION_LONG = 5
MSG_NPC_DURATION_VERY_LONG = 9

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

MIN_TICKS_ALLOWED_TO_PAUSE_GAME = 1060

ACTOR_POWER_RECOVERY_DEFAULT = 10
ACTOR_MIN_POWER_RECOVERY = 2
ACTOR_MIN_TIME_BETWEEN_ENERGY_SHIELD_CASTING = 1
ACTOR_TIME_BETWEEN_ENERGY_SHIELD_CASTING_DEFAULT = 3500

APP_TECH_NAME = 'codemaster'
LOG_START_APP_MSG = f"Start app {APP_TECH_NAME} version: {version.get_version()}"
LOG_END_APP_MSG = f"End app {APP_TECH_NAME}"

APP_NAME = f"The CodeMaster v. {version.get_version()}"
APP_NAME_SHORT = "The CodeMaster"
APP_NAME_LONG = "The CodeMaster. Nightmare on Bots' Island."
APP_NAME_DESC = "A spin-off sci-fi mystery based on " \
                "Pac's Revenge series games by @japinol (c) 1987, 1988, 2015, 2021, 2024."

LOG_FILE = os.path.join('logs', f"log_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')}.log")
LOG_FILE_UNIQUE = os.path.join('logs', "log.log")
SYS_STDOUT = sys.stdout

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
    FONT_FIXED_DEFAULT_NAME = os.path.join(FONT_FOLDER, 'fixed.ttf')
else:
    CURRENT_PATH = '.'
    # CURRENT_PATH = os.path.join(CURRENT_PATH, '..')
    BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
    SOUNDS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'snd', SOUND_FORMAT)
    MUSIC_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'music')
    FONT_DEFAULT_NAME = os.path.join(CURRENT_PATH, 'assets', 'data', 'sans.ttf')
    FONT_FIXED_DEFAULT_NAME = os.path.join(CURRENT_PATH, 'assets', 'data', 'fixed.ttf')

BM_BACKGROUNDS_FOLDER = os.path.join(BITMAPS_FOLDER, 'backgrounds')
BM_CLOCKS_FOLDER = os.path.join(BITMAPS_FOLDER, 'clocks')
BM_TEXT_MSGS_FOLDER = os.path.join(BITMAPS_FOLDER, 'text_msgs')
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
BM_SELECTORS_FOLDER = os.path.join(BITMAPS_FOLDER, 'selectors')
BM_SPECIAL_EFFECTS_FOLDER = os.path.join(BITMAPS_FOLDER, 'special_effects')
BM_LIGHTS_FOLDER = os.path.join(BM_SPECIAL_EFFECTS_FOLDER, 'lights')
BM_PCS_FOLDER = os.path.join(BITMAPS_FOLDER, 'PCs')
BM_PC_PAC_FOLDER = os.path.join(BM_PCS_FOLDER, 'Pac')
BM_NPCS_FOLDER = os.path.join(BITMAPS_FOLDER, 'NPCs')
BM_TETHLORIENS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'tethloriens')
BM_TERMINATOR_EYES_FOLDER = os.path.join(BM_NPCS_FOLDER, 'terminator_eyes')
BM_SNAKES_FOLDER = os.path.join(BM_NPCS_FOLDER, 'snakes')
BM_DRAGONS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'dragons')
BM_BATS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'bats')
BM_SKULLS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'skulls')
BM_GHOSTS_FOLDER = os.path.join(BM_NPCS_FOLDER, 'ghosts')
BM_LEVELS_FOLDER = os.path.join(BITMAPS_FOLDER, 'levels')
BM_MAGIC_FOLDER = os.path.join(BITMAPS_FOLDER, 'magic')
BM_MISC_FOLDER = os.path.join(BITMAPS_FOLDER, 'misc')

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
    'im_radios': ('radio', 'png'),
    'im_invisible_holders': ('invisible_holder', 'png'),
    'life_recoveries': ('life', 'png'),
    'life_heart': ('heart', 'png'),
    'im_snakes': ('im_snake', 'png'),
    'im_snake_head': ('im_snake_head', 'png'),
    'im_snake_head_u_r': ('im_snake_head_u_r', 'png'),
    'im_snake_head_d_r': ('im_snake_head_d_r', 'png'),
    'im_snake_body': ('im_snake_body', 'png'),
    'im_snake_tail': ('im_snake_tail', 'png'),
    'im_dragons': ('im_dragon', 'png'),
    'im_dragon_head': ('im_dragon_head', 'png'),
    'im_dragon_head_u_r': ('im_dragon_head_u_r', 'png'),
    'im_dragon_head_d_r': ('im_dragon_head_d_r', 'png'),
    'im_dragon_body': ('im_dragon_body', 'png'),
    'im_dragon_tail': ('im_dragon_tail', 'png'),
    'im_door_keys': ('door_key', 'png'),
    'im_en_ghosts': ('ghost', 'png'),
    'im_en_skulls': ('skull', 'png'),
    'im_en_bats': ('im_bat', 'png'),
    'im_en_wolfmen': ('wolfman', 'png'),
    'im_en_pokoyos': ('pokoyo', 'png'),
    'im_en_vampires': ('vampire', 'png'),
    'im_en_demons': ('demon', 'png'),
    'im_terminator_eyes': ('terminator_eye', 'png'),
    'im_en_mages': ('mage', 'png'),
    'im_en_robots': ('robot', 'png'),
    'im_tethloriens': ('tethlorien', 'png'),
    'im_en_samurais': ('samurai', 'png'),
    'im_en_pumpkin_zombies': ('pumpkin_zombie', 'png'),
    'im_en_pumpkin_heads': ('pumpkin_head', 'png'),
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
    'text_msgs': ('text_msg', 'png'),
    'im_energy_shields': ('energy_shield', 'png'),
    'im_lightS': ('im_light', 'png'),
    'im_selectors': ('im_selector', 'png'),
    'im_lights': ('im_light', 'png'),
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
    'im_magic_activated':  ('magic_activated', 'png'),
    'im_lightning_bolt':  ('lightning_bolt', 'png'),
    'im_doom_bolt':  ('doom_bolt', 'png'),
    'im_vortex_of_doom': ('vortex_of_doom', 'png'),
    'im_fire_breath': ('fire_breath', 'png'),
    'im_neutrinos_bolt': ('neutrinos_bolt', 'png'),
    'im_samutrinos_bolt': ('samutrinos_bolt', 'png'),
    'im_drain_life':  ('drain_life', 'png'),
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
    'magic_bolt': ('magic_bolt', SOUND_FORMAT),
    'snd_mine_hit': ('torpedo', SOUND_FORMAT),
    'snd_npc_killed': ('explosion', SOUND_FORMAT),
    'snd_door_unlock': ('door_unlock', SOUND_FORMAT),
    }
