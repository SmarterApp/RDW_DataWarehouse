__author__ = 'sravi'

import os
import threading
import fnmatch
from edcore.watch.constants import WatcherConstants as Const


class FileUtil:

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size if os.path.exists(filename) else None

    @staticmethod
    def file_contains_hash(file, file_hash):
        with open(file) as f:
            if file_hash in f.read():
                return True
        return False

    @staticmethod
    def get_complement_file_name(file):
        if fnmatch.fnmatch(file, '*' + Const.CHECKSUM_FILE_EXTENSION):
            # return corresponding source file path
            return file.strip(Const.CHECKSUM_FILE_EXTENSION)
        else:
            # return corresponding checksum file path
            return ''.join([file, Const.CHECKSUM_FILE_EXTENSION])


class FileCopyUtil:

    @staticmethod
    def remote_transfer_file(source_file):
        pass


def set_interval(interval):
    """Decorator to schedule method to run after every interval

    The method will be run in a separate thread and will run until explicitly stopped by the main thread
    To stop the scheduled method call set() on the returned event object

    :param interval: interval in seconds
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)
            t = threading.Thread(target=loop)
            t.daemon = True
            t.start()
            return stopped
        return wrapper
    return decorator
