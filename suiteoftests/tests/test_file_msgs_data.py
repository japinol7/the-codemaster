"""Module test_file_msgs_data."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import FILES_DISKS_DATA_FILE
from codemaster.persistence.persistence_utils import load_data_from_file
from suiteoftests.test_suite.game_test import game_test

MSG_TYPES = ['A', 'B', 'C', 'D']


@game_test(levels=[])
def test_file_msgs_basic_structure(game):
    error_msgs = []
    files_data = load_data_from_file(FILES_DISKS_DATA_FILE)

    if not isinstance(files_data, dict):
        error_msgs += ["files_data must be a dict"]

    if files_data.get('A', None) is None:
        error_msgs += ["KeyError(A)"]

    if files_data.get('B', None) is None:
        error_msgs += ["KeyError(B)"]

    if files_data.get('C', None) is None:
        error_msgs += ["KeyError(C)"]

    if files_data.get('D', None) is None:
        error_msgs += ["KeyError(D)"]

    if not error_msgs:
        for msg_type in MSG_TYPES:
            is_corrupted_file_key_present = False
            for file_msg_id in files_data[msg_type]:
                if not isinstance(file_msg_id, str):
                    error_msgs += [f"file msg id must be a str: {file_msg_id}"]
                if len(file_msg_id) < 4:
                    error_msgs += [f"file msg id must have at least "
                                   f"4 chars: {file_msg_id}"]
                elif file_msg_id[0] != msg_type or file_msg_id[1] != '_':
                    error_msgs += [f"file msg id of type '{msg_type}' "
                                   f"must start with '{msg_type}_': "
                                   f"{file_msg_id}"]
                if file_msg_id == f'{msg_type}_CORRUPTED_FILE':
                    is_corrupted_file_key_present = True
            if not is_corrupted_file_key_present:
                error_msgs += [
                    f"Missing corrupted file key: {msg_type}_CORRUPTED_FILE"
                    ]

    game.assert_test_passed(
        condition=not error_msgs,
        failed_msg=f"disk msgs file must have the required structure: "
                   f"{error_msgs}")


@game_test(levels=[])
def test_file_msgs_data_level_structure(game):
    error_msgs = []
    files_data = load_data_from_file(FILES_DISKS_DATA_FILE)

    for msg_type in MSG_TYPES:
        for file_msg in files_data[msg_type].values():
            if not isinstance(file_msg, dict):
                error_msgs += [
                    f"files_data['{file_msg}'] msg type must be a dict"
                    ]
            if file_msg.get('title', None) is None:
                error_msgs += ["KeyError(title)"]
            if file_msg.get('msg', None) is None:
                error_msgs += ["KeyError(msg)"]
            if file_msg.get('msg_encrypted', None) is None:
                error_msgs += ["KeyError(msg_encrypted)"]
            if file_msg.get('is_encrypted', None) is None:
                error_msgs += ["KeyError(is_encrypted)"]
            if file_msg.get('is_loaded_in_disk', None) is None:
                error_msgs += ["KeyError(is_loaded_in_disk)"]
            if file_msg.get('is_corrupted', None) is None:
                error_msgs += ["KeyError(is_corrupted)"]

            if not isinstance(file_msg.get('title'), str):
                error_msgs += [f"title must be a str"]
            if not isinstance(file_msg.get('msg'), str):
                error_msgs += [f"msg must be a str"]
            if not isinstance(file_msg.get('msg_encrypted'), str):
                error_msgs += [f"msg_encrypted must be a str"]
            if not isinstance(file_msg.get('is_encrypted'), bool):
                error_msgs += [f"is_encrypted must be a bool"]
            if not isinstance(file_msg.get('is_loaded_in_disk'), bool):
                error_msgs += [f"is_loaded_in_disk must be a bool"]
            if not isinstance(file_msg.get('is_corrupted'), bool):
                error_msgs += [f"is_corrupted must be a bool"]

    game.assert_test_passed(
        condition=not error_msgs,
        failed_msg=f"disk msgs file must have the required "
                   f"data level structure: {error_msgs}")
