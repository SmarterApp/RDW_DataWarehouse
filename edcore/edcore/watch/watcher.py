__author__ = 'sravi'

import os
import fnmatch
import time
import ast
import logging
from edcore.watch.util import set_interval, FileUtil
from edcore.watch.file_hasher import MD5Hasher
from edcore.watch.constants import WatcherConstants as Const

logger = logging.getLogger(__name__)

WATCH_INTERVAL = 2


class FileWatcher():
    """File sync class to watch for complete files"""
    conf = None
    file_stats = {}
    hasher = MD5Hasher()

    def __init__(self, config):
        FileWatcher.conf = config
        FileWatcher.clear_file_stats()
        global WATCH_INTERVAL
        WATCH_INTERVAL = FileWatcher.conf[Const.FILE_STAT_WATCH_INTERVAL]
        FileWatcher.source_path = os.path.join(FileWatcher.conf[Const.BASE_DIR], FileWatcher.conf[Const.SOURCE_DIR])

    @classmethod
    def valid_check_sum(cls, file):
        checksum_file = FileUtil.get_complement_file_name(file)
        if not os.path.exists(file) or not os.path.exists(checksum_file):
            return False
        file_hash = cls.hasher.get_file_hash(file)
        return FileUtil.file_contains_hash(checksum_file, file_hash)

    @classmethod
    def clear_file_stats(cls):
        cls.file_stats.clear()

    @classmethod
    def get_file_stats(cls):
        return cls.file_stats

    @classmethod
    def find_all_files(cls):
        assert cls.conf is not None

        cls.clear_file_stats()
        for root, dirs, files in os.walk(cls.source_path):
            filtered_files = [filename for pattern in set(ast.literal_eval(cls.conf[Const.FILE_PATTERNS_TO_WATCH]))
                              for filename in fnmatch.filter(files, pattern)]
            # filter hidden file
            filtered_files = [filename for filename in filtered_files if not filename.startswith('.')]
            for filename in filtered_files:
                file_path = os.path.join(root, filename)
                file_stat = FileUtil.get_file_stat(file_path)
                if file_stat is not None:
                    cls.file_stats[file_path] = file_stat

    @classmethod
    def get_updated_file_stats(cls):
        return {filename: FileUtil.get_file_stat(filename) for filename in cls.file_stats.keys()}

    @classmethod
    @set_interval(interval=WATCH_INTERVAL)
    def watch_and_filter_files_by_stats_changes(cls):
        file_stats_latest = cls.get_updated_file_stats()
        for file, size in cls.file_stats.copy().items():
            if file_stats_latest[file] is None or file_stats_latest[file] != size:
                logger.debug('Removing file {file} due to size changes during monitoring'.format(file=file))
                cls.remove_file_pair_from_dict(file)

    @classmethod
    def watch_files(cls):
        """Watches the files for the defined duration and discards file undergoing change"""
        # monitor the files for change in stats
        stop = cls.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(float(cls.conf[Const.FILE_STAT_WATCH_PERIOD]))
        # stop the timer
        stop.set()

    @classmethod
    def remove_file_from_dict(cls, file):
        cls.file_stats.pop(file, None)

    @classmethod
    def remove_file_pair_from_dict(cls, file):
        # check the file being removed and remove the corresponding pair file
        cls.remove_file_from_dict(FileUtil.get_complement_file_name(file))
        # remove the main file
        cls.remove_file_from_dict(file)

    @classmethod
    def filter_files_for_digest_mismatch(cls):
        """Verifies checksum for all the files (ignoring '*.done' files) currently being watched"""
        all_files = cls.file_stats.copy().keys()
        # filter out the checksum files which will contain the checksum for a corresponding source file
        source_files = set(all_files) - set(fnmatch.filter(all_files, '*' + Const.CHECKSUM_FILE_EXTENSION))
        for file in source_files:
            if not cls.valid_check_sum(file):
                logger.error('Removing file {file} due to invalid hash'.format(file=file))
                cls.remove_file_pair_from_dict(file)

    @classmethod
    def filter_checksum_files(cls):
        """Remove checksum files"""
        for file in set(fnmatch.filter(cls.file_stats.copy().keys(), '*' + Const.CHECKSUM_FILE_EXTENSION)):
            cls.remove_file_from_dict(file)
