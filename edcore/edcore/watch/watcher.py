__author__ = 'sravi'

import os
import fnmatch
import time
import shutil
import hashlib
import logging
from edcore.watch.util import set_interval, Singleton

logger = logging.getLogger(__name__)

WATCH_INTERVAL_IN_SECONDS = 2


class Watcher(metaclass=Singleton):
    """File sync class to watch for complete files"""
    conf = None
    file_stats = {}

    def __init__(self):
        pass

    @classmethod
    def set_conf(cls, config):
        cls.conf = config
        cls.clear_file_stats()
        global WATCH_INTERVAL_IN_SECONDS
        WATCH_INTERVAL_IN_SECONDS = cls.conf['file_stat_watch_internal_in_seconds']
        cls.source_path = os.path.join(cls.conf['base_dir'], cls.conf['source_dir'])
        cls.dest_path = os.path.join(cls.conf['base_dir'], cls.conf['dest_dir']) if 'dest_dir' in cls.conf else None

    @staticmethod
    def get_file_stat(filename):
        return os.stat(filename).st_size if os.path.exists(filename) else None

    @staticmethod
    def md5_for_file(path, block_size=256, hex_digest=True):
        """Returns md5 secure hash for the file specified

        :param path: path of the file for which md5 hash needs to be generated
        :param block_size: read the file in chunks of size block_size * md5.block_size (Defaults to 4MB)
        :param hex_digest: Generate md5 digest as string object with only hexadecimal digits

        :returns hexadecimal or simple digest of the file contents
        """
        md5 = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size * md5.block_size), b''):
                md5.update(chunk)
        if not hex_digest:
            return md5.digest()
        return md5.hexdigest()

    @staticmethod
    def get_file_hash(file):
        return Watcher.md5_for_file(file)

    @staticmethod
    def file_contains_hash(file, file_hash):
        with open(file) as f:
            if file_hash in f.read():
                return True
        return False

    @staticmethod
    def valid_check_sum(file):
        checksum_file = Watcher.get_complement_file_name(file)
        if not os.path.exists(file) or not os.path.exists(checksum_file):
            return False
        file_hash = Watcher.get_file_hash(file)
        return Watcher.file_contains_hash(checksum_file, file_hash)

    @staticmethod
    def get_complement_file_name(file):
        if fnmatch.fnmatch(file, '*.done'):
            # return corresponding source file
            return file.strip('.done')
        else:
            # return corresponding '.done' file
            return ''.join([file, '.done'])

    @classmethod
    def clear_file_stats(cls):
        cls.file_stats.clear()

    @classmethod
    def get_file_stats(cls):
        return cls.file_stats

    @classmethod
    def find_all_files(cls):
        for root, dirs, files in os.walk(cls.source_path):
            filtered_files = [filename for pattern in set(cls.conf['file_patterns_to_watch'])
                              for filename in fnmatch.filter(files, pattern)]
            for filename in filtered_files:
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
                cls.remove_file_pair_from_dict(file)

    @classmethod
    def watch_files(cls):
        """Watches the files for the defined duration and discards file undergoing change"""
        # monitor the files for change in stats
        stop = cls.watch_and_filter_files_by_stats_changes()
        # monitor for a duration
        time.sleep(float(cls.conf['file_stat_watch_period_in_seconds']))
        # stop the timer
        stop.set()

    @classmethod
    def remove_file_from_dict(cls, file):
        cls.file_stats.pop(file, None)

    @classmethod
    def remove_file_pair_from_dict(cls, file):
        # check the file being removed and remove the corresponding pair file
        cls.remove_file_from_dict(cls.get_complement_file_name(file))
        # remove the main file
        cls.remove_file_from_dict(file)

    @classmethod
    def filter_files_for_digest_mismatch(cls):
        """Verifies checksum for all the files (ignoring '*.done' files) currently being watched"""
        all_files = cls.get_file_stats().copy().keys()
        # filter out the '*.done' files which will contain the checksum for a corresponding source file
        source_files = set(all_files) - set(fnmatch.filter(all_files, '*.done'))
        for file in source_files:
            if not cls.valid_check_sum(file):
                print('Removing file {file} due to invalid hash'.format(file=file))
                cls.remove_file_pair_from_dict(file)

    @classmethod
    def filter_checksum_files(cls):
        """Remove '*.done' files"""
        for file in set(fnmatch.filter(cls.get_file_stats().copy().keys(), '*.done')):
            cls.remove_file_from_dict(file)

    @classmethod
    def move_files(cls):
        files_to_move = cls.get_file_stats().keys()
        for file in files_to_move:
            destination_file_path = os.path.join(cls.dest_path, os.path.relpath(file, cls.source_path))
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
    def find_files(cls):
        cls.clear_file_stats()
        cls.assert_inputs()
        cls.find_all_files()

    @classmethod
    def watch_and_move_files(cls):
        cls.find_files()
        cls.watch_files()
        files_moved = cls.move_files()
        return files_moved

    @classmethod
    def find_udl_ready_files(cls):
        cls.find_files()
        cls.watch_files()
        cls.filter_files_for_digest_mismatch()
        cls.filter_checksum_files()
        return cls.get_file_stats()
