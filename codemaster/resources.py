"""Module resources."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from codemaster.tools.utils.colors import Color
from codemaster.config import constants as consts
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.config.settings import Settings


def file_name_get(name, subname='', num=None, subnum=None, quality='', folder=consts.BITMAPS_FOLDER):
    return os.path.join(
        folder,
        f"{consts.FILE_NAMES['%s%s' % (name, subname)][0]}"
        f"{quality}"
        f"{num and '_%02i' % num or ''}"
        f"{subnum and '_%02i' % subnum or ''}"
        f".{consts.FILE_NAMES['%s%s' % (name, subname)][1]}")


def import_folder_images(path):
    surface_list = []
    for _, __, image_files in os.walk(path):
        for image in image_files:
            full_path = os.path.join(path, image)
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


class Resource:
    """Some resources used in the game that do not have their own class."""
    apple_hit_sound = None
    bat_hit_sound = None
    bat_scream_sound = None
    bullet_t1_sound = None
    bullet_t2_sound = None
    bullet_t3_sound = None
    bullet_t4_sound = None
    bullet_hit_sound = None
    collission_sound = None
    explosion_sound = None
    item_hit_sound = None
    mine_hit_sound = None
    weapon_empty_sound = None
    images = {}
    txt_surfaces = {
        'game_paused': None, 'player_wins': None,
        'game_over': None, 'game_over_2': None,
        'press_intro_to_continue': None, 'press_intro_to_continue_2': None,
        'game_start': None, 'game_continue_last': None,
        'game_continue_last_failed': None,
        'level_no': None, 'congrats': None, 'congrats_2': None,
        'you_have_beaten_the_game': None, 'you_have_beaten_the_game_2': None,
        }

    @classmethod
    def load_sound_resources(cls):
        try:
            cls.apple_hit_sound = pg.mixer.Sound(file_name_get(name='snd_apple_hit', folder=consts.SOUNDS_FOLDER))
        except Exception as e:
            raise Exception(f"{e} SDL Error. Probably no sound device found. Connect your headphones and it should work")

        cls.bat_hit_sound = pg.mixer.Sound(file_name_get(name='snd_bat_hit', folder=consts.SOUNDS_FOLDER))
        cls.bat_scream_sound = pg.mixer.Sound(file_name_get(name='snd_bat_scream', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t1_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t1', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t2_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t2', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t3_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t3', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t4_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t4', folder=consts.SOUNDS_FOLDER))
        cls.bullet_hit_sound = pg.mixer.Sound(file_name_get(name='snd_explosion', folder=consts.SOUNDS_FOLDER))
        cls.collission_sound = pg.mixer.Sound(file_name_get(name='snd_collission', folder=consts.SOUNDS_FOLDER))
        cls.explosion_sound = pg.mixer.Sound(file_name_get(name='snd_explosion', folder=consts.SOUNDS_FOLDER))
        cls.item_hit_sound = pg.mixer.Sound(file_name_get(name='snd_apple_hit', folder=consts.SOUNDS_FOLDER))
        cls.mine_hit_sound = pg.mixer.Sound(file_name_get(name='snd_mine_hit', folder=consts.SOUNDS_FOLDER))
        cls.weapon_empty_sound = pg.mixer.Sound(file_name_get(name='snd_weapon_empty', folder=consts.SOUNDS_FOLDER))

    @classmethod
    def render_text_frequently_used(cls, game):
        libg_jp.render_text('– PAUSED –', Settings.screen_width // 2, Settings.screen_height // 4.6,
                            cls.txt_surfaces, 'game_paused', color=Color.CYAN,
                            size=int(70*Settings.font_pos_factor), align="center")

        libg_jp.render_text('– Press Escape to Exit this Game  –', Settings.screen_width // 2,
                            (Settings.screen_height // 2.6) - int(6 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'exit_current_game_confirm', color=Color.CYAN,
                            size=int(78*Settings.font_pos_factor_t2), align="center")

        libg_jp.render_text("GAME OVER", Settings.screen_width // 1.99,
                            Settings.screen_height // 2.484,
                            cls.txt_surfaces, 'game_over', color=Color.BLUE,
                            size=int(120*Settings.font_pos_factor), align="center")
        libg_jp.render_text("GAME OVER", Settings.screen_width // 2,
                            Settings.screen_height // 2.5,
                            cls.txt_surfaces, 'game_over_2', color=Color.CYAN,
                            size=int(120*Settings.font_pos_factor), align="center")

        libg_jp.render_text('– Press Ctrl + Enter to Continue –', Settings.screen_width // 1.992,
                            (Settings.screen_height // 1.752) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue', color=Color.BLUE,
                            size=int(68*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('– Press Ctrl + Enter to Continue –', Settings.screen_width // 2,
                            (Settings.screen_height // 1.76) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue_2', color=Color.CYAN,
                            size=int(68*Settings.font_pos_factor_t2), align="center")

        libg_jp.render_text("KUDOS", Settings.screen_width // 1.99,
                            Settings.screen_height // 2.484,
                            cls.txt_surfaces, 'congrats', color=Color.BLUE,
                            size=int(150*Settings.font_pos_factor), align="center")
        libg_jp.render_text("KUDOS", Settings.screen_width // 2,
                            Settings.screen_height // 2.5,
                            cls.txt_surfaces, 'congrats_2', color=Color.CYAN,
                            size=int(150*Settings.font_pos_factor), align="center")

        libg_jp.render_text('You have beaten the game', Settings.screen_width // 1.991,
                            (Settings.screen_height // 1.356) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'you_have_beaten_the_game', color=Color.BLUE,
                            size=int(82*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('You have beaten the game', Settings.screen_width // 2,
                            (Settings.screen_height // 1.36) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'you_have_beaten_the_game_2', color=Color.CYAN,
                            size=int(82*Settings.font_pos_factor_t2), align="center")

    @classmethod
    def load_and_render_background_images(cls):
        """Load and render background images and effects."""
        img = pg.Surface((Settings.screen_width, Settings.screen_height)).convert_alpha()
        img.fill((0, 0, 0, 55))
        cls.images['dim_screen'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_background', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['background'] = img

        img = pg.image.load(file_name_get(folder=consts.BITMAPS_FOLDER,
                                          name='seal_just_a_demo', subname='')).convert()
        img = pg.transform.smoothscale(img, (960 // 1.7, 56 // 1.7))
        cls.images['seal_just_a_demo'] = img

        img = pg.image.load(file_name_get(folder=consts.BITMAPS_FOLDER,
                                          name='seal_tutorial', subname='')).convert()
        img = pg.transform.smoothscale(img, (327 // 1.5, 80 // 1.5))
        cls.images['seal_tutorial'] = img

        img = pg.image.load(file_name_get(folder=consts.BITMAPS_FOLDER,
                                          name='seal_cutscene', subname='')).convert()
        img = pg.transform.smoothscale(img, (327 // 1.8, 80 // 1.8))
        cls.images['seal_cutscene'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_bg_score_bar', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width,
                                             int(Settings.screen_near_top // 1.9)))
        cls.images['background_score_bar'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_bg_score_bar2', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_near_top))
        cls.images['background_score_bar2'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='bg_blue_t1_big_logo', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_blue_t1'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_bg_blue_', subname='t2')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_blue_t2'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_bg_black_', subname='t1')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_black_t1'] = img

        img = pg.image.load(file_name_get(name=Settings.im_screen_help,
                                          subname='', num=1)).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width_adjusted,
                                             Settings.screen_height_adjusted))
        cls.images['screen_help'] = img

        img = pg.image.load(file_name_get(name=Settings.im_bg_start_game,
                                          subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width_adjusted,
                                             Settings.screen_height_adjusted))
        cls.images['screen_start'] = img

        cls.images['help_key'] = pg.image.load(
            file_name_get(name='im_help_key', subname='')).convert()

        cls.images['logo_jp'] = pg.image.load(file_name_get(
            folder=consts.BM_LOGOS_FOLDER,
            name='im_logo_japinol', subname='')).convert()

    @classmethod
    def load_and_render_scorebar_images_and_txt(cls):
        img = pg.image.load(file_name_get(folder=consts.BM_LIVES_BASE_FOLDER,
                                          name='life_heart',
                                          quality='', num=1)).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_apples_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_lives_title1'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BATTERIES_FOLDER,
                                          name='im_batteries', num=1,
                                          subnum=1)).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_batteries_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_batteries_title'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_APPLES_FOLDER,
                                          name='im_apples',
                                          quality='_t1', num=1)).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_apples_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_apples_title'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_POTION_HEALTH_FOLDER,
                                          name='im_potion_health', num=1,
                                          quality='_t1')).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_batteries_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_potions_health_title'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_POTION_POWER_FOLDER,
                                          name='im_potion_power', num=1,
                                          quality='_t1')).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_batteries_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_potions_power_title'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_LEVELS_FOLDER,
                                          name='im_level_completed',
                                          quality='')).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_apples_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_level_completed'] = img
        img = pg.image.load(file_name_get(folder=consts.BM_MISC_FOLDER,
                                          name='im_magic_activated',
                                          quality='')).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_apples_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_magic_activated'] = img
        img = pg.image.load(file_name_get(folder=consts.BM_DOOR_KEYS_FOLDER,
                                          name='im_door_keys',
                                          num=2, subnum=1)).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_door_keys_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_door_keys_title'] = img

        bullets_stats = ['sb_bullets_t1', 'sb_bullets_t2', 'sb_bullets_t3', 'sb_bullets_t4']
        for bullet_stats in bullets_stats:
            img = pg.image.load(file_name_get(folder=consts.BM_BULLETS_FOLDER,
                                              name='im_bullet_', subname=bullet_stats[-2:],
                                              quality='_md', num=1)).convert()
            img = pg.transform.smoothscale(img, Settings.score_pos_bullets_size)
            img.set_colorkey(Color.BLACK)
            cls.images[bullet_stats] = img

        f_disks_stats = ['sb_f_disks_t1', 'sb_f_disks_t2', 'sb_f_disks_t3', 'sb_f_disks_t4']
        for i, f_disks_stats in enumerate(f_disks_stats, start=1):
            img = pg.image.load(file_name_get(folder=consts.BM_FILE_DISKS_FOLDER,
                                              name='im_files_disks',
                                              num=i, subnum=1)).convert()
            img = pg.transform.smoothscale(img, Settings.score_pos_f_disks_size)
            img.set_colorkey(Color.BLACK)
            cls.images[f_disks_stats] = img

        libg_jp.render_text('XP:', Settings.score_pos_score1[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_score_title1', color=Color.CYAN)
        libg_jp.render_text('#', Settings.score_pos_level[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_level_title', color=Color.CYAN)

        libg_jp.render_text('L:', Settings.score_pos_pc_level[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_pc_level_title', color=Color.CYAN)

    @staticmethod
    def load_music_song(current_song):
        pg.mixer.music.load(os.path.join(consts.MUSIC_FOLDER, consts.MUSIC_BOX[current_song]))
