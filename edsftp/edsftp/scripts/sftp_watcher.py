__author__ = 'sravi'

import time
import os
import logging
from edcore.watch.watcher import FileWatcher
from edcore.watch.mover import FileMover
from edcore.watch.constants import WatcherConstants as WatcherConst, MoverConstants as MoverConst
from edsftp.src.constants import Constants as SFTPConst

logger = logging.getLogger("edsftp")


def get_watcher_conf(config):
    """massages the conf to make it usable for the FileWatcher core module

    :param config: sftp config
    """
    sftp_conf = config
    sftp_conf.update({WatcherConst.SOURCE_DIR: config[SFTPConst.ARRIVALS_DIR]})
    return sftp_conf


def get_mover_conf(config):
    """massages the conf to make it usable for the FileMover core module

    :param config: sftp config
    """
    remote_conf = {}
    prefix = 'remote.'
    remote_conf.update({MoverConst.LANDING_ZONE_HOSTNAME: config[prefix + MoverConst.LANDING_ZONE_HOSTNAME],
                        MoverConst.SFTP_USER: config[prefix + MoverConst.SFTP_USER],
                        MoverConst.PRIVATE_KEY_FILE: config[prefix + MoverConst.PRIVATE_KEY_FILE],
                        MoverConst.ARRIVALS_PATH: config[prefix + MoverConst.ARRIVALS_PATH],
                        WatcherConst.BASE_DIR: config[WatcherConst.BASE_DIR],
                        WatcherConst.SOURCE_DIR: config[SFTPConst.ARRIVALS_DIR]})
    return remote_conf


def _watch_and_move_files(file_watcher, file_mover):
    """watch and move files from the sftp arrivals zone to arrivals sync zone"""
    files_moved = 0
    file_watcher.find_all_files()
    file_watcher.watch_files()
    files_to_move = list(file_watcher.get_file_stats().keys())
    logger.debug('files to move {files_to_move}'.format(files_to_move=files_to_move))
    if len(files_to_move) > 0:
        files_moved = file_mover.move_files(files_to_move)
    return files_moved


def sftp_file_sync(config):
    """sftp file sync main entry point

    This is a forever script

    :param config: sftp config needed for file sync
    """
    remote_conf = get_mover_conf(config)
    file_watcher = FileWatcher(get_watcher_conf(config))
    file_mover = FileMover(remote_conf)
    logger.info('Starting SFTP file sync loop {source_dir} => {dest_host}:{dest_dir}'.format(
        source_dir=config[SFTPConst.ARRIVALS_DIR], dest_host=remote_conf[MoverConst.LANDING_ZONE_HOSTNAME],
        dest_dir=remote_conf[MoverConst.ARRIVALS_PATH]))
    while True:
        try:
            logger.debug('Searching for new files in {source_dir}'.format(source_dir=config[SFTPConst.ARRIVALS_DIR]))
            files_moved = _watch_and_move_files(file_watcher, file_mover)
            logger.debug('Moved {count} files to {destination}'.format(count=str(files_moved),
                                                                       destination=remote_conf[MoverConst.LANDING_ZONE_HOSTNAME]))
        except KeyboardInterrupt:
            logger.warn('SFTP watcher process terminated by a user')
            os._exit(0)
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(float(FileWatcher.conf[WatcherConst.FILE_SYSTEM_SCAN_DELAY]))
    logger.warn('Exiting sftp watcher process')
