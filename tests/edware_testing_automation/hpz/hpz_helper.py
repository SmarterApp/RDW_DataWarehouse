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

import os
import subprocess

from requests_toolbelt import MultipartEncoder
from sqlalchemy.sql import select

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.utils.db_connector import DBConnection
from edware_testing_automation.utils.preferences import preferences, HPZ


class HpzHelper(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def set_headers_for_file_upload(self, file_name, file_name_with_path):
        stream = MultipartEncoder(
            fields={'file': (file_name, open(file_name_with_path, 'rb'), 'application/octet-stream')})
        self.set_non_json_payload(stream)
        self.set_request_header('Content-Type', stream.content_type)
        self.update_request_header('File-Name', file_name)

    def set_headers_for_file_registration(self, user):
        self.set_payload({'uid': user})

    def check_db_for_registration(self, reg_id):
        with DBConnection(name='hpz') as connector:
            table = connector.get_table(self.reg_table)
            query = select([table]).where(table.c.registration_id == reg_id)
            result = connector.execute(query).fetchall()
            self.assertTrue(result, 'Registration not stored in db')

    def check_db_for_no_registration(self, reg_id):
        with DBConnection(name='hpz') as connector:
            table = connector.get_table(self.reg_table)
            query = select([table]).where(table.c.registration_id == reg_id)
            result = connector.execute(query).fetchall()
            self.assertFalse(result, 'Registration is in db')

    def check_db_for_upload(self, reg_id):
        with DBConnection(name='hpz') as connector:
            table = connector.get_table(self.reg_table)
            query = select([table.c.file_path]).where(table.c.registration_id == reg_id)
            result = connector.execute(query).fetchall()
            self.assertNotEqual(result, [(None,)])

    def call_cleanup_script(self, expiration, config):
        cleanup_script_path = os.path.abspath(os.path.dirname(__file__)) + preferences(
            HPZ.cleanup_script_relative_location)
        subprocess.call('python {0} -e {1} -c {2}'.format(cleanup_script_path, str(expiration), config), shell=True)
