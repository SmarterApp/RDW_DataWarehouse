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

Module to configure sftp groups
"""

__author__ = 'sravi'

import subprocess
import sys
import grp


def _valid_group_name(name):
    """
    Check if group name is valid
    :param name: Name of SFTP group
    :return: True if group name is valid else False
    """
    return True if (name is not None) and len(name) > 0 else False


def _group_exists(name):
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
    return True if _group_exists(name) and len((grp.getgrnam(name)).gr_mem) > 0 else False


def _create_group(name):
    """
    create the group if not exists
    :param name: Name of SFTP group to be created
    :return: True if group created else false
    """
    if not _valid_group_name(name):
        print('Group name invalid')
        return False
    if not _group_exists(name):
        # Run groupadd group_name
        command_opts = ['groupadd', name]
        if sys.platform == 'linux':
            rtn_code = subprocess.call(command_opts)
            if rtn_code != 0:
                print('groupadd %s failed' % name)
                return False
        else:
            print('Not a Unix machine. Not adding group: %s' % name)
            return False
    else:
        print('Group %s already exists' % name)
        return False
    return True


def _remove_group(name):
    """
    remove the sftp group if exists
    :param name: Name of SFTP group to be removed
    :return: True if group removed else false
    """
    if _group_exists(name):
        if not _group_has_members(name):
            # Run groupdel group_name
            command_opts = ['groupdel', name]
            if sys.platform == 'linux':
                rtn_code = subprocess.call(command_opts)
                if rtn_code != 0:
                    print('groupdel %s failed' % name)
                    return False
            else:
                print('Not a Unix machine. Not removing group: %s' % name)
                return False
        else:
            print('Can not remove group %s . Group has members' % name)
            return False
    else:
        print('Group %s does not exists' % name)
        return False
    return True


def initialize(sftp_conf):
    group_name = sftp_conf['group']
    if _create_group(group_name):
        print('Group %s added successfully' % group_name)


def cleanup(sftp_conf):
    group_name = sftp_conf['group']
    if _remove_group(group_name):
        print('Group %s removed successfully' % group_name)
