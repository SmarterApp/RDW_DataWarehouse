__author__ = 'sravi'

import os
import fnmatch
import time
import shutil
import logging
from edsftp.scripts.util import set_interval, Singleton

console = logging.StreamHandler()
logger = logging.getLogger(__name__)

# TODO: move these to ini
SOURCE_DIR = '/opt/sftp/landing/arrivals'
DEST_DIR = '/opt/sftp/landing/arrivals_final'
PATTERN = '*.gpg'
FILE_STAT_WATCH_INTERVAL_IN_SECONDS = 2
FILE_STAT_WATCH_PERIOD_IN_SECONDS = 10
FILE_SYSTEM_SCAN_DELAY_IN_SECONDS = 5


class FileSync(metaclass=Singleton):

    source_dir = None
    dest_dir = None
    pattern = None

    def __init__(self):
        self._file_stats = {}

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size

    def clear_file_stats(self):
        self._file_stats.clear()

    def get_file_stats(self):
        return self._file_stats

    def find_all_files(self):
        for root, dirs, files in os.walk(FileSync.source_dir):
            for filename in fnmatch.filter(files, FileSync.pattern):
                file_path = os.path.join(root, filename)
                self._file_stats[file_path] = FileSync.get_file_stat(file_path)

    def get_updated_file_stats(self):
        return {filename: FileSync.get_file_stat(filename) for filename in self._file_stats.keys()}

    @set_interval(interval=FILE_STAT_WATCH_INTERVAL_IN_SECONDS)
    def watch_and_filter_files_by_stats_changes(self):
        file_stats_latest = self.get_updated_file_stats()
        for file, size in self._file_stats.copy().items():
            if file_stats_latest[file] != size:
                logger.info('Removing file {file} due to size changes during monitoring'.format(file=file))
                del self._file_stats[file]

    def watch_files(self):
        # monitor the files for change in stats
        stop = self.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(FILE_STAT_WATCH_PERIOD_IN_SECONDS)
        # stop the timer
        stop.set()

    def move_files(self):
        files_to_move = self._file_stats.keys()
        for file in files_to_move:
            destination_file_path = os.path.join(FileSync.dest_dir, os.path.relpath(file, FileSync.source_dir))
            destination_file_directory = os.path.split(destination_file_path)[0]
            if not os.path.exists(destination_file_directory):
                os.makedirs(destination_file_directory)
            logger.info('Moving file {source} to {dest}'.format(source=file, dest=destination_file_path))
            shutil.move(file, destination_file_path)
        return len(files_to_move)

    @staticmethod
    def assert_inputs():
        assert FileSync.pattern is not None
        assert FileSync.source_dir is not None
        assert FileSync.dest_dir is not None

    def find_and_move_files(self):
        FileSync.assert_inputs()
        self.clear_file_stats()
        self.find_all_files()
        self.watch_files()
        files_moved = self.move_files()
        return files_moved


def sftp_file_sync():
    finder = FileSync()
    FileSync.source_dir = SOURCE_DIR
    FileSync.dest_dir = DEST_DIR
    FileSync.pattern = PATTERN
    while True:
        logger.info('Searching for new files')
        files_moved = finder.find_and_move_files()
        logger.info('Files Moved: {count} '.format(count=str(files_moved)))
        time.sleep(FILE_SYSTEM_SCAN_DELAY_IN_SECONDS)

if __name__ == "__main__":
    sftp_file_sync()
