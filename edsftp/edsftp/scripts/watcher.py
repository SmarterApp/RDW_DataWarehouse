__author__ = 'sravi'

import os
import fnmatch
import time
import shutil
import logging
from edsftp.scripts.util import set_interval, Singleton

console = logging.StreamHandler()
logger = logging.getLogger(__name__)

WATCH_INTERVAL_IN_SECONDS = 2


class FileSync(metaclass=Singleton):

    conf = None

    def __init__(self, conf):
        self._file_stats = {}
        FileSync.set_conf(conf)

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size

    @staticmethod
    def set_conf(conf):
        FileSync.conf = conf
        global WATCH_INTERVAL_IN_SECONDS
        WATCH_INTERVAL_IN_SECONDS = FileSync.conf['file_stat_watch_internal_in_seconds']
        FileSync.source_dir = os.path.join(FileSync.conf['sftp_base_dir'], FileSync.conf['sftp_arrivals_dir'])
        FileSync.dest_dir = os.path.join(FileSync.conf['sftp_base_dir'], FileSync.conf['sftp_arrivals_rsync_dir'])

    def clear_file_stats(self):
        self._file_stats.clear()

    def get_file_stats(self):
        return self._file_stats

    def find_all_files(self):
        for root, dirs, files in os.walk(FileSync.source_dir):
            for filename in fnmatch.filter(files, FileSync.conf['file_pattern_to_watch']):
                file_path = os.path.join(root, filename)
                self._file_stats[file_path] = FileSync.get_file_stat(file_path)

    def get_updated_file_stats(self):
        return {filename: FileSync.get_file_stat(filename) for filename in self._file_stats.keys()}

    @set_interval(interval=WATCH_INTERVAL_IN_SECONDS)
    def watch_and_filter_files_by_stats_changes(self):
        file_stats_latest = self.get_updated_file_stats()
        for file, size in self._file_stats.copy().items():
            if file_stats_latest[file] != size:
                print('Removing file {file} due to size changes during monitoring'.format(file=file))
                del self._file_stats[file]

    def watch_files(self):
        # monitor the files for change in stats
        stop = self.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(float(FileSync.conf['file_stat_watch_period_in_seconds']))
        # stop the timer
        stop.set()

    def move_files(self):
        files_to_move = self._file_stats.keys()
        for file in files_to_move:
            destination_file_path = os.path.join(FileSync.dest_dir, os.path.relpath(file, FileSync.source_dir))
            destination_file_directory = os.path.split(destination_file_path)[0]
            if not os.path.exists(destination_file_directory):
                os.makedirs(destination_file_directory)
            print('Moving file {source} to {dest}'.format(source=file, dest=destination_file_path))
            shutil.move(file, destination_file_path)
        return len(files_to_move)

    @staticmethod
    def assert_inputs():
        assert FileSync.conf is not None

    def find_and_move_files(self):
        FileSync.assert_inputs()
        self.clear_file_stats()
        self.find_all_files()
        self.watch_files()
        files_moved = self.move_files()
        return files_moved


def sftp_file_sync(sftp_conf):
    finder = FileSync(sftp_conf)
    while True:
        print('Searching for new files')
        files_moved = finder.find_and_move_files()
        print('Files Moved: {count} '.format(count=str(files_moved)))
        time.sleep(float(FileSync.conf['file_system_scan_delay_in_seconds']))

if __name__ == "__main__":

    conf = {
        'sftp_base_dir': '/sftp/opt/edware/home',
        'sftp_arrivals_dir': 'arrivals',
        'sftp_arrivals_rsync_dir': 'arrivals_rsync',
        'file_pattern_to_watch': '*.gpg',
        'file_stat_watch_internal_in_seconds': 1,
        'file_stat_watch_period_in_seconds': 5,
        'file_system_scan_delay_in_seconds': 2
    }
    sftp_file_sync(conf)
