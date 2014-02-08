#!/usr/bin/env python
from __future__ import absolute_import
import subprocess
import argparse
import os


def start_celery(config=None):
    '''
    Given the path to a configuration file, this function takes the config file name, config, and
    start a celery worker process. If there is non default config file passed down from command line,
    it will use environment variable UDL2_CONF to pass it into celery system.

    @param config: The full path and file name. the config file has to contain udl2_conf objects. please see the example
    at https://github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0/blob/master/conf/udl2_conf.py
    @type config: str
    '''

    # we start celery by showing debug messages, and send event notifications
    try:
        if config is None:
            subprocess.call(["celery worker --app=edudl2.udl2 -l debug"], shell=True)
        else:
            local_env = dict(os.environ)
            local_env['UDL2_CONF'] = config
            subprocess.call(["celery worker --app=edudl2.udl2  -l debug"], shell=True, env=local_env)
    except Exception as e:
        print(e)


def _parse_arg():
    '''
    Parse argument list from command line.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", dest="config_file")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # if argument existing. it is for configuration files
    args = _parse_arg()

    if args.config_file is None:
        config_path_file = None
    else:
        config_path_file = args.config_file

    start_celery(config_path_file)
