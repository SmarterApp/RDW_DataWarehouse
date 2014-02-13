__author__ = 'swimberly'

import os
import glob


def find_files_in_directories(directories, file_count=0, match_extension=None):
    """
    Given a list of directories, return a list of valid files for the pipeline
    :param directories: a list of directories as strings
    :param file_count: the max number of files to return
    :param match_extension: the file extension to look for in all files returned
    :return: a list of files
    """

    files = []
    extension = create_extension(match_extension) if match_extension else '*'

    for tenant_dir in directories:
        print("checking tenant directory:", tenant_dir)
        # sort files by time created and filter possible directories
        files += [x for x in glob.glob(os.path.join(tenant_dir, extension)) if not os.path.isdir(x)]

    print('files in dir', files)
    files_in_dir = sorted(files, key=lambda x: os.stat(x).st_mtime)
    print('files in dir', files_in_dir)

    return files_in_dir[:file_count] if file_count else files_in_dir


def create_extension(extension):
    """
    Given an extension prepend it with '*.' if not already present
    :param extension: The file extension to use
    :return: an extension that has been adjusted properly
    """
    if extension[0] == '*':
        return extension
    elif extension[0] == '.':
        return '*{}'.format(extension)
    return '*.{}'.format(extension)
