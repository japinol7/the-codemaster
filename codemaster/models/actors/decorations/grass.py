"""Module grass."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_PLAT_GRASS
from codemaster.models.actors.actor_types import (
    ActorBaseType,
    ActorCategoryType,
    ActorType,
    )
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats

PLAT_GRASS_WIDTH = 216
PLAT_GRASS_HEIGHT = 72

PLAT_GRASS_SM_WIDTH = 140
PLAT_GRASS_SM_HEIGHT = 62
PLAT_GRASS_SM_DEEP_HEIGHT = 33


class Grass(ActorItem):
    """Represents a block of grass.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_PLAT_GRASS
        self.file_name_key = 'im_grass'
        self.transparency_alpha = True
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.base_type = ActorBaseType.GRASS
        self.category_type = ActorCategoryType.DECORATION

        super().__init__(x, y, game, name=name)


    def update_when_hit(self):
        """A block of grass cannot be hit."""
        pass

    @staticmethod
    def create_grass(x, y, game, qty, qty_depth, actor_type=ActorType.PLAT_GRASS_A):
        xx, yy = x, y - 35
        add_to_list = getattr(game.level_init, 'decors')
        for _ in range(qty):
            add_to_list.add(
                GRASS_TYPE_MAP[actor_type][0](xx, yy, game)
                )
            xx += PLAT_GRASS_WIDTH
        for ii in range(qty_depth):
            xx = x
            yy += PLAT_GRASS_HEIGHT
            for i in range(qty):
                if ii == qty_depth - 1 and i == 0:
                    map_image_index = 1  # start
                elif ii == qty_depth - 1 and i == qty - 1:
                    map_image_index = 3  # end
                else:
                    map_image_index = 2  # middle
                add_to_list.add(
                    GRASS_TYPE_MAP[actor_type][map_image_index](xx, yy, game)
                    )
                xx += PLAT_GRASS_WIDTH

    @staticmethod
    def create_grass_sm(x, y, game, qty, qty_depth, actor_type=ActorType.PLAT_GRASS_A):
        """create grass small"""
        xx, yy = x, y - 35
        add_to_list = getattr(game.level_init, 'decors')
        for _ in range(qty):
            add_to_list.add(
                GRASS_TYPE_MAP[actor_type][0](xx, yy, game)
                )
            xx += PLAT_GRASS_SM_WIDTH
        for ii in range(qty_depth):
            xx = x
            yy += PLAT_GRASS_SM_HEIGHT if ii == 0 else PLAT_GRASS_SM_DEEP_HEIGHT
            for i in range(qty):
                if ii == qty_depth - 1 and i == 0:
                    map_image_index = 1    # start
                elif ii == qty_depth - 1 and i == qty - 1:
                    map_image_index = 3    # end
                else:
                    map_image_index = 2    # middle
                add_to_list.add(
                    GRASS_TYPE_MAP[actor_type][map_image_index](xx, yy, game)
                    )
                xx += PLAT_GRASS_SM_WIDTH


