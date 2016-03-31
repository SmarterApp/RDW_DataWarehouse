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

__author__ = 'smuhit'

import os
from edudl2.fileloader.json_loader import load_json
from edudl2.udl2 import message_keys as mk
from uuid import uuid4
from sqlalchemy.sql import select
from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.database.udl2_connector import get_udl_connection, initialize_db_udl
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2.constants import Constants
from edudl2.sfv import sfv_util

STUDENT_REGISTRATION_JSON_COLUMNS = ['record_sid', 'guid_batch', 'guid_registration', 'academic_year',
                                     'extract_date', 'test_reg_id', 'callback_url', 'created_date']


class FunctionalTestLoadJsonToIntegrationTable(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTestLoadJsonToIntegrationTable, cls).setUpClass()
        initialize_db_udl(cls.udl2_conf)

    def setUp(self):
        self.udl2_conn = get_udl_connection()

    def tearDown(self):
        self.udl2_conn.close_connection()

    def generate_config(self, load_type, file, guid):
        results = sfv_util.get_source_target_column_values_from_ref_column_mapping(
            Constants.UDL2_JSON_LZ_TABLE, load_type)
        conf = {
            mk.GUID_BATCH: guid,
            mk.FILE_TO_LOAD: file,
            mk.MAPPINGS: dict([(row[0], row[1].split('.')) for row in results]),
            mk.TARGET_DB_TABLE: Constants.UDL2_JSON_INTEGRATION_TABLE(load_type),
            mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db_conn']['db_schema'],
            mk.TENANT_NAME: 'cat'
        }
        return conf

    def verify_json_load(self, load_type, conf, columns, guid):
        load_json(conf)

        sr_int_table = self.udl2_conn.get_table(Constants.UDL2_JSON_INTEGRATION_TABLE(load_type))
        query = select(['*'], sr_int_table.c.guid_batch == guid)
        result = self.udl2_conn.execute(query).fetchall()
        for row in result:
            self.assertEqual(len(row), len(columns), 'Unexpected number of columns')
            for column in columns:
                self.assertTrue(row[column], 'Expected column does not have data')

    def test_sr_json_load_to_int(self):
        batch_guid = str(uuid4())
        json_file = os.path.join(self.data_dir, 'student_registration_data', 'test_sample_student_reg.json')
        load_type = Constants.LOAD_TYPE_STUDENT_REGISTRATION
        conf = self.generate_config(load_type, json_file, batch_guid)

        columns = STUDENT_REGISTRATION_JSON_COLUMNS

        self.verify_json_load(load_type, conf, columns, batch_guid)
