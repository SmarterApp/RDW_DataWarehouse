'''
Created on Nov 9, 2013

@author: dip
'''
import os


def prepare_path(path):
    '''
    Create the directory if it doesn't exist

    :param string path: Path of the directory to create directory for
    '''
    if os.path.exists(path) is not True:
        os.makedirs(path, 0o700)


class File():
    def __init__(self, path, size):
        self.__path = path
        self.__size = size

    @property
    def name(self):
        return self.__path

    @property
    def size(self):
        return self.__size
