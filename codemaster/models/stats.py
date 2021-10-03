"""Module stats."""
__author__ = 'Joan A. Pinol  (japinol)'


class Stats:

    def __init__(self):
        # Base stats
        self.name = 'stats'
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
        self.breath_elements = []  # List of elements
        self.time_between_shots = None
        # Defence
        self.defense_melee = None
        self.defense_missile = None
        self.defense_thrown = None
        self.defense_breathes = []  # List of elements
        self.shield_bonus = None
        # Resistance against poisons, mental control, etc
        self.resistance_poison = None
        self.resistance_mental = None
        self.resistance_elements = []  # List of elements
        self.resistance_magic = []  # List of magic sources
        # Attacks
        self.melee = None
        self.missile = None
        self.thrown = None
        self.breath = None
        # Attack modifiers
        self.poisoned = None
        self.elemental = None

    def add_breath_element(self, element):
        self.breath_elements.append(element)

    def add_defense_breaths(self, element):
        self.defense_breathes.append(element)

    def add_resistance_elements(self, element):
        self.resistance_elements.append(element)

    def add_resistance_magic(self, element):
        self.resistance_magic.append(element)


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
