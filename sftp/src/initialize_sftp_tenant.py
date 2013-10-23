__author__ = 'swimberly'

import os

from src.util import create_path, cleanup_directory


def create_tenant(tenant, sftp_conf):
    """
    Create the necessary directories for the given tenant
    :param tenant: The name of the tenant
    :param sftp_conf: The configuration information for the tenant
    :return: None
    """

    arrivals_path = create_tenant_path_string(tenant, sftp_conf, True)
    departures_path = create_tenant_path_string(tenant, sftp_conf, False)
    create_path(arrivals_path)
    create_path(departures_path)
    print('Directories created for tenant:')
    print('\t', arrivals_path)
    print('\t', departures_path)


def remove_tenant(tenant, sftp_conf):
    """
    Remove a tenants directories
    :param tenant: The name of the tenant
    :param sftp_conf: sftp configuration information
    :return: None
    """
    arrivals_path = create_tenant_path_string(tenant, sftp_conf, True)
    departures_path = create_tenant_path_string(tenant, sftp_conf, False)
    try:
        os.rmdir(arrivals_path)
        os.rmdir(departures_path)
        print('Directories removed for tenant:')
        print('\t', arrivals_path)
        print('\t', departures_path)
    except OSError:
        print("All users must be removed before tenant can be removed")


def create_tenant_path_string(tenant, sftp_conf, is_arrivals=True):
    """
    Create the path for the tenant
    :param tenant:
    :param sftp_conf:
    :param is_arrivals:
    :return:
    """
    zone_str = sftp_conf['sftp_arrivals_dir'] if is_arrivals else sftp_conf['sftp_departures_dir']
    tenant_path = os.path.join(sftp_conf['sftp_home'], sftp_conf['sftp_base_dir'], zone_str, tenant)
    return tenant_path
