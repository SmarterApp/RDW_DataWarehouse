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

    def __init__(self, file_path, block_size=256):
        """
        :param file_path: path of the file for which hash needs to be calculated
        :param block_size: read the file in chunks of size block_size (Defaults to 256) * Hashing Algorithm block size
        """
        self.file_path = file_path
        self.block_size = block_size

    def __str__(self):
        return repr(self.file_path)

    @abstractmethod
    def get_file_hash(self):
        """Returns the hash for the file"""
        pass


class MD5Hasher(FileHasher):

    def __init__(self, file_path, block_size=256, hex_digest=True):
        """
        :param file_path: path of the file for which md5 needs to be calculated
        :param block_size: read the file in chunks of size block_size * md5.block_size (Defaults to 4MB)
        :param hex_digest: Generate md5 digest as string object with only hexadecimal digits (Defaults to True)
        """
        super().__init__(file_path=file_path, block_size=block_size)
        self.hex_digest = hex_digest

    def md5_for_file(self):
        """Returns md5 secure hash for the file specified

        :returns hexadecimal or binary digest of the file contents
        """
        md5 = hashlib.md5()
        with open(self.file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(self.block_size * md5.block_size), b''):
                md5.update(chunk)
        if not self.hex_digest:
            return md5.digest()
        return md5.hexdigest()

    def get_file_hash(self):
        """Returns the md5 hash for the file"""
        if self.file_path is None or not os.path.exists(self.file_path):
            raise FileHasherException('Invalid file')
        return self.md5_for_file()

if __name__ == "__main__":
    md5 = MD5Hasher('/opt/edware/zones/landing/arrivals/ca/ca_user1/file_drop/test_source_file_tar_gzipped.tar.gz.gpg')
    hash = MD5Hasher(None)
    print(md5.get_file_hash())
    print(hash.get_file_hash())
