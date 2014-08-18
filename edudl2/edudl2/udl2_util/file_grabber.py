'''
Created on Aug 18, 2014

@author: tosako
'''
import argparse
import logging
import logging.config
from edcore.utils.utils import read_ini, get_config_from_ini, run_cron_job,\
    create_daemon
from edudl2.udl2_util.rsync import rsync
import time


def main():
    parser = argparse.ArgumentParser(description='Process udl trigger args')
    parser.add_argument('-p', dest='pidfile', default='/opt/edware/run/edudl2-trigger.pid',
                        help="pid file for edudl2 trigger daemon")
    parser.add_argument('-d', dest='daemon', action='store_true', default=False,
                        help="daemon mode for udl trigger")
    parser.add_argument('-i', dest='ini_file', default='/opt/edware/conf/smarter.ini',
                        help="smarter ini file for logging configs")

    args = parser.parse_args()
    file = args.ini_file
    logging.config.fileConfig(file)
    ini_file = read_ini(file)
    d = get_config_from_ini(ini_file, '')
    daemon_mode = args.daemon
    pid_file = args.pidfile
    if daemon_mode:
        create_daemon(pid_file)
    # setup cron
    run_cron_job(d, 'udl2_rsync.', rsync)

if __name__ == "__main__":
    main()
