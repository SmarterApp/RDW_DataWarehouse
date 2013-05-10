#!/usr/bin/env python
from __future__ import absolute_import
import subprocess
import argparse
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp

def start_rabbitmq(RABBITMQ_SERVER):
    try:    
        subprocess.call(["sudo " +  RABBITMQ_SERVER + " &"], shell=True)
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
        
    udl2_conf = imp.load_source('udl2_conf', config_path_file)
    from udl2_conf import udl2_conf
    start_rabbitmq(udl2_conf['rabbitmq']['RABBITMQ_SERVER_PATH'])
