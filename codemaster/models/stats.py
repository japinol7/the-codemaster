"""Module stats."""
__author__ = 'Joan A. Pinol  (japinol)'


class Stats:

    def __init__(self):
        # Base stats
        self.name = 'stats'
        self.level = 1
        self.health = None
        self.health_total = None
        self.health_pot = None
        self.power = None
        self.power_total = None
        self.magic_power = None
        self.magic_power_total = None
        self.constitution = None
        self.constitution_total = None
        self.quickness = None
        self.quickness_total = None
        self.agility = None
        self.strength = None
        self.strength_total = None
        self.speed = None
        self.time_between_shots = None
        self.energy_shield = None


class NPCStats(Stats):

    def __init__(self):
        super().__init__()
        self.name = 'NPC stats'
        self.probability_min1_drop = None
        self.probability_min2_drop = None


class PCStats(Stats):

    def __init__(self):
        super().__init__()
        self.name = 'PC stats'
