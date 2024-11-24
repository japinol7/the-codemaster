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
            self.set_random_msg()
            return

        self.set_msg_loaded_in_disk(
            self.msg_id, is_loaded_in_disk=True, game=self.game)

    def set_random_msg(self):
        available_msgs = [
            k for k, v in self.game.files_disks_data[self.disk_type].items()
            if not v['is_loaded_in_disk'] and not v['is_corrupted']
            ]
        if not available_msgs:
            self.msg_id = f"{self.disk_type}_CORRUPTED_FILE"
            self.set_msg_encrypted(self.msg_id, is_encrypted=False, game=self.game)
            self.set_msg_loaded_in_disk(
                self.msg_id, is_loaded_in_disk=True, game=self.game)
            return

        self.msg_id = random.choice(available_msgs)

        self.set_msg_loaded_in_disk(self.msg_id, is_loaded_in_disk=True, game=self.game)

    def remove_msg(self):
        self.set_msg_loaded_in_disk(self.msg_id, is_loaded_in_disk=False, game=self.game)
        self.msg_id = None

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    @staticmethod
    def load_files_disks_data(game):
        game.__class__.files_disks_data = load_data_from_file(FILES_DISKS_DATA_FILE)

    @staticmethod
    def set_msgs_loaded_in_disks_to_false(game):
        for disk_category in game.__class__.files_disks_data.values():
            for disk in disk_category.values():
                disk['is_encrypted'] = True
                disk['is_loaded_in_disk'] = False

    @staticmethod
    def get_msg(msg_id, game):
        return game.files_disks_data[msg_id[0]][msg_id]

    @staticmethod
    def get_available_msgs_by_type(game, disk_type):
        return [
            k for k, v in game.files_disks_data[disk_type].items()
            if not v['is_loaded_in_disk'] and not v['is_corrupted']
            ]

    @staticmethod
    def read_msg(msg_id, game):
        is_encrypted = game.files_disks_data[msg_id[0]][msg_id]['is_encrypted']
        return game.files_disks_data[msg_id[0]][msg_id][
            'msg_encrypted' if is_encrypted else 'msg']

    @staticmethod
    def is_msg_encrypted(msg_id, game):
        return game.files_disks_data[msg_id[0]][msg_id]['is_encrypted']

    @staticmethod
    def set_msg_encrypted(msg_id, is_encrypted, game):
        game.files_disks_data[msg_id[0]][msg_id]['is_encrypted'] = is_encrypted

    @staticmethod
    def set_msg_loaded_in_disk(msg_id, is_loaded_in_disk, game):
        game.files_disks_data[msg_id[0]][msg_id]['is_loaded_in_disk'] = is_loaded_in_disk

    @staticmethod
    def get_msg_ids_used_in_all_levels(game):
        return {disk.msg_id for level in game.levels for disk in level.files_disks}

    @staticmethod
    def find_disk_for_msg_id(msg_id, game):
        return [disk for level in game.levels for disk in level.files_disks
                if disk.msg_id == msg_id][0]

    @staticmethod
    def remove_all_disks_msgs(game):
        for level in game.levels:
            for disk in level.files_disks:
                FilesDisk.set_msg_loaded_in_disk(disk.msg_id, is_loaded_in_disk=False, game=game)
                disk.msg_id = None

    @staticmethod
    def get_files_disks_without_msg(game):
        return [disk for level in game.levels for disk in level.files_disks
                if not disk.msg_id]

    @staticmethod
    def set_random_msg_to_disks_without_msg(game):
        for disk in FilesDisk.get_files_disks_without_msg(game):
            disk.set_random_msg()

    @staticmethod
    def get_files_disks_with_corrupted_msg(game):
        return [disk for level in game.levels for disk in level.files_disks
                if FilesDisk.get_msg(disk.msg_id, game)['is_corrupted']]

    @staticmethod
    def set_random_msg_to_disks_with_corrupted_msg(game):
        for disk in FilesDisk.get_files_disks_with_corrupted_msg(game):
            disk.set_random_msg()


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
