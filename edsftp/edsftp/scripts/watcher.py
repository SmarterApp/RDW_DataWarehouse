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
    """File sync class to watch for complete files"""
    conf = None
    file_stats = {}

    def __init__(self):
        pass

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size if os.path.exists(filename) else None

    @classmethod
    def set_conf(cls, config):
        cls.conf = config
        cls.clear_file_stats()
        global WATCH_INTERVAL_IN_SECONDS
        WATCH_INTERVAL_IN_SECONDS = FileSync.conf['file_stat_watch_internal_in_seconds']
        FileSync.source_dir = os.path.join(FileSync.conf['sftp_base_dir'], FileSync.conf['sftp_arrivals_dir'])
        FileSync.dest_dir = os.path.join(FileSync.conf['sftp_base_dir'], FileSync.conf['sftp_arrivals_sync_dir'])

    @classmethod
    def clear_file_stats(cls):
        cls.file_stats.clear()

    @classmethod
    def get_file_stats(cls):
        return cls.file_stats

    @classmethod
    def find_all_files(cls):
        for root, dirs, files in os.walk(cls.source_dir):
            for filename in fnmatch.filter(files, cls.conf['file_pattern_to_watch']):
                file_path = os.path.join(root, filename)
                file_stat = cls.get_file_stat(file_path)
                if file_stat is not None:
                    cls.file_stats[file_path] = file_stat

    @classmethod
    def get_updated_file_stats(cls):
        return {filename: cls.get_file_stat(filename) for filename in cls.get_file_stats().keys()}

    @classmethod
    @set_interval(interval=WATCH_INTERVAL_IN_SECONDS)
    def watch_and_filter_files_by_stats_changes(cls):
        file_stats_latest = cls.get_updated_file_stats()
        for file, size in cls.get_file_stats().copy().items():
            if file_stats_latest[file] is None or file_stats_latest[file] != size:
                print('Removing file {file} due to size changes during monitoring'.format(file=file))
                del cls.file_stats[file]

    @classmethod
    def watch_files(cls):
        # monitor the files for change in stats
        stop = cls.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(float(cls.conf['file_stat_watch_period_in_seconds']))
        # stop the timer
        stop.set()

    @classmethod
    def move_files(cls):
        files_to_move = cls.get_file_stats().keys()
        for file in files_to_move:
            destination_file_path = os.path.join(cls.dest_dir, os.path.relpath(file, cls.source_dir))
            destination_file_directory = os.path.split(destination_file_path)[0]
            if not os.path.exists(destination_file_directory):
                os.makedirs(destination_file_directory)
            print('Moving file {source} to {dest}'.format(source=file, dest=destination_file_path))
            shutil.move(file, destination_file_path)
        return len(files_to_move)

    @classmethod
    def assert_inputs(cls):
        assert cls.conf is not None

    @classmethod
    def find_and_move_files(cls):
        cls.clear_file_stats()
        cls.assert_inputs()
        cls.find_all_files()
        cls.watch_files()
        return cls.move_files()


def sftp_file_sync(sftp_conf):
    file_sync = FileSync()
    file_sync.set_conf(sftp_conf)
    while True:
        print('Searching for new files')
        files_moved = file_sync.find_and_move_files()
        print('Files Moved: {count} '.format(count=str(files_moved)))
        time.sleep(float(FileSync.conf['file_system_scan_delay_in_seconds']))

if __name__ == "__main__":

    conf = {
        'sftp_base_dir': '/sftp/opt/edware/home',
        'sftp_arrivals_dir': 'arrivals',
        'sftp_arrivals_sync_dir': 'arrivals_sync',
        'file_pattern_to_watch': '*.gpg',
        'file_stat_watch_internal_in_seconds': 1,
        'file_stat_watch_period_in_seconds': 5,
        'file_system_scan_delay_in_seconds': 2
    }
    sftp_file_sync(conf)
