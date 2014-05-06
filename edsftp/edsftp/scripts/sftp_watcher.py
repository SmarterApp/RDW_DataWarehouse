__author__ = 'sravi'

import time
import os
import logging
from edcore.watch.watcher import FileWatcher
from edcore.watch.constants import WatcherConstants as WatcherConst
from edsftp.src.constants import Constants as SFTPConst

logger = logging.getLogger("edsftp")


def get_conf(config):
    """massages the conf to make it usable for the FileWatcher core module

    :param config: sftp config
    """
    sftp_conf = config
    sftp_conf.update({WatcherConst.SOURCE_DIR: config[SFTPConst.ARRIVALS_DIR], WatcherConst.DEST_DIR: config[SFTPConst.ARRIVALS_SYNC_DIR]})
    return sftp_conf


def _watch_and_move_files(file_watcher):
    """watch and move files from the sftp arrivals zone to arrivals sync zone"""
    file_watcher.find_all_files()
    file_watcher.watch_files()
    files_moved = file_watcher.move_files()
    return files_moved


def sftp_file_sync(config):
    """sftp file sync main entry point

    This is a forever script

    :param config: sftp config needed for file sync
    """
    file_watcher = FileWatcher(get_conf(config))
    while True:
        try:
            logger.debug('Searching for new files in {source_dir}'.format(source_dir=config[SFTPConst.ARRIVALS_DIR]))
            files_moved = _watch_and_move_files(file_watcher)
            logger.debug('Moved {count} files to {dest_dir}'.format(count=str(files_moved),
                                                                    dest_dir=config[SFTPConst.ARRIVALS_SYNC_DIR]))
        except KeyboardInterrupt:
            logger.warn('SFTP watcher process terminated by a user')
            os._exit(0)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(float(FileWatcher.conf[WatcherConst.FILE_SYSTEM_SCAN_DELAY]))
    logger.warn('Exiting sftp watcher process')
