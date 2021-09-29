"""Module elements."""
__author__ = 'Joan A. Pinol  (japinol)'


class Element:

    def __init__(self):
        self.name = ''
        self.strength = None


class Air(Element):

    def __init__(self):
        super().__init__()
        self.name = 'air'


class Earth(Element):

    def __init__(self):
        super().__init__()
        self.name = 'earth'


class Fire(Element):

    def __init__(self):
        super().__init__()
        self.name = 'fire'


class Water(Element):

    def __init__(self):
        super().__init__()
        self.name = 'water'


class DarkEnergy(Element):

    def __init__(self):
        super().__init__()
        self.name = 'dark energy'
