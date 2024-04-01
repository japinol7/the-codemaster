"""Module stats."""
__author__ = 'Joan A. Pinol  (japinol)'


class Stats:

    def __init__(self):
        # Base stats
        self.name = 'stats'
        self.health = None
        self.health_total = None
        self.power = None
        self.power_total = None
        self.power_recovery = None
        self.strength = None
        self.strength_total = None
        self.magic_resistance = 0
        self.speed = None
        self.time_between_shots = None
        self.energy_shield = None
        self.energy_shields_stock = []


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
