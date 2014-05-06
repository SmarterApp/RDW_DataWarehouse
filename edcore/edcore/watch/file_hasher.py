__author__ = 'sravi'

import hashlib
import os
from abc import ABCMeta, abstractmethod


class FileHasherException(Exception):
    '''
    generic file hasher exception
    '''
    def __init__(self, msg='File Hasher Generic Exception'):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)


class FileHasher(object):
    """Abstract base class for File Hashing"""
    __metaclass__ = ABCMeta

    def __init__(self, block_size=256):
        """
        :param block_size: read the file in chunks of size block_size (Defaults to 256) * Hashing Algorithm block size
        """
        self.block_size = block_size

    @abstractmethod
    def get_file_hash(self, file_path):
        """Returns the hash for the file

        :param file_path: path to the file to compute hash
        """
        pass


class MD5Hasher(FileHasher):

    def __init__(self, block_size=256, hex_digest=True):
        """
        :param block_size: read the file in chunks of size block_size * md5.block_size (Defaults to 4MB)
        :param hex_digest: Generate md5 digest as string object with only hexadecimal digits (Defaults to True)
        """
        super().__init__(block_size=block_size)
        self.hex_digest = hex_digest

    def _md5_for_file(self, file_path):
        """Returns md5 secure hash for the file specified

        :returns hexadecimal or binary digest of the file contents
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(self.block_size * md5.block_size), b''):
                md5.update(chunk)
        if not self.hex_digest:
            return md5.digest()
        return md5.hexdigest()

    def get_file_hash(self, file_path):
        """Returns the md5 hash for the file

        :param file_path: path to the file to compute md5
        """
        if file_path is None or not os.path.exists(file_path):
            raise FileHasherException('Invalid file')
        return self._md5_for_file(file_path)
