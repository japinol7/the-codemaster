"""Module files disks."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_FILE_DISKS_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats


class FilesDisk(ActorItem):
    """Represents a files disk.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_FILE_DISKS_FOLDER
        self.file_name_key = 'im_files_disks'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.FILES_DISK
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class FilesDiskD(FilesDisk):
    """Represents a files disk of type D."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.FILES_DISK_D
        self.disk_type = 'D'
        super().__init__(x, y, game, name=name)


class FilesDiskC(FilesDisk):
    """Represents a files disk of type C."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.FILES_DISK_C
        self.disk_type = 'C'
        super().__init__(x, y, game, name=name)


class FilesDiskB(FilesDisk):
    """Represents a files disk of type B."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '03'
        self.type = ActorType.FILES_DISK_B
        self.disk_type = 'B'
        super().__init__(x, y, game, name=name)


class FilesDiskA(FilesDisk):
    """Represents a files disk of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '04'
        self.type = ActorType.FILES_DISK_A
        self.disk_type = 'A'
        super().__init__(x, y, game, name=name)
