__author__ = 'swimberly'

import os
import shutil


def create_path(path):
    """
    create the path if not exists
    :param path: the path of the directory to create
    :type path: str
    :return: None
    """
    if not os.path.exists(path):
        os.mkdir(path, 0o755)


def cleanup_directory(sftp_dir_path):
    """
    cleanup the sftp zone. Recursively removes all directory
    :param None
    :return: None
    """
    if os.path.exists(sftp_dir_path):
        shutil.rmtree(sftp_dir_path, True)