"""Module robots."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.config.constants import BM_NPCS_FOLDER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.actors.items.bullets import BulletType
from codemaster.models.stats import Stats


class Robot(NPC):
    """Represents a Robot.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_robots'
        self.images_sprite_no = 1
        self.can_shot = True
        self.bullet_start_position_delta_x = 14
        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class RobotB(Robot):
    """Represents a Robot B."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.ROBOT_B

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 5
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 6
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_shots = self.time_between_shots_base / 2.6
        self.shot_x_delta_max = self.shot_x_delta_max + 150

    def update_shot_bullet_fire_shots(self):
        if randint(1, 100) + 50 >= 100:
            self.shot_bullet(BulletType.T1_LASER1)
        else:
            self.shot_bullet(BulletType.T2_LASER2)


class RobotA(Robot):
    """Represents a Robot A."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.ROBOT_A

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 4
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 5
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_shots = self.time_between_shots_base / 2.6
        self.shot_x_delta_max = self.shot_x_delta_max + 150

    def update_shot_bullet_fire_shots(self):
        dice = randint(1, 100)
        if dice + 8 >= 100:
            self.shot_bullet(BulletType.T3_PHOTONIC)
        elif dice + 40 >= 100:
            self.shot_bullet(BulletType.T2_LASER2)
        else:
            self.shot_bullet(BulletType.T1_LASER1)
