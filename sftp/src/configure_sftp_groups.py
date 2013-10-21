"""
Created on Oct 17, 2013

Module to configure sftp groups
"""

__author__ = 'sravi'

import subprocess
import sys
import grp


def _group_exits(name):
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


def _group_has_members(name):
    """
    Check if group has members
    :param name: Name of SFTP group
    :return: True if group has members else False
    """
    return True if _group_exits(name) and len((grp.getgrnam(name)).gr_mem) > 0 else False


def _create_group(name):
    """
    create the group if not exists
    :param name: Name of SFTP group to be created
    :return: None
    """
    if not _group_exits(name):
        # Run groupadd group_name
        command_opts = ['groupadd', name]
        if sys.platform == 'linux':
            rtn_code = subprocess.call(command_opts)
            if rtn_code != 0:
                print('groupadd %s failed' % name)
            print('Group %s added successfully' % name)
        else:
            print('Not a Unix machine. Not adding group: %s' % name)
    else:
        print('Group %s already exists' % name)


def _remove_group(name):
    """
    remove the sftp group if exists
    :param name: Name of SFTP group to be removed
    :return: None
    """
    if _group_exits(name):
        if not _group_has_members(name):
            pass
            print('Group %s removed successfully' % name)
        else:
            print('Can not remove group %s . Group has members' % name)
    else:
        print('Group %s does not exists' % name)


def initialize(sftp_conf):
    for group_name in sftp_conf['groups']:
        _create_group(group_name)


def cleanup(sftp_conf):
    for group_name in sftp_conf['groups']:
        _remove_group(group_name)
