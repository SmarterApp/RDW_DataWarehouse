__author__ = 'swimberly'

import os
import fnmatch


def find_files_in_directories(directory, file_count=0, match_extension=None):
    """
    Given a list of directories, return a list of valid files for the pipeline
    :param directories: a list of directories as strings
    :param file_count: the max number of files to return
    :param match_extension: the file extension to look for in all files returned
    :return: a list of files
    """

    extension = create_extension(match_extension) if match_extension else '*'
    files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, extension):
            files.append(os.path.join(root, filename))

    files_in_dir = sorted(files, key=lambda x: os.stat(x).st_mtime)

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
