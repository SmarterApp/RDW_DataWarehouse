"""
Created on Oct 17, 2013

Module to configure sftp groups
"""

__author__ = 'sravi'

import subprocess
import sys

def _create_group(name):
    """
    create the group if not exists
    :param name: Name of SFTP group to be created
    :return: None
    """
    # Run groupadd group_name
    command_opts = ['groupadd', name]
    if sys.platform == 'linux':
        rtn_code = subprocess.call(command_opts)
        if rtn_code != 0:
            print('groupadd %s failed' % name)
    else:
        None


def initialize(sftp_conf):
    for group_name in sftp_conf['groups']:
        _create_group(group_name)
