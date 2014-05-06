__author__ = 'sravi'

import time
import logging
from edcore.watch.watcher import FileWatcher
from edudl2.udl2.W_schedule_pipeline import schedule_pipeline
from edcore.utils.utils import get_config_from_ini
from edcore.watch.constants import WatcherConstants as Const


logger = logging.getLogger(__name__)


def _find_udl_ready_files(file_watcher):
    file_watcher.find_all_files()
    file_watcher.watch_files()
    file_watcher.filter_files_for_digest_mismatch()
    file_watcher.filter_checksum_files()
    return file_watcher.get_file_stats()


def udl_trigger(config):
    """Runs the watcher script on the udl arrivals zone to schedule pipeline
    when a file is ready

    :param config: Entire udl2_conf as flat dictionary
    """
    # get the settings needed for the udl trigger alone
    config = get_config_from_ini(config=config, config_prefix='udl2_trigger.')
    file_watcher = FileWatcher(config)
    while True:
        print('Searching for new files')
        udl_ready_files = _find_udl_ready_files(file_watcher)
        print('UDL ready files: {files} '.format(files=udl_ready_files))
        for file in udl_ready_files:
            schedule_pipeline.delay(file)
        time.sleep(float(FileWatcher.conf[Const.FILE_SYSTEM_SCAN_DELAY]))
