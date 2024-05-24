"""Module score_bars."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.tools.utils.colors import Color
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.models.actors.actor_types import ActorType


class ScoreBar:
    """Represents a score bar."""

    def __init__(self, game, screen):
        self.game = game
        self.player = game.player
        self.screen = screen
        self.level_no = None
        self.level_no_old = None

    def draw_chars_render_text(self, text, x, y, color=Color.YELLOW):
        libg_jp.draw_text_rendered(text, x, y, self.screen, color)

    def render_stats_if_necessary(self, x, y, stats_name):
        # player stats
        libg_jp.draw_text_rendered(text=f'{self.player.stats[stats_name]}',
                                        x=x, y=y, screen=self.screen, color=Color.GREEN)
        if self.player.stats[stats_name] != self.player.stats_old[stats_name]:
            self.player.stats_old[stats_name] = self.player.stats[stats_name]

    def draw_stats(self):
        # Draw player score titles
        self.screen.blit(*Resource.txt_surfaces['sb_level_title'])
        self.screen.blit(Resource.images['sb_lives_title1'],
                         (Settings.score_pos_lives1[0], Settings.score_pos_lives_y))
        self.screen.blit(Resource.images['sb_batteries_title'],
                         (Settings.score_pos_batteries1[0], Settings.score_pos_batteries1_y))
        self.screen.blit(Resource.images['sb_apples_title'],
                         (Settings.score_pos_apples1[0], Settings.score_pos_apples_y - 5))
        self.screen.blit(*Resource.txt_surfaces['sb_score_title1'])

        self.screen.blit(Resource.images['sb_potions_health_title'],
                         (Settings.score_pos_potions_health[0], Settings.score_pos_potions_health_y - 2))
        self.screen.blit(Resource.images['sb_potions_power_title'],
                         (Settings.score_pos_potions_power[0], Settings.score_pos_potions_power_y - 2))
        self.screen.blit(Resource.images['sb_door_keys_title'],
                         (Settings.score_pos_apples1[0] + 301, Settings.score_pos_apples_y - 5))

        bullet_pos_x = 150
        bullets_stats = ['sb_bullets_t1', 'sb_bullets_t2', 'sb_bullets_t3', 'sb_bullets_t4']
        for bullet_stats in bullets_stats:
            self.screen.blit(Resource.images[bullet_stats],
                             (bullet_pos_x * Settings.font_pos_factor,
                              int(Settings.score_pos_bullets_size[1]
                                  + Settings.score_pos_bullets_y)))
            bullet_pos_x += 85

        f_disk_pos_x = 745
        f_disks_stats = ['sb_f_disks_t1', 'sb_f_disks_t2', 'sb_f_disks_t3', 'sb_f_disks_t4']
        for f_disks_stats in f_disks_stats:
            self.screen.blit(Resource.images[f_disks_stats],
                             (f_disk_pos_x * Settings.font_pos_factor,
                              Settings.score_pos_f_disks_y))
            f_disk_pos_x += 112


        if self.game.level.completed:
            self.screen.blit(Resource.images['sb_level_completed'],
                             (Settings.score_pos_apples1[0] - 130, Settings.score_pos_apples_y - 6))

        if self.game.is_magic_on:
            self.screen.blit(Resource.images['sb_magic_activated'],
                             (Settings.score_pos_apples1[0] + 410, Settings.score_pos_apples_y - 6))

        self.screen.blit(*Resource.txt_surfaces['sb_pc_level_title'])

        # Draw score stats and render them if needed
        self.render_stats_if_necessary(Settings.score_pos_lives1[1],
                                       Settings.screen_bar_near_top, 'lives')
        self.render_stats_if_necessary(Settings.score_pos_batteries1[1],
                                       Settings.screen_bar_near_top, 'batteries')

        self.render_stats_if_necessary(Settings.score_pos_score1[1],
                                       Settings.screen_bar_near_top, 'score')
        self.render_stats_if_necessary(Settings.score_pos_apples1[1],
                                       (Settings.score_pos_apples_y - 2) * Settings.font_pos_factor, 'apples')

        self.render_stats_if_necessary(Settings.score_pos_potions_health[1],
                                       Settings.score_pos_potions_health_y * Settings.font_pos_factor,
                                       ActorType.POTION_HEALTH.name)
        self.render_stats_if_necessary(Settings.score_pos_potions_power[1],
                                       Settings.score_pos_potions_power_y * Settings.font_pos_factor,
                                       ActorType.POTION_POWER.name)

        self.render_stats_if_necessary(Settings.score_pos_door_keys[1],
                                       (Settings.score_pos_apples_y - 2) * Settings.font_pos_factor, 'door_keys')

        self.render_stats_if_necessary(Settings.score_pos_door_keys[1],
                                       (Settings.score_pos_apples_y - 2) * Settings.font_pos_factor, 'door_keys')

        self.render_stats_if_necessary(Settings.score_pos_pc_level[1],
                                       Settings.screen_bar_near_top, 'level')

        bullet_pos_x = 179
        bullets_stats = ['bullets_t01', 'bullets_t02', 'bullets_t03', 'bullets_t04']
        for bullet_stats in bullets_stats:
            self.render_stats_if_necessary(
                bullet_pos_x * Settings.font_pos_factor,
                Settings.score_pos_bullets_y + 10 * Settings.font_pos_factor,
                bullet_stats)
            bullet_pos_x += 83

        f_disk_pos_x = 790
        f_disks_stats = [ActorType.FILES_DISK_D.name, ActorType.FILES_DISK_C.name,
                         ActorType.FILES_DISK_B.name, ActorType.FILES_DISK_A.name]
        for f_disk_stats in f_disks_stats:
            self.render_stats_if_necessary(
                f_disk_pos_x * Settings.font_pos_factor,
                Settings.score_pos_f_disks_y + 5 * Settings.font_pos_factor,
                f_disk_stats)
            f_disk_pos_x += 112

        libg_jp.draw_text_rendered(
            text=f'{self.level_no + 1}',
            x=Settings.score_pos_level[1],
            y=Settings.screen_bar_near_top,
            screen=self.screen, color=Color.CYAN)

    def update(self, level_no, level_no_old):
        self.level_no = level_no
        self.level_no_old = level_no_old
        libg_jp.draw_bar_graphic(
            self.screen, amount_pct=self.player.health / self.player.health_total,
            x=Settings.score_pos_health1_xy[0], y=Settings.score_pos_health1_xy[1],
            bar_width=Settings.score_pos_health_size[0],
            bar_height=Settings.score_pos_health_size[1])

        libg_jp.draw_bar_graphic(
            self.screen, amount_pct=self.player.power / self.player.power_total,
            x=Settings.score_pos_health1_xy[0],
            y=Settings.score_pos_health1_xy[1] + 39 * Settings.font_pos_factor,
            bar_width=Settings.score_pos_power_size[0],
            bar_height=Settings.score_pos_power_size[1],
            color_max=Color.BLUE, color_med=Color.BLUE_VIOLET, color_min=Color.CYAN)
        self.draw_stats()
