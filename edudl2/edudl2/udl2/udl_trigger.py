__author__ = 'sravi'

import time
import logging
from edcore.watch.watcher import Watcher
from edudl2.udl2.W_schedule_pipeline import schedule_pipeline
from edudl2.udl2.celery import udl2_flat_conf as udl2_conf


logger = logging.getLogger(__name__)


# TODO: move this generic method to core and make edsftp also use the same
def get_config_from_ini(config, config_prefix):
    """Filters and returns the configs starting with the prefix specified.
    The key's in the returned config will exclude the prefix

    :param config: ini config
    :param config_prefix: prefix string to look for in the config key

    :returns dict: dictionary of configs starting with the prefix specified
    """
    options = {}
    config_prefix_len = len(config_prefix)
    for key, val in config.items():
        if key.startswith(config_prefix):
            options[key[config_prefix_len:]] = val
    return options


def udl_trigger(config):
    """Runs the watcher script on the udl arrivals zone to schedule pipeline
    when a file is ready

    :param config: Entire udl2_conf as flat dictionary
    """
    # get the settings needed for the udl trigger alone
    config = get_config_from_ini(config, config_prefix='udl2_trigger.')
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
    udl_trigger(config=udl2_conf)
