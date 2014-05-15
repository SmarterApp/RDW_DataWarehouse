__author__ = 'sravi'

import logging
from edcore.watch.util import FileCopyUtil

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
            FileCopyUtil.remote_transfer_file(source_file=file)
        return len(files_to_move)
