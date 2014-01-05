__author__ = 'swimberly'

import os
from edsftp.src.util import create_path


def create_tenant(tenant, sftp_conf):
    '''
    Create the necessary directories for the given tenant
    :param tenant: The name of the tenant
    :param sftp_conf: The configuration information for the tenant
    :return: None
    '''
    dir_list = create_list_of_dirs_for_tenant(tenant, sftp_conf)

    print('Directories created for tenant:')
    for path in dir_list:
        create_path(path)
        os.chmod(path, 0o755)
        print('\t', path)


def remove_tenant(tenant, sftp_conf):
    """
    Remove a tenants directories
    :param tenant: The name of the tenant
    :param sftp_conf: sftp configuration information
    :return: None
    """
    dir_list = create_list_of_dirs_for_tenant(tenant, sftp_conf)

    print('Directories removed for tenant:')
    try:
        for path in dir_list:
            os.rmdir(path)
            print('\t', path)
    except OSError:
        print("All users must be removed before tenant can be removed")


def create_list_of_dirs_for_tenant(tenant, sftp_conf):
    """
    Create a list of directory strings that are necessary for the tenant to be created
    :param tenant: The name of the tenant
    :param sftp_conf: The configuration information for the tenant
    :return: None
    """
    return [create_tenant_path_string(tenant, sftp_conf, True),
            create_tenant_path_string(tenant, sftp_conf, False),
            create_tenant_home_folder_string(tenant, sftp_conf, True),
            create_tenant_home_folder_string(tenant, sftp_conf, False)]


def create_tenant_path_string(tenant, sftp_conf, is_arrivals=True):
    """
    Create the path for the tenant
    :param tenant: the tenant name to use for creating the path
    :param sftp_conf: the sftp configuration dictionary
    :param is_arrivals: create the arrivals directory or the departures directory
    :return: a string containing the path to be created
    """
    zone_str = sftp_conf['sftp_arrivals_dir'] if is_arrivals else sftp_conf['sftp_departures_dir']
    tenant_path = os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'], zone_str, tenant)
    return tenant_path


def create_tenant_home_folder_string(tenant, sftp_conf, is_arrivals=True):
    """
    Create the home directory path for the tenant
    This path is almost the same as
    :param tenant: the tenant name to use for creating the path
    :param sftp_conf: the sftp configuration dictionary
    :param is_arrivals: create the arrivals directory or the departures directory
    :return: a string containing the path to be created
    """
    zone_str = sftp_conf['sftp_arrivals_dir'] if is_arrivals else sftp_conf['sftp_departures_dir']
    tenant_path = os.path.join(sftp_conf['user_home_base_dir'], zone_str, tenant)
    return tenant_path
