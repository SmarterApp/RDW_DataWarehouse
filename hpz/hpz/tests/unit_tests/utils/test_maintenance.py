import unittest
import tempfile
import os
from hpz.utils.maintenance import cleanup
from hpz.tests.unit_tests.utils.unittest_with_hpz_sqlite import Unittest_with_hpz_sqlite
from hpz.database.hpz_connector import HPZDBConnection
from datetime import datetime, timedelta
from hpz.database.constants import HPZ
from uuid import uuid4

record_expiration = '7'


class Test(Unittest_with_hpz_sqlite):

    def tearDown(self):
        self.__tmp_dir.cleanup()

    def test_maintenance_purge_file(self):
        time_now = datetime.now()
        time_stamp_file = time_now - timedelta(days=20)  # 20 day old
        file = 'file1'
        self.__tmp_dir = tempfile.TemporaryDirectory()
        filename = os.path.join(self.__tmp_dir.name, file)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
                os.makedirs(dirname)
        open(os.path.join(filename), 'w').close()
        registration_id = uuid4()
        registration_info = {HPZ.FILE_PATH: filename,
                             HPZ.CREATE_DT: time_stamp_file,
                             HPZ.FILE_NAME: 'temp_file_1', HPZ.REGISTRATION_ID: str(registration_id),
                             HPZ.USER_ID: 'user_id_1'}
        with HPZDBConnection() as conn:
            file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
            conn.execute(file_reg_table.insert().values(registration_info))
        cleanup(record_expiration)
        self.assertFalse(os.path.exists(filename))
        with HPZDBConnection() as conn:
            file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
            result = conn.execute(file_reg_table.select().where(file_reg_table.c.registration_id == str(registration_id)))
            result = result.fetchone()
        self.assertIsNone(result)

    def test_maintenance_dont_purge_file(self):
        time_now = datetime.now()
        time_stamp_file = time_now - timedelta(days=1)  # 1 day old
        file = 'file2'
        self.__tmp_dir = tempfile.TemporaryDirectory()
        filename = os.path.join(self.__tmp_dir.name, file)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
                os.makedirs(dirname)
        open(os.path.join(filename), 'w').close()
        registration_id = uuid4()
        registration_info = {HPZ.FILE_PATH: filename,
                             HPZ.CREATE_DT: time_stamp_file,
                             HPZ.FILE_NAME: 'temp_file_2', HPZ.REGISTRATION_ID: str(registration_id),
                             HPZ.USER_ID: 'user_id_2'}
        with HPZDBConnection() as conn:
            file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
            conn.execute(file_reg_table.insert().values(registration_info))
        cleanup(record_expiration)
        self.assertTrue(os.path.exists(filename))
        with HPZDBConnection() as conn:
            file_reg_table = conn.get_table(table_name=HPZ.TABLE_NAME)
            result = conn.execute(file_reg_table.select().where(file_reg_table.c.registration_id == str(registration_id)))
            result = result.fetchone()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
