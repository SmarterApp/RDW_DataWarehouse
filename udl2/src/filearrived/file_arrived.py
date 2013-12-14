__author__ = 'swimberly'

import time
import os
import shutil

from udl2 import message_keys as mk
from udl2.celery import udl2_conf
from udl2_util.file_util import convert_path_to_list


def move_file_from_arrivals(incoming_file, batch_guid, tenant_name_pos=None):
    """
    Create the subdirectories for the current batch and mv the incoming file to the proper locations.
    :param incoming_file: the path the incoming file
    :param batch_guid: the guid for the current batch
    :param tenant_name_pos: the position of where the tenant name is located in the incoming_file
        path
    :return: a tuple of (A dictionary containing all the created directories, the tenant name)
    """
    tenant_name_pos = tenant_name_pos if tenant_name_pos else udl2_conf['tenant_position']
    tenant_name = get_tenant_name(incoming_file, tenant_name_pos)
    tenant_directory_paths = create_directory_paths(tenant_name, batch_guid)
    create_batch_directories(tenant_directory_paths)
    move_file_to_work_and_history(incoming_file, tenant_directory_paths[mk.ARRIVED], tenant_directory_paths[mk.HISTORY])
    return tenant_directory_paths, tenant_name


def move_file_to_work_and_history(incoming_file, arrived_dir, history_dir):
    """
    Move the incoming file to its arrived directory under the work folder
        and move it to its history directory
    :param incoming_file: the path to the incoming file
    :param arrived_dir: the directory path to the arrived directory
    :param history_dir: the directory path to the history directory
    :return: None
    """
    shutil.copy2(incoming_file, arrived_dir)
    shutil.move(incoming_file, history_dir)


def get_tenant_name(incoming_file, tenant_path_pos):
    """
    Given the incoming files path return the name of the tenant
    :param incoming_file: the path to the incoming file
    :param tenant_path_pos: the position of the tenant in the
    :return: A string containing the tenant name
    """
    return convert_path_to_list(incoming_file)[tenant_path_pos]


def create_directory_paths(tenant_name, batch_guid):
    """
    Create the path strings to all directories that need to be created for the batch
    :param tenant_name: The name of the tenant
    :param batch_guid: the batch guid for the current run
    :return: a dictionary containing the paths to all directories that need to be created
    """
    dir_name = time.strftime('%Y%m%d%H%M%S', time.gmtime())
    dir_name += '_' + batch_guid

    directories = {
        mk.ARRIVED: os.path.join(udl2_conf['zones']['work'], tenant_name,
                                 udl2_conf['work_zone_sub_dir']['arrived'], dir_name),
        mk.DECRYPTED: os.path.join(udl2_conf['zones']['work'], tenant_name,
                                   udl2_conf['work_zone_sub_dir']['decrypted'], dir_name),
        mk.EXPANDED: os.path.join(udl2_conf['zones']['work'], tenant_name,
                                  udl2_conf['work_zone_sub_dir']['expanded'], dir_name),
        mk.SUBFILES: os.path.join(udl2_conf['zones']['work'], tenant_name,
                                  udl2_conf['work_zone_sub_dir']['subfiles'], dir_name),
        mk.HISTORY: os.path.join(udl2_conf['zones']['history'], tenant_name, dir_name)
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
