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

__author__ = 'swimberly'

import time
import os
import shutil

from edudl2.udl2 import message_keys as mk
from edudl2.udl2.celery import udl2_conf
from edcore.watch.util import FileUtil
from edudl2.udl2.constants import Constants as Const
from edudl2.udl2_util.exceptions import InvalidTenantNameException


def move_file_from_arrivals(incoming_file, batch_guid, tenant_name):
    """
    Create the subdirectories for the current batch and mv the incoming file to the proper locations.
    :param incoming_file: the path the incoming file
    :param batch_guid: the guid for the current batch
    :param tenant_name: tenant name for the current batch
    :return: a tuple of (A dictionary containing all the created directories, the tenant name)
    """
    if not tenant_name:
        raise InvalidTenantNameException
    tenant_directory_paths = create_directory_paths(tenant_name, batch_guid)
    create_batch_directories(tenant_directory_paths)
    move_file_to_work(incoming_file, tenant_directory_paths.get(mk.ARRIVED))
    return tenant_directory_paths


def get_file_path_striped_extension(file_path, extension=Const.PROCESSING_FILE_EXT):
    """Returns file path striped extension if found

    :param file_path: file path as string
    :param extension: extension to be stripped (should include dot)
    """
    if not extension.startswith('.'):
        extension = ''.join(('.', extension))
    loc = file_path.rfind(extension)
    return file_path[:loc] if loc != -1 else file_path


def move_file_to_work(incoming_file, arrived_dir):
    """
    Copy the incoming source file to its arrived directory under the work folder
        and move the file pair(source and checksum file) to its history directory
    :param incoming_file: the path to the incoming file
    :param arrived_dir: the directory path to the arrived directory
    :param history_dir: the directory path to the history directory
    :return: None
    """

    shutil.move(incoming_file, arrived_dir)
    arrived_file_path = os.path.join(arrived_dir, os.path.basename(incoming_file))
    os.rename(arrived_file_path, get_file_path_striped_extension(arrived_file_path))


def create_directory_paths(tenant_name, batch_guid):
    """
    Create the path strings to all directories that need to be created for the batch
    :param tenant_name: The name of the tenant
    :param batch_guid: the batch guid for the current run
    :return: a dictionary containing the paths to all directories that need to be created
    """
    dir_name = time.strftime('%Y%m%d%H%M%S', time.gmtime())
    dir_name += '_' + batch_guid
    zones_config = udl2_conf.get('zones')
    if zones_config:
        work_zone = zones_config.get('work')
        directories = {
            mk.ARRIVED: os.path.join(work_zone, tenant_name, 'arrived', dir_name),
            mk.DECRYPTED: os.path.join(work_zone, tenant_name, 'decrypted', dir_name),
            mk.EXPANDED: os.path.join(work_zone, tenant_name, 'expanded', dir_name),
            mk.SUBFILES: os.path.join(work_zone, tenant_name, 'subfiles', dir_name),
            mk.HISTORY: os.path.join(zones_config.get('history'), tenant_name, dir_name)
        }
    return directories


def create_batch_directories(directory_dict):
    """
    Create all the directories in the given dict
    :param directory_dict: a dictionary of directories
    :return:
    """

    for directory in directory_dict.values():
        os.makedirs(directory, mode=0o755)
