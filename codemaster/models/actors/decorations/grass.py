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
        for __ in range(qty_depth):
            xx = x
            yy += PLAT_GRASS_HEIGHT
            for _ in range(qty):
                add_to_list.add(
                    GRASS_TYPE_MAP[actor_type][1](xx, yy, game)
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
        for i in range(qty_depth):
            xx = x
            yy += PLAT_GRASS_SM_HEIGHT if i == 0 else PLAT_GRASS_SM_DEEP_HEIGHT
            for _ in range(qty):
                add_to_list.add(
                    GRASS_TYPE_MAP[actor_type][1](xx, yy, game)
                    )
                xx += PLAT_GRASS_SM_WIDTH


class GrassA(Grass):
    """Represents a superficial block of grass A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_A
        super().__init__(x, y, game, name=name)


class GrassADeep(Grass):
    """Represents a deep block of grass A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_A_DEEP
        super().__init__(x, y, game, name=name)


class GrassB(Grass):
    """Represents a superficial block of grass B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_B
        super().__init__(x, y, game, name=name)


class GrassBDeep(Grass):
    """Represents a deep block of grass B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_B_DEEP
        super().__init__(x, y, game, name=name)


class GrassC(Grass):
    """Represents a superficial block of grass C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_C
        super().__init__(x, y, game, name=name)


class GrassCDeep(Grass):
    """Represents a deep block of grass C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_C_DEEP
        super().__init__(x, y, game, name=name)


class GrassEwSM(Grass):
    """Represents a superficial block of grass E SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '05_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_E_SM
        super().__init__(x, y, game, name=name)


class GrassEwSMDeep(Grass):
    """Represents a deep block of grass E SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '05_sm_deep'
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


class GrassFwSMDeep(Grass):
    """Represents a deep block of grass F SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '06_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_F_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassGwSM(Grass):
    """Represents a superficial block of grass G SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '07_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM
        super().__init__(x, y, game, name=name)


class GrassGwSMDeep(Grass):
    """Represents a deep block of grass G SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '07_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassHwSM(Grass):
    """Represents a superficial block of grass H SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '08_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM
        super().__init__(x, y, game, name=name)


class GrassHwSMDeep(Grass):
    """Represents a deep block of grass H SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '08_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_G_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassJwSM(Grass):
    """Represents a superficial block of grass J SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '09_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_J_SM
        super().__init__(x, y, game, name=name)


class GrassJwSMDeep(Grass):
    """Represents a deep block of grass J SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '09_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_J_SM_DEEP
        super().__init__(x, y, game, name=name)


class GrassKwSM(Grass):
    """Represents a superficial block of grass K SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '10_sm'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_K_SM
        super().__init__(x, y, game, name=name)


class GrassKwSMDeep(Grass):
    """Represents a deep block of grass K SM."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '10_sm_deep'
        self.images_sprite_no = 1
        self.type = ActorType.PLAT_GRASS_K_SM_DEEP
        super().__init__(x, y, game, name=name)


GRASS_TYPE_MAP = {
    ActorType.PLAT_GRASS_A: (GrassA, GrassADeep),
    ActorType.PLAT_GRASS_B: (GrassB, GrassBDeep),
    ActorType.PLAT_GRASS_C: (GrassC, GrassCDeep),
    ActorType.PLAT_GRASS_E_SM: (GrassEwSM, GrassEwSMDeep),
    ActorType.PLAT_GRASS_F_SM: (GrassFwSM, GrassFwSMDeep),
    ActorType.PLAT_GRASS_G_SM: (GrassGwSM, GrassGwSMDeep),
    ActorType.PLAT_GRASS_H_SM: (GrassHwSM, GrassHwSMDeep),
    ActorType.PLAT_GRASS_J_SM: (GrassJwSM, GrassJwSMDeep),
    ActorType.PLAT_GRASS_K_SM: (GrassKwSM, GrassKwSMDeep),
    }
