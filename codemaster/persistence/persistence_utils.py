"""Module persistence_utils."""
__author__ = 'Joan A. Pinol  (japinol)'

import json

from codemaster.config.constants import JSON_INDENT_SIZE


def load_data_from_file(file_name):
    try:
        with open(file_name, 'r', encoding='UTF-8') as file_in:
            data_json = json.load(file_in)
    except Exception as e:
        return {}

    return data_json


def save_data_to_file(file_name, data):
    data_json = json.dumps(data, indent=JSON_INDENT_SIZE)
    with open(file_name, 'w', encoding='UTF-8') as file_out:
        file_out.write(data_json)
