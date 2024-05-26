"""Module utils."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple

from codemaster.tools.utils.colors import Color
from codemaster.config import constants as consts


Point = namedtuple('Point', ['x', 'y'])
Size = namedtuple('Size', ['w', 'h'])


def pretty_dict_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent, f"{str(key):22}", '-->', end='')
        if isinstance(value, dict):
            print('')
            pretty_dict_print(value, indent + 1)
        else:
            print('\t' * (indent + 1), '{:>10}'.format(str(value)))


def pretty_dict_to_string(d, indent=0, with_last_new_line=False, res='', first_time=True):
    for key, value in d.items():
        res = '%s%s%s%s' % (res, '\t' * indent, f"{str(key):28}", '-->')
        if isinstance(value, dict):
            res = '%s\n' % res
            res = '%s%s' % (res, pretty_dict_to_string(value, indent + 1, res='', first_time=False))
        else:
            res = '{}{}{:>10}\n'.format(res, '\t' * (indent + 1), str(value))
    if first_time and not with_last_new_line:
        res = res[:-1]
    return res


def write_list_to_file(file, value, open_method='a'):
    with open(file, open_method) as fout:
        for line in value:
            fout.write(line)
    value = []


def file_read_list(file_name, lines_to_read):
    res = []
    try:
        with open(file_name, "r") as file_in:
            i = 0
            for line in file_in:
                if i <= lines_to_read:
                    res.append(line.lower().replace('\n', '').replace(' ', ''))
                i += 1
    except FileNotFoundError:
        res = False
        print(f"File does not exist: {file_name}")
    except Exception:
        res = False
    return res


def map_color_to_img_num(color):
    res = 0
    if color == Color.GREEN:
        res = 1
    elif color == Color.YELLOW:
        res = 2
    elif color == Color.BLUE:
        res = 3
    elif color == Color.RED:
        res = 4
    elif color == Color.BLACK:
        res = 5
    return res


def map_color_num_to_name_txt(color):
    res = ''
    if color == 1:
        res = 'Green'
    elif color == 2:
        res = 'Yellow'
    elif color == 3:
        res = 'Blue'
    elif color == 4:
        res = 'Red'
    elif color == 5:
        res = 'Black'
    return res


def map_direction_to_string(direction):
    res = None
    if direction == consts.DIRECTION_LEFT:
        res = 'left'
    if direction == consts.DIRECTION_RIGHT:
        res = 'right'
    if direction == consts.DIRECTION_UP:
        res = 'up'
    if direction == consts.DIRECTION_DOWN:
        res = 'down'
    if direction == consts.DIRECTION_RIP:
        res = 'RIP'
    return res
