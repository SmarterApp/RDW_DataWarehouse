'''
Created on Nov 9, 2013

@author: dip
'''
import os
from edextract.exceptions import NotFileException
import copy


def prepare_path(path):
    '''
    Create the directory if it doesn't exist

    :param string path: Path of the directory to create directory for
    '''
    if os.path.exists(path) is not True:
        os.makedirs(path, 0o700)


class File():
    def __init__(self, path):
        if os.path.isfile(path):
            self.__path = path
            self.__size = os.stat(path).st_size
        else:
            raise NotFileException(path + 'is not file')

    @property
    def name(self):
        return self.__path

    @property
    def size(self):
        return self.__size


def _read_dirs(parent_dir):
    files = []
    for _root, _dirs, _files in os.walk(parent_dir):
        for _file in _files:
            _path = os.path.join(_root, _file)
            files.append(File(_path))
    return files


def generate_file_group(parent_dir, threshold_size):
    files = _read_dirs(parent_dir)
    file_group = []
    page = []
    file_total_size = 0
    for file in files:
        if float(file_total_size) + float(file.size) > float(threshold_size):
            file_group.append(copy.deepcopy(page))
            del page[:]
            page.append(file)
            file_total_size = file.size
        else:
            file_total_size += file.size
            page.append(file)
    if page:
        file_group.append(page)
    return file_group
