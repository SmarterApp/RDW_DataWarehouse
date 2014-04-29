__author__ = 'sravi'


import os
import fnmatch
import time
import threading
import shutil


SOURCE_DIR = '/opt/sftp/landing/arrivals'
DEST_DIR = '/opt/sftp/landing/arrivals_final'
PATTERN = '*.gpg'
FILE_STAT_WATCH_INTERVAL_IN_SECONDS = 5
FILE_STAT_WATCH_PERIOD_IN_SECONDS = 10
FILE_SYSTEM_SCAN_DELAY_IN_SECONDS = 5


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator


class FileSync:

    def __init__(self, source_dir, dest_dir, pattern):
        globals()[self.__class__.__name__] = self
        self._file_stats = {}
        self._source_dir = source_dir
        self._dest_dir = dest_dir
        self._pattern = pattern

    def __call__(self):
        return self

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size

    def clear_file_stats(self):
        self._file_stats.clear()

    def find_all_files(self):
        for root, dirs, files in os.walk(self._source_dir):
            for filename in fnmatch.filter(files, self._pattern):
                file_path = os.path.join(root, filename)
                self._file_stats[file_path] = FileSync.get_file_stat(file_path)

    def get_file_stats(self):
        return {filename: FileSync.get_file_stat(filename) for filename in self._file_stats.keys()}

    @set_interval(interval=FILE_STAT_WATCH_INTERVAL_IN_SECONDS)
    def watch_and_filter_files_by_stats_changes(self):
        file_stats_latest = self.get_file_stats()
        for file, size in self._file_stats.copy().items():
            if file_stats_latest[file] != size:
                print('Removing file due to size changes during monitoring: ', file)
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
            destination_file_path = os.path.join(self._dest_dir, os.path.relpath(file, self._source_dir))
            destination_file_directory = os.path.split(destination_file_path)[0]
            if not os.path.exists(destination_file_directory):
                os.makedirs(destination_file_directory)
            print('Moving file ', file, 'to ', destination_file_path)
            shutil.move(file, destination_file_path)
        return len(files_to_move)

    def find_and_move_files(self):
        self.clear_file_stats()
        self.find_all_files()
        self.watch_files()
        files_moved = self.move_files()
        return files_moved


def sftp_file_sync():
    finder = FileSync(SOURCE_DIR, DEST_DIR, PATTERN)
    while True:
        print('Searching for new files')
        files_moved = finder.find_and_move_files()
        print('Files Moved: ' + str(files_moved))
        time.sleep(FILE_SYSTEM_SCAN_DELAY_IN_SECONDS)

if __name__ == "__main__":
    sftp_file_sync()