class GrassA(Grass):
    """Represents a superficial block of grass A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_A
        super().__init__(x, y, game, name=name)


class GrassADeepStart(Grass):
    """Represents a deep block of grass A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_A_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassADeep(Grass):
    """Represents a deep block of grass A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_A_DEEP
        super().__init__(x, y, game, name=name)


class GrassADeepEnd(Grass):
    """Represents a deep block of grass A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_A_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassB(Grass):
    """Represents a superficial block of grass B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_B
        super().__init__(x, y, game, name=name)


class GrassBDeepStart(Grass):
    """Represents a deep block of grass B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_B_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassBDeep(Grass):
    """Represents a deep block of grass B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_B_DEEP
        super().__init__(x, y, game, name=name)


class GrassBDeepEnd(Grass):
    """Represents a deep block of grass B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_B_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassC(Grass):
    """Represents a superficial block of grass C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '03'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_C
        super().__init__(x, y, game, name=name)


class GrassCDeepStart(Grass):
    """Represents a deep block of grass C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '03_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_C_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassCDeep(Grass):
    """Represents a deep block of grass C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '03_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_C_DEEP
        super().__init__(x, y, game, name=name)


class GrassCDeepEnd(Grass):
    """Represents a deep block of grass C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '03_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_C_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassD(Grass):
    """Represents a superficial block of grass D."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '04'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_D
        super().__init__(x, y, game, name=name)


class GrassDDeepStart(Grass):
    """Represents a deep block of grass D."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '04_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_D_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassDDeep(Grass):
    """Represents a deep block of grass D."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '04_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_D_DEEP
        super().__init__(x, y, game, name=name)


class GrassDDeepEnd(Grass):
    """Represents a deep block of grass D."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '04_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_D_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassEwSM(Grass):
    """Represents a superficial block of grass E SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '05_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_E_SM
        super().__init__(x, y, game, name=name)


class GrassEwSMDeepStart(Grass):
    """Represents a deep block of grass E SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '05_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_E_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassEwSMDeep(Grass):
    """Represents a deep block of grass E SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '05_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_E_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassEwSMDeepEnd(Grass):
    """Represents a deep block of grass E SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '05_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_E_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassFwSM(Grass):
    """Represents a superficial block of grass F SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '06_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_F_SM
        super().__init__(x, y, game, name=name)


class GrassFwSMDeepStart(Grass):
    """Represents a deep block of grass F SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '06_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_F_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassFwSMDeep(Grass):
    """Represents a deep block of grass F SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '06_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_F_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassFwSMDeepEnd(Grass):
    """Represents a deep block of grass F SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '06_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_F_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassGwSM(Grass):
    """Represents a superficial block of grass G SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '07_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM
        super().__init__(x, y, game, name=name)


class GrassGwSMDeepStart(Grass):
    """Represents a deep block of grass G SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '07_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassGwSMDeep(Grass):
    """Represents a deep block of grass G SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '07_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassGwSMDeepEnd(Grass):
    """Represents a deep block of grass G SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '07_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassHwSM(Grass):
    """Represents a superficial block of grass H SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '08_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM
        super().__init__(x, y, game, name=name)


class GrassHwSMDeepStart(Grass):
    """Represents a deep block of grass H SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '08_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassHwSMDeep(Grass):
    """Represents a deep block of grass H SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '08_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassHwSMDeepEnd(Grass):
    """Represents a deep block of grass H SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '08_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassJwSM(Grass):
    """Represents a superficial block of grass J SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '09_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_J_SM
        super().__init__(x, y, game, name=name)


class GrassJwSMDeepStart(Grass):
    """Represents a deep block of grass J SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '09_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_J_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassJwSMDeep(Grass):
    """Represents a deep block of grass J SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '09_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_J_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassJwSMDeepEnd(Grass):
    """Represents a deep block of grass J SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '09_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_J_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassKwSM(Grass):
    """Represents a superficial block of grass K SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '10_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_K_SM
        super().__init__(x, y, game, name=name)


class GrassKwSMDeepStart(Grass):
    """Represents a deep block of grass K SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '10_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_K_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassKwSMDeep(Grass):
    """Represents a deep block of grass K SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '10_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_K_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassKwSMDeepEnd(Grass):
    """Represents a deep block of grass K SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '10_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_K_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassLwSM(Grass):
    """Represents a superficial block of grass L SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '11_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_L_SM
        super().__init__(x, y, game, name=name)


class GrassLwSMDeepStart(Grass):
    """Represents a deep block of grass L SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '11_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_L_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassLwSMDeep(Grass):
    """Represents a deep block of grass L SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '11_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_L_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassLwSMDeepEnd(Grass):
    """Represents a deep block of grass L SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '11_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_L_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassMwSM(Grass):
    """Represents a superficial block of grass M SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '12_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_M_SM
        super().__init__(x, y, game, name=name)


class GrassMwSMDeepStart(Grass):
    """Represents a deep block of grass M SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '12_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_M_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassMwSMDeep(Grass):
    """Represents a deep block of grass M SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '12_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_M_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassMwSMDeepEnd(Grass):
    """Represents a deep block of grass M SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '12_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_M_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassOwSM(Grass):
    """Represents a superficial block of grass O SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '13_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_O_SM
        super().__init__(x, y, game, name=name)


class GrassOwSMDeepStart(Grass):
    """Represents a deep block of grass O SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '13_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_O_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassOwSMDeep(Grass):
    """Represents a deep block of grass O SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '13_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_O_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassOwSMDeepEnd(Grass):
    """Represents a deep block of grass O SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '13_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_O_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassP(Grass):
    """Represents a superficial block of grass P."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '14'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_P
        super().__init__(x, y, game, name=name)


class GrassPDeepStart(Grass):
    """Represents a deep block of grass P."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '14_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_P_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassPDeep(Grass):
    """Represents a deep block of grass P."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '14_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_P_DEEP
        super().__init__(x, y, game, name=name)


class GrassPDeepEnd(Grass):
    """Represents a deep block of grass P."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '14_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_P_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassQ(Grass):
    """Represents a superficial block of grass Q."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '15'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_Q
        super().__init__(x, y, game, name=name)


class GrassQDeepStart(Grass):
    """Represents a deep block of grass Q."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '15_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_Q_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassQDeep(Grass):
    """Represents a deep block of grass Q."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '15_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_Q_DEEP
        super().__init__(x, y, game, name=name)


class GrassQDeepEnd(Grass):
    """Represents a deep block of grass Q."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '15_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_Q_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassR(Grass):
    """Represents a superficial block of grass R."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '16'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_R
        super().__init__(x, y, game, name=name)


class GrassRDeepStart(Grass):
    """Represents a deep block of grass R."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '16_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_R_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassRDeep(Grass):
    """Represents a deep block of grass R."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '16_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_R_DEEP
        super().__init__(x, y, game, name=name)


class GrassRDeepEnd(Grass):
    """Represents a deep block of grass R."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '16_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_R_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassSwSM(Grass):
    """Represents a superficial block of grass S SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '17_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_S_SM
        super().__init__(x, y, game, name=name)


class GrassSwSMDeepStart(Grass):
    """Represents a deep block of grass S SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '17_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_S_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassSwSMDeep(Grass):
    """Represents a deep block of grass S SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '17_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_S_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassSwSMDeepEnd(Grass):
    """Represents a deep block of grass S SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '17_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_S_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassTwSM(Grass):
    """Represents a superficial block of grass T SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '18_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_T_SM
        super().__init__(x, y, game, name=name)


class GrassTwSMDeepStart(Grass):
    """Represents a deep block of grass T SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '18_sm_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_T_SM_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassTwSMDeep(Grass):
    """Represents a deep block of grass T SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '18_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_T_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassTwSMDeepEnd(Grass):
    """Represents a deep block of grass T SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '18_sm_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_T_SM_DEEP_END
        super().__init__(x, y, game, name=name)


