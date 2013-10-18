"""
Created on Oct 17, 2013

Module to initialize the sftp zones and creating groups
"""

__author__ = 'sravi'

import os
import subprocess
from src.sftp_config import sftp_conf


def _create_path_as_root(path):
    """
    create the path as root if not exists
    :param None
    :return: None
    """
    if not os.path.exists(path):
        # Run sudo mkdir path
        command_opts = ['sudo', 'mkdir', path]
        rtn_code = subprocess.call(command_opts)
        if rtn_code != 0:
            print('sudo mkdir %s failed' % path)


def _create_sftp_base_dir():
    """
    create sftp base dir if not exists
    :param None
    :return: None
    """
    if os.path.exists(sftp_conf['sftp_home']):
        _create_path_as_root(os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir']))


def _create_sftp_arrivals_zone():
    """
    create sftp arrivals zone
    :param None
    :return: None
    """
    if os.path.exists(os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'])):
        _create_path_as_root(os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'], sftp_conf['sftp_arrivals_dir']))


def _create_sftp_departures_zone():
    """
    create sftp departures zone
    :param None
    :return: None
    """
    if os.path.exists(os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'])):
        _create_path_as_root(os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'], sftp_conf['sftp_departures_dir']))


def initialize():
    _create_sftp_base_dir()
    _create_sftp_arrivals_zone()
    _create_sftp_departures_zone()
