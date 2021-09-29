"""Module magic."""
__author__ = 'Joan A. Pinol  (japinol)'


class Magic:

    def __init__(self):
        self.name = ''
        self.strength = None


class Chaos(Magic):

    def __init__(self):
        super().__init__()
        self.name = 'chaos'


class Dark(Magic):

    def __init__(self):
        super().__init__()
        self.name = 'dark'


class Nature(Magic):

    def __init__(self):
        super().__init__()
        self.name = 'nature'


class Sorcery(Magic):

    def __init__(self):
        super().__init__()
        self.name = 'sorcery'


class White(Magic):

    def __init__(self):
        super().__init__()
        self.name = 'white'
