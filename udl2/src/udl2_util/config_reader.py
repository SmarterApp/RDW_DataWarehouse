__author__ = 'swimberly'

import configparser
import argparse
import ast
from celery.utils import strtobool
import pprint

CEL_UPPER_KEY = ['celery_defaults', 'rabbitmq']


def read_ini_file(filename, section_name='app'):
    """
    Given an ini filename create dictionary the represents the ini file
    :param filename: A string that points to the python file
    :return: A dictionary representing the configuration
    """

    config = configparser.ConfigParser()
    config.read(filename)

    conf_dict = {}

    # loop over items
    for item in config[section_name]:
        split_keys = item.split('.')
        current_dict = conf_dict

        # for each key in the list (except the last) create an empty dict if not already created
        for i in range(len(split_keys) - 1):
        #for key in split_keys:
            key = split_keys[i]
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]

        last_key = split_keys[-1].upper() if len(split_keys) > 1 and split_keys[-2] in CEL_UPPER_KEY else split_keys[-1]
        current_dict[last_key] = _interpolate_type(config[section_name][item])

    return conf_dict


def _interpolate_type(value_str):
    """
    Given a string convert it to its actual type
    :param value_str:
    :return:
    """

    # try to evaluate the string to its proper type
    try:
        return ast.literal_eval(value_str)
    except (ValueError, SyntaxError):  # string not cannot be evaluated
        return value_str


if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument('-f', '--filename', help='filename', required=True)

    args = arg_parse.parse_args()
    read_ini_file(args.filename)