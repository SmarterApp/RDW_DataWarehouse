__author__ = 'sravi'

import time
import logging
from edcore.watch.watcher import Watcher
from edudl2.udl2.W_schedule_pipeline import schedule_pipeline
from edudl2.udl2.celery import udl2_flat_conf as udl2_conf


logger = logging.getLogger(__name__)


#TODO: move this generic method to core and make edsftp also use the same
def get_config_from_ini(config, config_prefix):
    """Filters and returns the configs starting with the prefix specified.
    The key's in the returned config will exclude the prefix"""
    options = {}
    config_prefix_len = len(config_prefix)
    for key, val in config.items():
        if key.startswith(config_prefix):
            options[key[config_prefix_len:]] = val
    return options


def get_udl_trigger_conf(config):
    """massages the conf to make it usable for the Watcher core module

    :param config: udl trigger config
    """
    udl_trigger_conf = get_config_from_ini(config, config_prefix='udl2_trigger.')
    return {
        'base_dir': udl_trigger_conf['base_dir'],
        'source_dir': udl_trigger_conf['source_dir'],
        'file_patterns_to_watch': udl_trigger_conf['file_patterns_to_watch'],
        'file_stat_watch_internal_in_seconds': udl_trigger_conf['file_stat_watch_internal_in_seconds'],
        'file_stat_watch_period_in_seconds': udl_trigger_conf['file_stat_watch_period_in_seconds'],
        'file_system_scan_delay_in_seconds': udl_trigger_conf['file_system_scan_delay_in_seconds']}


def udl_trigger(config):
    file_watcher = Watcher()
    file_watcher.set_conf(config)
    while True:
        print('Searching for new files')
        udl_ready_files = file_watcher.find_udl_ready_files()
        print('UDL ready files: {files} '.format(files=udl_ready_files))
        for file in udl_ready_files:
            schedule_pipeline.delay(file)
        time.sleep(float(Watcher.conf['file_system_scan_delay_in_seconds']))

if __name__ == "__main__":
    """Dev testing entry point"""
    udl_trigger(config=get_udl_trigger_conf(udl2_conf))
