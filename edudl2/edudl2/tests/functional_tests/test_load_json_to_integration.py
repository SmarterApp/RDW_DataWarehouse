__author__ = 'smuhit'

from edudl2.fileloader.json_loader import load_json
from edudl2.udl2_util.udl_mappings import get_json_table_mapping
from edudl2.udl2 import message_keys as mk
from uuid import uuid4
from sqlalchemy.sql import select
from edudl2.database.udl2_connector import UDL2DBConnection
from edudl2.udl2.celery import udl2_conf
import os
import unittest

STUDENT_REGISTRATION_JSON_COLUMNS = ['record_sid', 'guid_batch', 'guid_registration', 'academic_year',
                                     'extract_date', 'test_reg_id', 'created_date']


class FunctionalTestLoadJsonToIntegrationTable(unittest.TestCase):

    def setUp(self):
        self.udl2_conn = UDL2DBConnection()

    def tearDown(self):
        self.udl2_conn.close_connection()

    def generate_config(self, load_type, file, guid):
        conf = {
            mk.GUID_BATCH: guid,
            mk.FILE_TO_LOAD: file,
            mk.MAPPINGS: get_json_table_mapping(load_type),
            mk.TARGET_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.TARGET_DB_TABLE: udl2_conf['udl2_db']['json_integration_tables'][load_type],
            mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
        }
        return conf

    def verify_json_load(self, load_type, conf, columns, guid):
        load_json(conf)

        sr_int_table = self.udl2_conn.get_table(udl2_conf['udl2_db']['json_integration_tables'][load_type])
        query = select(['*'], sr_int_table.c.guid_batch == guid)
        result = self.udl2_conn.execute(query).fetchall()
        for row in result:
            self.assertEqual(len(row), len(columns), 'Unexpected number of columns')
            for column in columns:
                self.assertTrue(row[column], 'Expected column does not have data')

    def test_sr_json_load_to_int(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        batch_guid = str(uuid4())
        json_file = os.path.join(data_dir, 'student_registration_data', 'test_sample_student_reg.json')
        load_type = udl2_conf['load_type']['student_registration']
        conf = self.generate_config(load_type, json_file, batch_guid)

        columns = STUDENT_REGISTRATION_JSON_COLUMNS

        self.verify_json_load(load_type, conf, columns, batch_guid)
