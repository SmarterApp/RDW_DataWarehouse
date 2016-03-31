# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'swimberly'

import configparser
import argparse
import ast

CEL_UPPER_KEY = ['celery_defaults', 'rabbitmq']


def read_ini_file(filename, section_name='app'):
    """
    Given an ini filename returns a nested amd flat dictionary that represents the ini file
    :param filename: A string that points to the python file
    :return: A nested dictionary representing the configuration
    :return: A dictionary with flat config
    """
    config = configparser.ConfigParser()
    config.read(filename)

    conf_dict = {}
    flat_conf = {}

    options = config.options(section_name)
    for option in options:
        flat_conf[option] = config.get(section_name, option)
        split_keys = option.split('.')
        current_dict = conf_dict

        # for each key in the list (except the last) create an empty dict if not already created
        for i in range(len(split_keys) - 1):
        #for key in split_keys:
            key = split_keys[i]
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]

        last_key = split_keys[-1].upper() if len(split_keys) > 1 and split_keys[-2] in CEL_UPPER_KEY else split_keys[-1]
        current_dict[last_key] = _interpolate_type(config[section_name][option])

    return conf_dict, flat_conf


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
