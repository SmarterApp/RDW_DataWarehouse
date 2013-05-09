#!/usr/bin/env python
from __future__ import absolute_import
import subprocess
import argparse
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import os

def start_celery(config=None):
    # we start celery by showing debug messages, and send event notifications
    try:
        if config is None:
            subprocess.call(["celery worker --app=udl2 -l debug"], shell=True)
        else:
            local_env = dict(os.environ)
            local_env['UDL2_CONF'] = config
            subprocess.call(["celery worker --app=udl2 -l debug"], shell=True, env=local_env)
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
        config_path_file = None
    else:
        config_path_file = args.config_file

    start_celery(config_path_file)
