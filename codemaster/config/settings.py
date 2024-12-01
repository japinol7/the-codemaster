"""Module settings."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.tools.utils import utils
from codemaster.config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

FPS_DEFAULT = 92  # Recommended: 92
FPS_MIN = 60
FPS_MAX = 900

DEFAULT_MUSIC_VOLUME = 0.5

DEFAULT_CELL_SIZE = 14


class Settings:
    """Settings of the game."""
    screen_width = None
    screen_height = None
    screen_scale = None
    screen_aspect_ratio = None
    screen_height_adjusted = None
    screen_width_adjusted = None
    # max. width of the user's initial display mode
    display_start_width = None
    # max. height of the user's initial display mode
    display_start_height = None
    cell_size = None
    fps = None
    fps_paused = None
    speed_pct = None
    has_selector_no_light = False
    is_full_screen = False
    im_screen_help = None
    im_bg_start_game = None
    score_to_win = None
    snake_body_len_start = None
    snake_body_len_max = None
    screen_near_top = None
    screen_near_bottom = None
    screen_near_right = None
    grid_width = None
    grid_height = None
    screen_bar_near_top = None
    player_position_ini = None
    are_bullets_allowed_to_collide = None
    # Relative position for sprite health bar
    sprite_health_bar_pos_rel = None
    sprite_health_bar_size = None
    font_size1 = None
    font_size2 = None
    font_spc_btn_chars1 = None
    font_spc_btn_chars2 = None
    # scores tuple with label and value x positions
    score_pos_lives1 = None
    score_pos_batteries1 = None
    score_pos_potions_power = None
    score_pos_potions_health = None
    score_pos_apples1 = None
    score_pos_door_keys = None
    score_pos_score1 = None
    score_pos_pc_level = None
    score_pos_level = None
    score_pos_lives2 = None
    score_pos_apples2 = None
    score_pos_score2 = None
    score_pos_health1_xy = None
    score_pos_health_size = None
    score_pos_power_size = None
    font_pos_factor = None
    font_pos_factor_t2 = None
    score_pos_lives_y = None
    score_pos_batteries1_y = None
    score_pos_potions_health_y = None
    score_pos_potions_power_y = None
    score_pos_apples_y = None
    score_pos_lives_size = None
    score_pos_batteries_size = None
    score_pos_apples_size = None
    score_pos_door_keys_size = None
    score_pos_bullets_y = None
    score_pos_bullets_size = None
    score_pos_f_disks_size = None
    score_pos_f_disks_y = None

    @classmethod
    def clean(cls):
        cls.screen_scale = 1
        cls.screen_width = int(SCREEN_WIDTH * cls.screen_scale)
        cls.screen_height = int(SCREEN_HEIGHT * cls.screen_scale)
        cls.screen_aspect_ratio = cls.screen_width / cls.screen_height
        cls.screen_height_adjusted = None
        cls.screen_width_adjusted = None
        cls.cell_size = DEFAULT_CELL_SIZE
        cls.cell_size_ratio = cls.screen_width * cls.screen_height / DEFAULT_CELL_SIZE
        cls.fps = FPS_DEFAULT
        cls.fps_paused = 14
        cls.speed_pct = 100
        cls.has_selector_no_light = False
        cls.is_full_screen = False
        cls.im_screen_help = 'im_screen_help'
        cls.im_bg_start_game = 'im_bg_start_game'
        cls.snake_body_len_start = 5
        cls.snake_body_len_max = 700
        cls.screen_near_top = None
        cls.screen_near_bottom = None
        cls.screen_near_right = None
        cls.grid_width = None
        cls.grid_height = None
        cls.screen_bar_near_top = None
        cls.player_position_ini = None
        cls.are_bullets_allowed_to_collide = False
        cls.font_size1 = None
        cls.font_size2 = None
        cls.font_spc_btn_chars1 = None
        cls.font_spc_btn_chars2 = None
        # scores tuple with label and value x positions
        cls.score_pos_health1_xy = [15, 15]
        cls.score_pos_lives1 = [150, 190]
        cls.score_pos_batteries1 = [240, 273]
        cls.score_pos_apples1 = [748, 790]
        cls.score_pos_door_keys = [748, 1024]
        cls.score_pos_potions_health = [860, 820]
        cls.score_pos_potions_power = [973, 922]
        cls.score_pos_score1 = [322, 405]
        cls.score_pos_pc_level = [1075, 1110]
        cls.score_pos_level = [580, 613]
        cls.score_pos_health_size = [100, 15]
        cls.score_pos_power_size = cls.score_pos_health_size
        cls.font_pos_factor = 0.91     # position or size factor for some text to render
        cls.font_pos_factor_t2 = 0.91  # position or size factor for some other text to render
        cls.score_pos_lives_y = None
        cls.score_pos_batteries1_y = None
        cls.score_pos_apples_y = None
        cls.score_pos_lives_size = [23, 23]
        cls.score_pos_batteries_size = [20, 20]
        cls.score_pos_apples_size = [21, 21]
        cls.score_pos_door_keys_size = [29, 21]
        cls.score_pos_bullets_size = [16, 16]
        cls.score_pos_bullets_y = None
        cls.score_pos_f_disks_size = [28, 28]
        cls.score_pos_f_disks_y = None

    @classmethod
    def calculate_settings(cls, full_screen=None, speed_pct=None):
        cls.clean()
        # Define screen values to resize the screen and images if necessary
        cls.screen_width_adjusted = int(cls.screen_height * cls.screen_aspect_ratio)
        cls.screen_height_adjusted = cls.screen_height
        # Resizes adjusted screen values for images if they are to high
        if cls.screen_height_adjusted > cls.screen_height:
            cls.screen_width_adjusted -= cls.screen_height_adjusted - cls.screen_height
            cls.screen_height_adjusted -= cls.screen_height_adjusted - cls.screen_height
        if cls.screen_width_adjusted > cls.screen_width:
            cls.screen_height_adjusted -= cls.screen_width_adjusted - cls.screen_width
            cls.screen_width_adjusted -= cls.screen_width_adjusted - cls.screen_width
        # Set full screen or windowed screen
        cls.is_full_screen = True if full_screen else False
        # Set fps
        if speed_pct and speed_pct.isdigit():
            cls.speed_pct = speed_pct
            cls.fps = int(cls.fps * int(speed_pct) / 100)
            if cls.fps < FPS_MIN:
                cls.fps = FPS_MIN
            elif cls.fps > FPS_MAX:
                cls.fps = FPS_MAX
        # Set positions for images and text
        cls.screen_near_bottom = cls.screen_height - cls.cell_size + 1
        cls.screen_near_right = cls.screen_width - cls.cell_size + 1
        cls.grid_width = cls.screen_width // cls.cell_size
        cls.grid_height = cls.screen_height // cls.cell_size
        cls.screen_bar_near_top = 10

        cls.player_position_ini = (cls.cell_size * 14, cls.screen_height // 5)

        # Font sizes for scores, etc
        cls.font_size1 = 24
        cls.font_size2 = 36
        cls.font_spc_btn_chars1 = 15
        cls.font_spc_btn_chars2 = 21
        cls.score_pos_lives_y = cls.screen_bar_near_top + 2
        cls.score_pos_batteries1_y = cls.screen_bar_near_top + 5
        cls.score_pos_f_disks_y = cls.screen_bar_near_top + 2
        cls.score_pos_potions_power_y = cls.screen_bar_near_top + 43
        cls.score_pos_potions_health_y = cls.screen_bar_near_top + 43
        cls.score_pos_apples_y = cls.screen_bar_near_top + 46
        cls.score_pos_bullets_y = cls.screen_bar_near_top + 29

        # Adapt size of images and text for some tested scenarios
        cls.font_pos_factor_t2 = cls.font_pos_factor
        cls.screen_bar_near_top = int(cls.screen_bar_near_top * cls.font_pos_factor)

        # Set score text and images positions and size
        cls.font_size1 = int(cls.font_size1 * cls.font_pos_factor)
        cls.font_size2 = int(cls.font_size2 * cls.font_pos_factor)
        cls.font_spc_btn_chars1 = int(cls.font_spc_btn_chars1 * cls.font_pos_factor)
        cls.font_spc_btn_chars2 = int(cls.font_spc_btn_chars2 * cls.font_pos_factor)
        cls.score_pos_lives1[0] = int(cls.score_pos_lives1[0] * cls.font_pos_factor)
        cls.score_pos_batteries1[0] = int(cls.score_pos_batteries1[0] * cls.font_pos_factor)
        cls.score_pos_apples1[0] = int(cls.score_pos_apples1[0] * cls.font_pos_factor)
        cls.score_pos_potions_power[0] = int(cls.score_pos_potions_power[0] * cls.font_pos_factor)
        cls.score_pos_potions_health[0] = int(cls.score_pos_potions_health[0] * cls.font_pos_factor)
        cls.score_pos_potions_power_y = int(cls.score_pos_potions_power_y * cls.font_pos_factor)
        cls.score_pos_potions_health_y = int(cls.score_pos_potions_health_y * cls.font_pos_factor)
        cls.score_pos_level[0] = int(cls.score_pos_level[0] * cls.font_pos_factor)
        cls.score_pos_batteries1_y = int(cls.score_pos_batteries1_y * cls.font_pos_factor)
        cls.score_pos_apples_y = int(cls.score_pos_apples_y * cls.font_pos_factor)
        cls.score_pos_bullets_y = int(cls.score_pos_bullets_y * cls.font_pos_factor)
        cls.score_pos_f_disks_y = int(cls.score_pos_f_disks_y * cls.font_pos_factor)

        cls.score_pos_health_size[0] = int(cls.score_pos_health_size[0] * cls.font_pos_factor)
        cls.score_pos_health_size[1] = int(cls.score_pos_health_size[1] * cls.font_pos_factor)
        cls.score_pos_lives_size[0] = int(cls.score_pos_lives_size[0] * cls.font_pos_factor)
        cls.score_pos_lives_size[1] = int(cls.score_pos_lives_size[1] * cls.font_pos_factor)
        cls.score_pos_batteries_size[0] = int(cls.score_pos_batteries_size[0] * cls.font_pos_factor)
        cls.score_pos_batteries_size[1] = int(cls.score_pos_batteries_size[1] * cls.font_pos_factor)
        cls.score_pos_apples_size[0] = int(cls.score_pos_apples_size[0] * cls.font_pos_factor)
        cls.score_pos_apples_size[1] = int(cls.score_pos_apples_size[1] * cls.font_pos_factor)

        cls.score_pos_bullets_size[0] = int(cls.score_pos_bullets_size[0] * cls.font_pos_factor)
        cls.score_pos_bullets_size[1] = int(cls.score_pos_bullets_size[1] * cls.font_pos_factor)
        cls.score_pos_f_disks_size[0] = int(cls.score_pos_f_disks_size[0] * cls.font_pos_factor)
        cls.score_pos_f_disks_size[1] = int(cls.score_pos_f_disks_size[1] * cls.font_pos_factor)

        cls.score_pos_lives1[1] = int(cls.score_pos_lives1[1] * cls.font_pos_factor)
        cls.score_pos_batteries1[1] = int(cls.score_pos_batteries1[1] * cls.font_pos_factor)
        cls.score_pos_apples1[1] = int(cls.score_pos_apples1[1] * cls.font_pos_factor)
        cls.score_pos_score1[1] = int(cls.score_pos_score1[1] * cls.font_pos_factor)
        cls.score_pos_level[1] = int(cls.score_pos_level[1] * cls.font_pos_factor)
        cls.score_pos_health1_xy[1] = int(cls.score_pos_health1_xy[1] * cls.font_pos_factor)

        cls.screen_near_top = int(cls.screen_height * 0.057)
        cls.screen_near_top = int(cls.screen_near_top * cls.font_pos_factor * 2)

        # Sprite health bar size and relative position
        cls.score_pos_power_size = cls.score_pos_health_size
        cls.sprite_health_bar_size = utils.Size(
            w=8 + cls.cell_size * 1.8,
            h=2 + cls.cell_size / 2.5)
        cls.sprite_health_bar_pos_rel = utils.Point(
            x=-1 + cls.cell_size * 1.2 if cls.cell_size * 1.2 > 8 else 8,
            y=cls.cell_size * 0.8 if cls.cell_size * 0.8 < 10 else 10)
