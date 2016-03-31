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

import unittest
import tempfile
import os
from hpz.utils.maintenance import cleanup
from hpz.tests.unit_tests.utils.unittest_with_hpz_sqlite import Unittest_with_hpz_sqlite
from hpz.database.hpz_connector import HPZDBConnection
from datetime import datetime, timedelta
from hpz.database.constants import HPZ
from uuid import uuid4


class Test(Unittest_with_hpz_sqlite):

    def setUp(self):
        self.__settings = {'hpz.record_expiration': '7'}
        self.__file1_details = {'filename': 'file1', 'days': 20, 'user_id': 'user_id_1'}  # file that will be purged
        self.__file2_details = {'filename': 'file2', 'days': 1, 'user_id': 'user_id_2'}  # file that wont be purged
        time_now = datetime.now()
        self.__tmp_dir = tempfile.TemporaryDirectory()
        for file_details in [self.__file1_details, self.__file2_details]:
            time_stamp_file = time_now - timedelta(days=file_details['days'])
            file = file_details['filename']
            full_file_path = os.path.join(self.__tmp_dir.name, file)
            file_details['full_file_path'] = full_file_path
            dirname = os.path.dirname(full_file_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            open(os.path.join(full_file_path), 'w').close()
            registration_id = uuid4()
            file_details['registration_id'] = str(registration_id)
            registration_info = {HPZ.FILE_PATH: full_file_path,
                                 HPZ.CREATE_DT: time_stamp_file,
                                 HPZ.FILE_NAME: file_details['filename'], HPZ.REGISTRATION_ID: str(registration_id),
                                 HPZ.USER_ID: file_details['filename']}
            with HPZDBConnection() as conn:
                file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
                conn.execute(file_reg_table.insert().values(registration_info))

    def tearDown(self):
        self.__tmp_dir.cleanup()

    def test_maintenance_purge_file(self):
        cleanup(self.__settings)
        self.assertFalse(os.path.exists(self.__file1_details['full_file_path']))
        with HPZDBConnection() as conn:
            file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
            result = conn.execute(file_reg_table.select().where(file_reg_table.c.registration_id == self.__file1_details['registration_id']))
            result = result.fetchone()
        self.assertIsNone(result)

    def test_maintenance_dont_purge_file(self):
        cleanup(self.__settings)
        self.assertTrue(os.path.exists(self.__file2_details['full_file_path']))
        with HPZDBConnection() as conn:
            file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
            result = conn.execute(file_reg_table.select().where(file_reg_table.c.registration_id == self.__file2_details['registration_id']))
            result = result.fetchone()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
