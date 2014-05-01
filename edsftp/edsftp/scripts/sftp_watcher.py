__author__ = 'sravi'

import time
import logging
from edcore.watch.watcher import Watcher

logger = logging.getLogger(__name__)


def get_conf(config):
    """massages the conf to make it usable for the Watcher core module

    :param config: sftp config
    """
    return {
        'base_dir': config['sftp_base_dir'],
        'source_dir': config['sftp_arrivals_dir'],
        'dest_dir': config['sftp_arrivals_sync_dir'],
        'file_patterns_to_watch': config['file_patterns_to_watch'],
        'file_stat_watch_internal_in_seconds': config['file_stat_watch_internal_in_seconds'],
        'file_stat_watch_period_in_seconds': config['file_stat_watch_period_in_seconds'],
        'file_system_scan_delay_in_seconds': config['file_system_scan_delay_in_seconds']}


def sftp_file_sync(config):
    """sftp file sync main entry point

    This is a forever script

    :param config: sftp config needed for file sync
    """
    file_watcher = Watcher()
    file_watcher.set_conf(get_conf(config))
    while True:
        print('Searching for new files')
        files_moved = file_watcher.watch_and_move_files()
        print('Files Moved: {count} '.format(count=str(files_moved)))
        time.sleep(float(Watcher.conf['file_system_scan_delay_in_seconds']))
