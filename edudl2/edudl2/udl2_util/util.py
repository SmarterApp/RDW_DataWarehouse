__author__ = 'sravi'

import os
from edudl2.udl2_util.file_util import convert_path_to_list
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2.constants import Constants


def get_tenant_name(incoming_file):
    """
    Given the incoming files path return the name of the tenant
    :param incoming_file: the path to the incoming file
    :return: A string containing the tenant name or None
    """
    zones_config = udl2_conf.get(Constants.ZONES)
    if zones_config:
        arrivals_dir_path = zones_config.get(Constants.ARRIVALS)
    if arrivals_dir_path and incoming_file.startswith(arrivals_dir_path):
        relative_file_path = os.path.relpath(incoming_file, arrivals_dir_path)
        folders = convert_path_to_list(relative_file_path)
        return folders[0] if len(folders) > 0 else None
    return None
