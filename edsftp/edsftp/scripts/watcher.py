__author__ = 'sravi'


import os
import fnmatch
import time
import threading
import shutil


SOURCE_DIR = '/opt/sftp/landing/arrivals'
DEST_DIR = '/opt/sftp/landing/arrivals_final'
PATTERN = '*.gpg'


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

    def __init__(self):
        globals()[self.__class__.__name__] = self
        self.file_stats = {}

    def __call__(self):
        return self

    def clear_file_stats(self):
        self.file_stats = {}

    def find_all_files(self, directory, extension):
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, extension):
                file_path = os.path.join(root, filename)
                self.file_stats[file_path] = FileSync.get_file_stat(file_path)

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size

    def get_file_stats(self):
        return {filename: FileSync.get_file_stat(filename) for filename in self.file_stats.keys()}

    @set_interval(5)
    def watch_and_filter_files_by_stats_changes(self):
        file_stats_latest = self.get_file_stats()
        for file, size in self.file_stats.copy().items():
            if file_stats_latest[file] != size:
                print('Removing file due to size changes during monitoring: ', file)
                del self.file_stats[file]

    def filter_files_by_stat(self):
        # monitor the files for change in stats
        stop = self.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(10)
        # stop the timer
        stop.set()

    @staticmethod
    def move_files(files, source_base_dir, dest_base_dir):
        for file in files:
            file_relative_path = os.path.relpath(file, source_base_dir)
            destination_file_path = os.path.join(dest_base_dir, file_relative_path)
            destination_file_directory = os.path.split(destination_file_path)[0]
            if not os.path.exists(destination_file_directory):
                os.makedirs(destination_file_directory)
            print('Moving file ', file, 'to ', destination_file_path)
            shutil.move(file, destination_file_path)
        return len(files)

    def find_and_move_files(self, source_directory, dest_directory, extension):
        self.clear_file_stats()
        self.find_all_files(source_directory, extension)
        self.filter_files_by_stat()
        files_moved = FileSync.move_files(self.file_stats.keys(), source_directory, dest_directory)
        return files_moved


def sftp_file_sync():
    finder = FileSync()
    while True:
        print('Searching for new files')
        files_moved = finder.find_and_move_files(SOURCE_DIR, DEST_DIR, PATTERN)
        print('Files Moved: ' + str(files_moved))
        time.sleep(5)

if __name__ == "__main__":
    sftp_file_sync()