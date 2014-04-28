__author__ = 'sravi'


import os
import fnmatch
import time
import threading


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


class FileFinder:

    def __init__(self):
        self.file_stats = {}

    def find_all_files(self, directory, extension):
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, extension):
                file_path = os.path.join(root, filename)
                self.file_stats[file_path] = FileFinder.get_file_stat(file_path)

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size

    def get_file_stats(self):
        return {filename: FileFinder.get_file_stat(filename) for filename in self.file_stats.keys()}

    @set_interval(5)
    def watch_and_filter_files_by_stats_changes(self):
        file_stats_latest = self.get_file_stats()
        for file, size in self.file_stats.copy().items():
            if file_stats_latest[file] != size:
                print('Removing file due to size changes during monitoring: ', file)
                del self.file_stats[file]

    def filter_files_by_stat(self):
        # monitor the files for change in stats
        # start timer, the first call is in 2 seconds
        stop = self.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(20)
        # stop the timer
        stop.set()

    def find_files(self, directory, extension):
        self.find_all_files(directory, extension)
        self.filter_files_by_stat()
        return set(self.file_stats.keys())

finder = FileFinder()
while True:
    files_found = finder.find_files('/opt/edware/zones/landing/arrivals', '*.gpg')
    print(files_found)
    time.sleep(10)
