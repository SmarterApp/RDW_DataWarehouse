'''
Created on Nov 7, 2013

@author: tosako
'''
from edcore.watch.mover import SendFileUtil
from edextract.settings.config import Config, get_setting


def copy(filename, hostname, tenant, gatekeeper, sftp_username, private_key_file, timeout=1800):
    SendFileUtil.remote_transfer_file(source_file=filename, hostname=hostname,
                                      remote_base_dir=get_setting(Config.PICKUP_ROUTE_BASE_DIR),
                                      file_tenantname=tenant, file_username=gatekeeper,
                                      sftp_username=sftp_username, private_key_file=private_key_file,
                                      timeout=timeout)
