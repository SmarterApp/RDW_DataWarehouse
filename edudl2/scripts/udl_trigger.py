__author__ = 'sravi'

import time
import logging
from edcore.watch.watcher import Watcher

logger = logging.getLogger(__name__)


def get_conf(config):
    """massages the conf to make it usable for the Watcher core module

    :param config: udl trigger config
    """
    return {
        'base_dir': '/opt/edware/zones/landing',
        'source_dir': 'arrivals',
        'file_patterns_to_watch': ['*.gpg', '*.gpg.done'],
        'file_stat_watch_internal_in_seconds': 1,
        'file_stat_watch_period_in_seconds': 5,
        'file_system_scan_delay_in_seconds': 2}


def udl_trigger(config):
    file_watcher = Watcher()
    file_watcher.set_conf(config)
    while True:
        print('Searching for new files')
        udl_ready_files = file_watcher.find_udl_ready_files()
        print('UDL ready files: {files} '.format(files=udl_ready_files))
        time.sleep(float(Watcher.conf['file_system_scan_delay_in_seconds']))

if __name__ == "__main__":

    # TODO: parse ini and get the configs needed to run the udl trigger script
    udl_trigger(config=get_conf(None))
