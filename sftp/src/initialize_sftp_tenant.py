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


def remove_tenant(tenant, sftp_conf):
    """
    Remove a tenants directories
    :param tenant: The name of the tenant
    :param sftp_conf: sftp configuration information
    :return: None
    """
    arrivals_path = create_tenant_path_string(tenant, sftp_conf, True)
    departures_path = create_tenant_path_string(tenant, sftp_conf, False)
    cleanup_directory(arrivals_path)
    cleanup_directory(departures_path)


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


#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description="Script to create a tenant in the sftp system")
#    parser.add_argument('-t', '--tenant', required=True, help="The name of the tenant")
#    parser.add_argument('-d', '--delete', action='store_true', help="Delete the given tenant")
#    args = parser.parse_args()
#
#    if args.delete:
#        remove_tenant(args.tenant, sftp.src.sftp_config)
#    else:
#        create_tenant(args.tenant, sftp.src.sftp_config)