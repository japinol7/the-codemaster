"""Module light."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter
import math
import random

import pygame as pg

from codemaster.tools.utils.colors import Color
from codemaster.config.constants import BM_LIGHTS_FOLDER
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.models.actors.actors import Actor


COLOR_TRANSP_RATIO_DEFAULT = 0.2


class Light:
    """Represents a light. It is expected to be rendered in a light grid."""
    sprite_image = None
    type_id_count = Counter()

    def __init__(self, position, radius, color=Color.WHITE, alpha=255,
                 color_transparency_ratio=COLOR_TRANSP_RATIO_DEFAULT):
        self.type = 'LIGHT_' + ''.join([f'{x:03d}' for x in color])
        Light.type_id_count[self.type] += 1
        self.id = f"{self.type}_{Light.type_id_count[self.type]:05d}"

        self.color_transparency_ratio = color_transparency_ratio
        self.color = [x * color_transparency_ratio for x in color]

        self._base_surface_size = radius
        self.position = position
        self.radius = radius
        self.radius_variance = 0
        self.variance_size = self._base_surface_size // 32

        self.file_name_key = 'im_lights'
        self.file_mid_prefix = '01'
        self._load_image()
        self._light_img_base = pg.transform.scale(self.__class__.sprite_image, (radius * 2, radius * 2))
        self._colored_light_img = self._light_img_base.copy()
        self.light_img = self._light_img_base.copy()

        self.alpha = alpha
        self.alpha_color = (alpha, alpha, alpha)
        self.timer = 1
        self.timer_flicker = 1

        self._calculate_light_image()

    def _load_image(self):
        if not self.__class__.sprite_image:
            self.__class__.sprite_image = pg.image.load(Actor.file_name_im_get(
                    BM_LIGHTS_FOLDER, self.file_name_key,
                    self.file_mid_prefix, suffix_index=1
                    )).convert()

    def update(self):
        base_size = self._base_surface_size
        self.timer += 1
        self.set_size(int((1 + math.sin(self.timer / 10)) + (base_size + self.radius_variance)))
        self.timer_flicker -= 1

        if self.timer_flicker < 0:
            self._calculate_flicker_effect(base_size)

    def _calculate_light_image(self):
        self._colored_light_img = libg_jp.multiply_color_on_surface(
                libg_jp.set_mask_alpha(self._light_img_base, self.alpha), self.color)
        self.light_img = self._colored_light_img.copy()

    def _calculate_flicker_effect(self, base_size):
        self.radius_variance = random.randint(-self.variance_size, self.variance_size)
        radius = base_size + self.radius_variance
        self.set_size(radius)

        alpha_variance = int(self.radius_variance)
        self.set_alpha(max(0, min(255, self.alpha + alpha_variance)))
        self.timer_flicker = random.randint(20, 50)

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.alpha_color = (alpha, alpha, alpha)
        self._colored_light_img = libg_jp.set_mask_alpha(self._light_img_base, self.alpha_color)
        self.set_size(self.radius)

    def set_color(self, color, override_alpha=False, color_transparency_ratio=COLOR_TRANSP_RATIO_DEFAULT):
        self.color_transparency_ratio = color_transparency_ratio
        self.color = [x * color_transparency_ratio for x in color]
        if override_alpha:
            # Do not calculate alpha for performance reasons
            self._colored_light_img = libg_jp.multiply_color_on_surface(self._light_img_base, self.color)
        else:
            self._calculate_light_image()
        self.set_size(self.radius)

    def set_size(self, radius):
        self.radius = radius
        self.light_img = pg.transform.scale(self._colored_light_img, (radius * 2, radius * 2))


class LightGrid:
    """Represents a light grid to handle the processing of Lights."""

    def __init__(self, size, blit_flags=None):
        self.lights = {}
        self.light_count = 0
        self.grid_rect = pg.Rect(0, 0, size[0], size[1])
        self.light_id = 0
        self.blit_flags = blit_flags or pg.BLEND_RGBA_ADD

    def add_light(self, light):
        self.light_id += 1
        self.light_count += 1
        self.lights[str(self.light_id)] = light
        return str(self.light_id)

    def get_light(self, light_id):
        return self.lights[light_id]

    def delete_light(self, light_id):
        self.light_count -= 1
        del self.lights[light_id]

    def get_max_light_radius(self):
        max_radius = 0
        for light in self.lights:
            max_radius = max(max_radius, self.lights[light].radius)
        return max_radius

    def render(self, target_surface, offset=None):
        if offset is None:
            offset = (0, 0)

        max_radius = self.get_max_light_radius()
        render_grid = pg.Rect(
            -max_radius, -max_radius,
            self.grid_rect.width + max_radius * 2, self.grid_rect.height + max_radius * 2)

        mask_surf_rendered = pg.Surface(self.grid_rect.size)
        for light in self.lights.values():
            # Calculate the offset of the base surface
            light_pos = [light.position[0] - offset[0], light.position[1] - offset[1]]

            if render_grid.collidepoint(light_pos):
                # Calculate visible light
                light_instance_surf = light.light_img.copy()
                light_offset = light_pos[0] - light.radius, light_pos[1] - light.radius
                mask_surf_rendered.blit(light_instance_surf, light_offset, special_flags=pg.BLEND_RGBA_ADD)
                light.update()
        target_surface.blit(mask_surf_rendered, (0, 0), special_flags=self.blit_flags)
