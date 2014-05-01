from edudl2.udl2.W_load_from_integration_to_star import get_explode_to_tables_tasks,\
    create_target_schema
from celery.canvas import chain
from edudl2.udl2.W_tasks_utils import handle_group_results
__author__ = 'swimberly'

import os
import csv
from sqlalchemy.sql import select, func
from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.database.udl2_connector import get_target_connection, get_udl_connection
from edudl2.udl2.W_load_sr_integration_to_target import task as load_student_registration_data_to_target
from edudl2.udl2.constants import Constants

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
ASMT_OUTCOME_FILE = os.path.join(data_dir, 'INT_SBAC_ASMT_OUTCOME.csv')
ASMT_FILE = os.path.join(data_dir, 'INT_SBAC_ASMT.csv')
SR_FILE = os.path.join(data_dir, 'student_registration_data', 'INT_SBAC_STU_REG.csv')
SR_META_FILE = os.path.join(data_dir, 'student_registration_data', 'INT_SBAC_STU_REG_META.csv')


class FTestMoveToTarget(UDLTestHelper):

    guid_batch_asmt = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'
    guid_batch_sr = '75f1aa80-a459-406a-8529-c357ad0996ad'
    tenant_code = 'edware'

    @classmethod
    def setUpClass(cls):
        super(FTestMoveToTarget, cls).setUpClass()
        cls.create_schema_for_target(cls.tenant_code, cls.guid_batch_asmt)
        cls.create_schema_for_target(cls.tenant_code, cls.guid_batch_sr)

    @classmethod
    def tearDownClass(cls):
        super(FTestMoveToTarget, cls).tearDownClass()
        cls.drop_target_schema(cls.tenant_code, cls.guid_batch_asmt)
        cls.drop_target_schema(cls.tenant_code, cls.guid_batch_sr)

    def setUp(self):
        super(FTestMoveToTarget, self).setUp()

    def tearDown(self):
        pass

    def test_multi_tenant_move_to_target_assessment_data(self):
        udl2_conf['multi_tenant']['active'] = True
        self.verify_target_assessment_schema(self.guid_batch_asmt, True)
        self.load_csv_data_to_integration(ASMT_OUTCOME_FILE, ASMT_FILE, 'int_sbac_asmt_outcome', 'int_sbac_asmt')
        msg = self.create_msg(Constants.LOAD_TYPE_ASSESSMENT, self.guid_batch_asmt)
        dim_tasks = get_explode_to_tables_tasks(msg, 'dim')
        fact_tasks = get_explode_to_tables_tasks(msg, 'fact')
        tasks = chain(create_target_schema.s(msg), dim_tasks, handle_group_results.s(), fact_tasks, handle_group_results.s())
        results = tasks.delay()
        results.get()
        self.verify_target_assessment_schema(self.guid_batch_asmt, False)

    def test_multi_tenant_move_to_target_student_registration_data(self):
        udl2_conf['multi_tenant']['active'] = True
        self.verify_target_student_registration_schema(self.guid_batch_sr, True)
        self.load_csv_data_to_integration(SR_FILE, SR_META_FILE, 'int_sbac_stu_reg', 'int_sbac_stu_reg_meta')
        msg = self.create_msg(Constants.LOAD_TYPE_STUDENT_REGISTRATION, self.guid_batch_sr)
        load_student_registration_data_to_target(msg)
        self.verify_target_student_registration_schema(self.guid_batch_sr, False)

    def verify_target_assessment_schema(self, schema_name, is_empty=False):
        counts = self.get_counts(schema_name)
        if is_empty:
            self.assertEqual(counts[:5], (0, 0, 0, 0, 0))
        else:
            self.assertEqual(counts[:5], (99, 99, 1, 71, 94))
        return

    def verify_target_student_registration_schema(self, schema_name, is_empty=False):
        counts = self.get_counts(schema_name)
        if is_empty:
            self.assertEqual(counts[-1], 0)
        else:
            self.assertEqual(counts[-1], 10)
        return

    def get_counts(self, schema_name):
        with get_target_connection(self.tenant_code, schema_name) as conn:
            fact_select = select([func.count()]).select_from(conn.get_table('fact_asmt_outcome'))
            fact_primary_select = select([func.count()]).select_from(conn.get_table('fact_asmt_outcome_primary'))
            asmt_selct = select([func.count()]).select_from(conn.get_table('dim_asmt'))
            inst_select = select([func.count()]).select_from(conn.get_table('dim_inst_hier'))
            stud_select = select([func.count()]).select_from(conn.get_table('dim_student'))
            sr_select = select([func.count()]).select_from(conn.get_table('student_reg'))

            fact_count = conn.execute(fact_select).fetchall()[0][0]
            fact_primary_count = conn.execute(fact_primary_select).fetchall()[0][0]
            asmt_count = conn.execute(asmt_selct).fetchall()[0][0]
            inst_count = conn.execute(inst_select).fetchall()[0][0]
            stud_count = conn.execute(stud_select).fetchall()[0][0]
            sr_count = conn.execute(sr_select).fetchall()[0][0]
        return fact_count, fact_primary_count, asmt_count, inst_count, stud_count, sr_count

    def load_csv_data_to_integration(self, data_file, metadata_file, data_table_name, meta_table_name):

        with get_udl_connection() as udl2_conn:
            data_table = udl2_conn.get_table(data_table_name)
            metadata_table = udl2_conn.get_table(meta_table_name)
            data_dict_list = self.get_csv_dict_list(data_file)
            metadata_dict_list = self.get_csv_dict_list(metadata_file)
            udl2_conn.execute(metadata_table.insert(), metadata_dict_list)
            udl2_conn.execute(data_table.insert(), data_dict_list)

    def create_msg(self, load_type, guid_batch):
        return {
            mk.BATCH_TABLE: Constants.UDL2_BATCH_TABLE,
            mk.GUID_BATCH: guid_batch,
            mk.LOAD_TYPE: load_type,
            mk.PHASE: 4,
            mk.TENANT_NAME: self.tenant_code,
            mk.TARGET_DB_SCHEMA: guid_batch}

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
