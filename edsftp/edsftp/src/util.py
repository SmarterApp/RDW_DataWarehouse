__author__ = 'swimberly'

import os
import shutil
import grp


def create_path(path):
    """
    create the path if not exists
    :param path: the path of the directory to create
    :type path: str
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path, 0o755)


def cleanup_directory(sftp_dir_path):
    """
    cleanup the sftp zone. Recursively removes all directory
    :param None
    :return: None
    """
    if os.path.exists(sftp_dir_path):
        shutil.rmtree(sftp_dir_path, True)


def group_exists(name):
    """
    Check if group exists
    :param name: Name of SFTP group
    :return: True if group exists else False
    """
    try:
        grp.getgrnam(name)
        return True
    except KeyError:
        return False


def change_owner(path, user, group):
    shutil.chown(path, user, group)


