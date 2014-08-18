__author__ = 'sravi'

import os
import time
import logging
import logging.config
import argparse
from edcore.watch.watcher import FileWatcher
from edudl2.udl2.W_schedule_pipeline import schedule_pipeline
from edcore.utils.utils import get_config_from_ini, run_cron_job, read_ini
from edcore.watch.constants import WatcherConstants as Const
from edudl2.udl2.celery import udl2_flat_conf as udl2_conf
from edcore.utils.utils import create_daemon
from edudl2.udl2_util.rsync import rsync


logger = logging.getLogger('edudl2')


def _find_udl_ready_files(file_watcher):
    file_watcher.find_all_files()
    file_watcher.filter_files_for_digest_mismatch()
    file_watcher.filter_checksum_files()
    return file_watcher.get_file_stats().keys()


def udl_trigger(config, loop_once=False):
    """Runs the watcher script on the udl arrivals zone to schedule pipeline
    when a file is ready

    :param config: Entire udl2_conf as flat dictionary
    :pram loop_once: Runs the loop only once if set to True (Needed for testing)
    """
    # get the settings needed for the udl trigger alone
    config = get_config_from_ini(config=config, config_prefix='udl2_trigger.')
    file_watcher = FileWatcher(config, append_logs_to='edudl2')
    logger.info('Starting UDL2 trigger loop. Looking at directory => {source_dir}'.format(
                source_dir=config.get(Const.SOURCE_DIR)))
    while True:
        try:
            logger.debug('Searching for new files in {source_dir}'.format(source_dir=config.get(Const.SOURCE_DIR)))
            udl_ready_files = _find_udl_ready_files(file_watcher)
            logger.debug('Found {count} files ready to process'.format(count=str(len(udl_ready_files))))
            for file in udl_ready_files:
                logger.debug('Scheduling pipeline for file - {file}'.format(file=file))
                schedule_pipeline.delay(file)
            if loop_once:
                break
        except KeyboardInterrupt:
            logger.warn('UDL2 trigger process terminated by a user')
            os._exit(0)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(float(file_watcher.conf.get(Const.FILE_SYSTEM_SCAN_DELAY)))
    logger.warn('Exiting udl trigger process')


def run_udl2_trigger_process(daemon_mode, conf, pid_file):
    if daemon_mode:
        create_daemon(pid_file)
    udl_trigger(conf)


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

    daemon_mode = args.daemon
    pid_file = args.pidfile
    run_udl2_trigger_process(daemon_mode, udl2_conf, pid_file)


if __name__ == "__main__":
    main()
