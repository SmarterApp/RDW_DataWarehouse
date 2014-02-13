#!/usr/bin/env python
from __future__ import absolute_import
import subprocess
import argparse
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import os.path
from edudl2.udl2_util.config_reader import read_ini_file


def start_rabbitmq(RABBITMQ_SERVER):
    try:
        if type(RABBITMQ_SERVER).__name__ == 'str':
            subprocess.call(["sudo " + RABBITMQ_SERVER + " &"], shell=True)
        elif type(RABBITMQ_SERVER).__name__ == 'list':
            for i in RABBITMQ_SERVER:
                if os.path.isfile(i):
                    subprocess.call(["sudo " + i + " &"], shell=True)
    except Exception as e:
        print(e)


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", dest="config_file")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # if argument existing. it is for configuration files
    args = parse_arg()
    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file

    conf_tup = read_ini_file(config_path_file)
    udl2_conf = conf_tup[0]

    start_rabbitmq(udl2_conf['rabbitmq']['RABBITMQ_SERVER_PATH'])
