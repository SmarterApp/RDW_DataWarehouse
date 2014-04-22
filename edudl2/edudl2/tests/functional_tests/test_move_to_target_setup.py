__author__ = 'swimberly'

import os
import csv
from sqlalchemy.sql import select, func
from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.W_load_from_integration_to_star import explode_to_dims, explode_to_facts
from edudl2.database.udl2_connector import get_target_connection, get_udl_connection

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
ASMT_OUTCOME_FILE = os.path.join(data_dir, 'INT_SBAC_ASMT_OUTCOME.csv')
ASMT_FILE = os.path.join(data_dir, 'INT_SBAC_ASMT.csv')


class FTestMoveToTarget(UDLTestHelper):

    guid_batch = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'
    tenant_code = 'edware'

    @classmethod
    def setUpClass(cls):
        super(FTestMoveToTarget, cls).setUpClass()
        cls.create_schema_for_target(cls.tenant_code, cls.guid_batch)

    @classmethod
    def tearDownClass(cls):
        super(FTestMoveToTarget, cls).tearDownClass()
        cls.drop_target_schema(cls.tenant_code, cls.guid_batch)

    def setUp(self):
        super(FTestMoveToTarget, self).setUp()

    def tearDown(self):
        pass

    def test_multi_tenant_target_database(self):
        self.check3_entire_assessment_load_to_star_stage_with_multi_tenancy()

    def check3_entire_assessment_load_to_star_stage_with_multi_tenancy(self):
        udl2_conf['multi_tenant']['active'] = True
        self.verify_target_assessment_schema(True)
        self.read_csv_data_to_dict(ASMT_OUTCOME_FILE, ASMT_FILE)
        msg = self.create_msg('assessment')
        explode_to_dims(msg)
        explode_to_facts(msg)
        self.verify_target_assessment_schema(False)

    def verify_target_assessment_schema(self, is_empty=False):
        counts = self.get_counts()
        if is_empty:
            self.assertEqual(counts[:5], (0, 0, 0, 0, 0))
        else:
            self.assertEqual(counts[:5], (99, 99, 1, 71, 94))
        return

    def get_counts(self):
        with get_target_connection(self.tenant_code, self.guid_batch) as conn:
            fact_select = select([func.count()]).select_from(conn.get_table('fact_asmt_outcome'))
            fact_primary_select = select([func.count()]).select_from(conn.get_table('fact_asmt_outcome_primary'))
            asmt_selct = select([func.count()]).select_from(conn.get_table('dim_asmt'))
            inst_select = select([func.count()]).select_from(conn.get_table('dim_inst_hier'))
            stud_select = select([func.count()]).select_from(conn.get_table('dim_student'))

            fact_count = conn.execute(fact_select).fetchall()[0][0]
            fact_primary_count = conn.execute(fact_primary_select).fetchall()[0][0]
            asmt_count = conn.execute(asmt_selct).fetchall()[0][0]
            inst_count = conn.execute(inst_select).fetchall()[0][0]
            stud_count = conn.execute(stud_select).fetchall()[0][0]
        return fact_count, fact_primary_count, asmt_count, inst_count, stud_count

    def read_csv_data_to_dict(self, data_file, metadata_file):

        with get_udl_connection() as udl2_conn:
            data_table = udl2_conn.get_table('int_sbac_asmt_outcome')
            metadata_table = udl2_conn.get_table('int_sbac_asmt')
            data_dict_list = self.get_csv_dict_list(data_file)
            metadata_dict_list = self.get_csv_dict_list(metadata_file)
            udl2_conn.execute(metadata_table.insert(), metadata_dict_list)
            udl2_conn.execute(data_table.insert(), data_dict_list)

    def create_msg(self, load_type):
        return {
            mk.BATCH_TABLE: udl2_conf['udl2_db']['batch_table'],
            mk.GUID_BATCH: self.guid_batch,
            mk.LOAD_TYPE: udl2_conf['load_type'][load_type],
            mk.PHASE: 4,
            mk.TENANT_NAME: self.tenant_code,
            mk.TARGET_DB_SCHEMA: self.guid_batch}

    def get_csv_dict_list(self, filename):
        """
        Read the csv file and pull out the data and place in a list of dictionaries
        :param filename: The name of the file
        :return: A list of dictionaries mapping to the values in the csv file.
            Uses the first line as dict keys
        """
        row_dict_list = []
        with open(filename, 'r') as af:
            csv_reader = csv.DictReader(af)
            for row in csv_reader:
                clean_row = self.clean_dictionary_values(row)
                row_dict_list.append(clean_row)
        return row_dict_list

    def clean_dictionary_values(self, val_dict):
        """
        Take a row dictionary and replace all empty strings with None value
        :param val_dict: The dictionary for the given row
        :return: A cleaned dictionary
        """
        for k, v in val_dict.items():
            if v == '':
                val_dict[k] = None

        return val_dict
