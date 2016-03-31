# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

"""
Created on Oct 17, 2013

Module to configure sftp zones
"""

__author__ = 'sravi'

import os
import sys
import shutil
import subprocess
from edsftp.src.util import create_path, change_owner


def _create_sftp_base_dir(sftp_conf):
    """
    create sftp base dir if not exists
    :param None
    :return: None
    """
    if os.path.exists(sftp_conf['home']):
        create_path(os.path.join(sftp_conf['home'], sftp_conf['base_dir']))


def _create_sftp_arrivals_zone(sftp_conf):
    """
    create sftp arrivals zone
    :param None
    :return: None
    """
    if os.path.exists(os.path.join(sftp_conf['home'], sftp_conf['base_dir'])):
        create_path(os.path.join(sftp_conf['home'], sftp_conf['base_dir'], sftp_conf['arrivals_dir']))


def _create_sftp_departures_zone(sftp_conf):
    """
    create sftp departures zone
    :param None
    :return: None
    """
    if os.path.exists(os.path.join(sftp_conf['home'], sftp_conf['base_dir'])):
        create_path(os.path.join(sftp_conf['home'], sftp_conf['base_dir'], sftp_conf['sftp_departures_dir']))


def _cleanup_sftp_zone(sftp_zone_path):
    """
    cleanup the sftp zone. Recursively removes all directory
    :param None
    :return: None
    """
    if os.path.exists(sftp_zone_path):
        shutil.rmtree(sftp_zone_path, True)


def initialize(sftp_conf):
    _create_sftp_base_dir(sftp_conf)
    _create_sftp_arrivals_zone(sftp_conf)
    _create_sftp_departures_zone(sftp_conf)
    print('SFTP zone initialized successfully')


def cleanup(sftp_conf):
    sftp_zone_path = os.path.join(sftp_conf['home'], sftp_conf['base_dir'])
    _cleanup_sftp_zone(sftp_zone_path)
    print('SFTP zone cleanedup successfully')
