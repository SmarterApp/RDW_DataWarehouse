'''
Created on Aug 18, 2014

@author: tosako
'''
import argparse
import logging
import logging.config
from edcore.utils.utils import read_ini, get_config_from_ini, run_cron_job, \
    create_daemon
from edudl2.udl2_util.rsync import rsync
import time
import copy


FILE_GRABBER = 'file-grabber'


def main():
    parser = argparse.ArgumentParser(description='Process udl trigger args')
    parser.add_argument('-p', dest='pidfile', default='/opt/edware/run/edudl2-filegrabber.pid',
                        help="pid file for edudl2 trigger daemon")
    parser.add_argument('-d', dest='daemon', action='store_true', default=False,
                        help="daemon mode for udl trigger")
    parser.add_argument('-i', dest='ini_file', default='/opt/edware/conf/smarter.ini',
                        help="smarter ini file for logging configs")

    args = parser.parse_args()
    file = args.ini_file
    logging.config.fileConfig(file)
    ini_file = read_ini(file)
    config = get_config_from_ini(ini_file, '')
    daemon_mode = args.daemon
    pid_file = args.pidfile
    if daemon_mode:
        create_daemon(pid_file)
    # get file-grabber and reassembly config file
    config_for_grabber = copy.deepcopy(config)
    file_grabber_configs = {}
    for key in config_for_grabber.keys():
        key_values = key.split('.')
        if key_values[0] == FILE_GRABBER:
            key_values.pop(0)
            name = key_values.pop(0)
            file_grabber_config = file_grabber_configs.get(name, {})
            file_grabber_config[FILE_GRABBER + '.' + '.'.join(key_values)] = config['.'.join([FILE_GRABBER, name]) + '.' + '.'.join(key_values)]
            file_grabber_configs[name] = file_grabber_config

    if file_grabber_configs:
        # setup cron
        for file_grabber_config in file_grabber_configs:
            run_cron_job(file_grabber_configs[file_grabber_config], FILE_GRABBER + '.', rsync)
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()
