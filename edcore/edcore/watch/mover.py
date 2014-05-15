__author__ = 'sravi'

import os
import logging
from edcore.watch.util import SendFileUtil
from edcore.watch.util import FileUtil
from edcore.watch.constants import MoverConstants as MoverConst, WatcherConstants as WatcherConst

logger = logging.getLogger("edsftp")


class FileMover():
    """File mover class to move files to needed destination"""
    conf = None
    files_to_move = []

    def __init__(self, config):
        FileMover.conf = config

    @classmethod
    def move_files(cls, files_to_move):
        logger.debug('Remote Config: {conf}'.format(conf=cls.conf))
        for file in files_to_move:
            logger.debug('SFTPing file: ' + file)
            file_tenant_name, file_tenant_user_name = \
                FileUtil.get_file_tenant_and_user_name(file, os.path.join(cls.conf[WatcherConst.BASE_DIR],
                                                                          cls.conf[WatcherConst.SOURCE_DIR]))
            file_transfer_status = \
                SendFileUtil.remote_transfer_file(source_file=file,
                                                  hostname=cls.conf[MoverConst.LANDING_ZONE_HOSTNAME],
                                                  remote_base_dir=cls.conf[MoverConst.ARRIVALS_PATH],
                                                  file_tenantname=file_tenant_name,
                                                  file_username=file_tenant_user_name,
                                                  sftp_username=cls.conf[MoverConst.SFTP_USER],
                                                  private_key_file=cls.conf[MoverConst.PRIVATE_KEY_FILE])
            logger.debug('File transfer status {status}'.format(status=file_transfer_status))
            if file_transfer_status != 0:
                logger.error('File transfer failed for {file}'.format(file=file))
            else:
                logger.debug('File transfer was success for {file}'.format(file=file))
                os.remove(file)
                logger.debug('Deleted source file {file}'.format(file=file))

        return len(files_to_move)
