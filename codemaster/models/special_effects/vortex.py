"""Module vortex."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter
from enum import Enum
import math

import pygame as pg

from codemaster.utils.colors import Color
from codemaster.utils import utils_graphics as libg_jp

COLOR_TRANSP_RATIO_DEFAULT = 0.2


class VortexDrawMethod(Enum):
    NONE = 0
    CIRCLE = 1
    POLYGON = 2


class Vortex:
    """Represents a vortex."""
    sprite_image = None
    type_id_count = Counter()
    surface_renders = {}

    def __init__(self, position, angle, speed, color=Color.WHITE,
                 color_transparency_ratio=COLOR_TRANSP_RATIO_DEFAULT, scale=1,
                 draw_method=VortexDrawMethod.CIRCLE):
        self.type = 'SPARK_' + ''.join([f'{x:03d}' for x in color])
        Vortex.type_id_count[self.type] += 1
        self.id = f"{self.type}_{Vortex.type_id_count[self.type]:05d}"
        self.position = position
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.alive = True
        self.color_transparency_ratio = color_transparency_ratio
        self.color = [x * color_transparency_ratio for x in color]

        if draw_method == VortexDrawMethod.POLYGON:
            self.draw_method = self.draw_method_polygon
        else:
            self.draw_method = self.draw_method_circle

    def calc_move(self, dt):
        return [math.cos(self.angle) * self.speed * dt,
                math.sin(self.angle) * self.speed * dt]

    def set_point_towards(self, angle, rate):
        rotate_dir = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        rotate_sign = abs(rotate_dir) / rotate_dir if rotate_dir else 1

        if abs(rotate_dir) < rate:
            self.angle = angle
            return
        self.angle += rate * rotate_sign

    def move(self, dt):
        move = self.calc_move(dt)
        self.position[0] += move[0]
        self.position[1] += move[1]

        self.angle += 0.14

        self.speed -= 0.1
        if self.speed <= 0:
            self.alive = False

    def draw_method_polygon(self, surface):
        lateral_point = [
            self.position[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
            self.position[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3]

        points = [
            [self.position[0] + math.cos(self.angle) * self.speed * self.scale,
             self.position[1] + math.sin(self.angle) * self.speed * self.scale],
            lateral_point,
            [self.position[0] + math.cos(self.angle) * self.speed * self.scale * 3.5,
             self.position[1] + math.sin(self.angle) * self.speed * self.scale * 3.5],
            lateral_point,
            ]
        pg.draw.polygon(surface, self.color, points)

    def draw_method_circle(self, surface):
        libg_jp.create_circle_in_surface_cached(
                surface, color=tuple(self.color),
                position=(self.position[0], self.position[1]),
                radius=self.speed * self.scale * 0.3,
                surface_renders=self.__class__.surface_renders)

    def draw(self, surface):
        if not self.alive:
            return
        self.draw_method(surface)
