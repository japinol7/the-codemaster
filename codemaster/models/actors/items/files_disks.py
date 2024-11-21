"""Module files disks."""
__author__ = 'Joan A. Pinol  (japinol)'

import random

from codemaster.config.constants import (
    BM_FILE_DISKS_FOLDER,
    FILES_DISKS_DATA_FILE,
    )
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats
from codemaster.persistence.persistence_utils import load_data_from_file


class FilesDisk(ActorItem):
    """Represents a files disk.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, msg_id=None):
        self.file_folder = BM_FILE_DISKS_FOLDER
        self.file_name_key = 'im_files_disks'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.FILES_DISK
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.msg_id = msg_id

        if not getattr(self, 'disk_type', None):
            self.disk_type = None

        super().__init__(x, y, game, name=name)

        if self.msg_id is None:
            self.calculate_msg()

    def calculate_msg(self):
        self.msg_id = random.choice(list(self.game.files_disks_data[self.disk_type]))

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    @staticmethod
    def load_files_disks_data(game):
        game.__class__.files_disks_data = load_data_from_file(FILES_DISKS_DATA_FILE)

    @staticmethod
    def read_msg(msg_id, game):
        is_encrypted = game.files_disks_data[msg_id[0]][msg_id][2]
        return game.files_disks_data[msg_id[0]][msg_id][1 if is_encrypted else 0]

    @staticmethod
    def is_msg_encrypted(msg_id, game):
        return game.files_disks_data[msg_id[0]][msg_id][2]

    @staticmethod
    def set_msg_encrypted(msg_id, is_encrypted, game):
        game.files_disks_data[msg_id[0]][msg_id][2] = is_encrypted


class FilesDiskD(FilesDisk):
    """Represents a files disk of type D."""

    def __init__(self, x, y, game, name=None, msg_id=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.FILES_DISK_D
        self.disk_type = 'D'
        super().__init__(x, y, game, name=name, msg_id=msg_id)


class FilesDiskC(FilesDisk):
    """Represents a files disk of type C."""

    def __init__(self, x, y, game, name=None, msg_id=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.FILES_DISK_C
        self.disk_type = 'C'
        super().__init__(x, y, game, name=name, msg_id=msg_id)


class FilesDiskB(FilesDisk):
    """Represents a files disk of type B."""

    def __init__(self, x, y, game, name=None, msg_id=None):
        self.file_mid_prefix = '03'
        self.type = ActorType.FILES_DISK_B
        self.disk_type = 'B'
        super().__init__(x, y, game, name=name, msg_id=msg_id)


class FilesDiskA(FilesDisk):
    """Represents a files disk of type A."""

    def __init__(self, x, y, game, name=None, msg_id=None):
        self.file_mid_prefix = '04'
        self.type = ActorType.FILES_DISK_A
        self.disk_type = 'A'
        super().__init__(x, y, game, name=name, msg_id=msg_id)
