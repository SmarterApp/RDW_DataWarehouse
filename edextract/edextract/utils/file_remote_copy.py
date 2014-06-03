'''
Created on Nov 7, 2013

@author: tosako
'''
from edcore.watch.mover import SendFileUtil
from edextract.settings.config import Config, get_setting

DEFAULT_TIMEOUT = 1800


def copy(filename, copy_info):
    tenant = copy_info['tenant']
    gatekeeper = copy_info['gatekeeper_id']
    hostname = copy_info['pickup_zone'][0]
    sftp_username = copy_info['pickup_zone'][1]
    private_key_file = copy_info['pickup_zone'][2]

    timeout = copy_info['timeout'] if 'timeout' in copy_info else DEFAULT_TIMEOUT

    SendFileUtil.remote_transfer_file(source_file=filename, hostname=hostname,
                                      remote_base_dir=get_setting(Config.PICKUP_ROUTE_BASE_DIR),
                                      file_tenantname=tenant, file_username=gatekeeper,
                                      sftp_username=sftp_username, private_key_file=private_key_file,
                                      timeout=timeout)
