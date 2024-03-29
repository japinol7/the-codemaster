﻿"""Module experience points."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.models.actors.actor_types import ActorType


class ExperiencePoints:
    xp_points = {
        'level': 800,
        ActorType.BATTERY_A.name: 25,
        ActorType.FILES_DISK_A.name: 170,  # critic file
        ActorType.FILES_DISK_B.name: 80,   # great clue file
        ActorType.FILES_DISK_C.name: 25,   # average file
        ActorType.FILES_DISK_D.name: 5,
        ActorType.SKULL_GREEN.name: 1,
        ActorType.SKULL_BLUE.name: 5,
        ActorType.SKULL_YELLOW.name: 15,
        ActorType.SKULL_RED.name: 40,
        ActorType.GHOST_GREEN.name: 40,
        ActorType.GHOST_BLUE.name: 45,
        ActorType.GHOST_YELLOW.name: 60,
        ActorType.GHOST_RED.name: 70,
        ActorType.BAT_BLUE.name: 60,
        ActorType.BAT_LILAC.name: 65,
        ActorType.BAT_RED.name: 75,
        ActorType.BAT_BLACK.name: 80,
        ActorType.WOLFMAN_MALE.name: 120,
        ActorType.VAMPIRE_MALE.name: 140,
        ActorType.VAMPIRE_FEMALE.name: 160,
        ActorType.DEMON_MALE.name: 350,
        ActorType.MINE_CYAN.name: 0,
        ActorType.MINE_LILAC.name: 0,
        ActorType.SNAKE_GREEN.name: 130,
        ActorType.SNAKE_BLUE.name: 165,
        ActorType.SNAKE_YELLOW.name: 230,
        ActorType.SNAKE_RED.name: 400,
        ActorType.TERMINATOR_EYE_GREEN.name: 130,
        ActorType.TERMINATOR_EYE_BLUE.name: 175,
        ActorType.TERMINATOR_EYE_YELLOW.name: 260,
        ActorType.TERMINATOR_EYE_RED.name: 410,
        ActorType.ENERGY_SHIELD_A.name: 0,
    }
