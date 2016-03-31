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

'''
Created on Nov 7, 2013

@author: tosako
'''
from edcore.watch.mover import SendFileUtil
from edextract.settings.config import Config, get_setting

DEFAULT_TIMEOUT = 1800


def copy(filename, hostname, tenant, gatekeeper, sftp_username, private_key_file, timeout=1800):
    SendFileUtil.remote_transfer_file(source_file=filename, hostname=hostname,
                                      remote_base_dir=get_setting(Config.PICKUP_ROUTE_BASE_DIR),
                                      file_tenantname=tenant, file_username=gatekeeper,
                                      sftp_username=sftp_username, private_key_file=private_key_file,
                                      timeout=timeout)
