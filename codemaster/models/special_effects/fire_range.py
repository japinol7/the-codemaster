"""Module fire_range."""
__author__ = 'Joan A. Pinol  (japinol)'

import math

from codemaster.models.special_effects.vortex import (
    COLOR_TRANSP_RATIO_DEFAULT,
    VORTEX_SCALE_DEFAULT,
    Vortex,
    VortexDrawMethod,
    )
from codemaster.tools.utils.colors import Color


class FireRange(Vortex):
    """Represents a fire range."""

    def __init__(self, position, angle, speed, color=Color.WHITE,
                 color_transparency_ratio=COLOR_TRANSP_RATIO_DEFAULT,
                 scale=VORTEX_SCALE_DEFAULT,
                 draw_method=VortexDrawMethod.CIRCLE,
                 type_base='SPARK_FR_',
                 angle_acceleration=0.14, speed_acceleration=0.08):

        super().__init__(
            position, angle, speed, color, color_transparency_ratio, scale,
            draw_method, type_base, angle_acceleration, speed_acceleration)

    def calc_move(self, dt):
        return (math.cos(self.angle * self.angle / 2) * self.speed * dt,
                math.sin(self.angle * self.angle / 2) * self.speed * dt)