class GrassU(Grass):
    """Represents a superficial block of grass U."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '19'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_U
        super().__init__(x, y, game, name=name)


class GrassUDeepStart(Grass):
    """Represents a deep block of grass U."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '19_deep_start'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_U_DEEP_ST
        super().__init__(x, y, game, name=name)


class GrassUDeep(Grass):
    """Represents a deep block of grass U."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '19_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_U_DEEP
        super().__init__(x, y, game, name=name)


class GrassUDeepEnd(Grass):
    """Represents a deep block of grass U."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '19_deep_end'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_U_DEEP_END
        super().__init__(x, y, game, name=name)


GRASS_TYPE_MAP = {
    ActorType.PLAT_GRASS_A: (GrassA, GrassADeepStart, GrassADeep, GrassADeepEnd),
    ActorType.PLAT_GRASS_B: (GrassB, GrassBDeepStart, GrassBDeep, GrassBDeepEnd),
    ActorType.PLAT_GRASS_C: (GrassC, GrassCDeepStart, GrassCDeep, GrassCDeepEnd),
    ActorType.PLAT_GRASS_D: (GrassD, GrassDDeepStart, GrassDDeep, GrassDDeepEnd),
    ActorType.PLAT_GRASS_E_SM: (GrassEwSM, GrassEwSMDeepStart, GrassEwSMDeep, GrassEwSMDeepEnd),
    ActorType.PLAT_GRASS_F_SM: (GrassFwSM, GrassFwSMDeepStart, GrassFwSMDeep, GrassFwSMDeepEnd),
    ActorType.PLAT_GRASS_G_SM: (GrassGwSM, GrassGwSMDeepStart, GrassGwSMDeep, GrassGwSMDeepEnd),
    ActorType.PLAT_GRASS_H_SM: (GrassHwSM, GrassHwSMDeepStart, GrassHwSMDeep, GrassHwSMDeepEnd),
    ActorType.PLAT_GRASS_J_SM: (GrassJwSM, GrassJwSMDeepStart, GrassJwSMDeep, GrassJwSMDeepEnd),
    ActorType.PLAT_GRASS_K_SM: (GrassKwSM, GrassKwSMDeepStart, GrassKwSMDeep, GrassKwSMDeepEnd),
    ActorType.PLAT_GRASS_L_SM: (GrassLwSM, GrassLwSMDeepStart, GrassLwSMDeep, GrassLwSMDeepEnd),
    ActorType.PLAT_GRASS_M_SM: (GrassMwSM, GrassMwSMDeepStart, GrassMwSMDeep, GrassMwSMDeepEnd),
    ActorType.PLAT_GRASS_O_SM: (GrassOwSM, GrassOwSMDeepStart, GrassOwSMDeep, GrassOwSMDeepEnd),
    ActorType.PLAT_GRASS_P: (GrassP, GrassPDeepStart, GrassPDeep, GrassPDeepEnd),
    ActorType.PLAT_GRASS_Q: (GrassQ, GrassQDeepStart, GrassQDeep, GrassQDeepEnd),
    ActorType.PLAT_GRASS_R: (GrassR, GrassRDeepStart, GrassRDeep, GrassRDeepEnd),
    ActorType.PLAT_GRASS_S_SM: (GrassSwSM, GrassSwSMDeepStart, GrassSwSMDeep, GrassSwSMDeepEnd),
    ActorType.PLAT_GRASS_T_SM: (GrassTwSM, GrassTwSMDeepStart, GrassTwSMDeep, GrassTwSMDeepEnd),
    ActorType.PLAT_GRASS_U: (GrassU, GrassUDeepStart, GrassUDeep, GrassUDeepEnd),
    }
