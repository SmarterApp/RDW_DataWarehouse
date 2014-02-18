__author__ = 'swimberly'

import unittest
import os
import csv

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.sql import select, func
from sqlalchemy.exc import ProgrammingError

from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edschema.metadata.ed_metadata import generate_ed_metadata
from edudl2.udl2_util.database_util import connect_db, get_sqlalch_table_object
from edudl2.move_to_target.move_to_target_setup import get_tenant_target_db_information
from edudl2.udl2.W_load_from_integration_to_star import explode_to_dims, explode_to_fact

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
ASMT_OUTCOME_FILE = os.path.join(data_dir, 'INT_SBAC_ASMT_OUTCOME.csv')
ASMT_FILE = os.path.join(data_dir, 'INT_SBAC_ASMT.csv')
BATCH_GUID = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'


class FTestMoveToTarget(unittest.TestCase):

    ###
    # Setup and Teardown code
    ####
    def setUp(self):
        self.tenant_info = {
            'tenant_code': 'func_tests',
            'tenant_name': 'ftest_test_tenant',
            'target_db_host': udl2_conf['target_db']['db_host'],
            'target_db_name': udl2_conf['target_db']['db_database'],
            'target_schema_name': 'ftest_test_schema',
            'target_schema_port': udl2_conf['target_db']['db_port'],
            'target_schema_user_name': udl2_conf['target_db']['db_user'],
            'target_schema_passwd': udl2_conf['target_db']['db_pass']
        }
        con_string = '{driver}://{user}:{passwd}@{host}:{port}/{db}'.format(driver=udl2_conf['target_db']['db_driver'],
                                                                            user=udl2_conf['target_db']['db_user'],
                                                                            passwd=udl2_conf['target_db']['db_pass'],
                                                                            host=udl2_conf['target_db']['db_host'],
                                                                            port=udl2_conf['target_db']['db_port'],
                                                                            db=udl2_conf['target_db']['db_database'])
        # Connect to the target db and create a schema for the tenant
        self.target_engine = create_engine(con_string, echo=True)
        self.target_connection = self.target_engine.connect()
        try:
            self.target_connection.execute(CreateSchema(self.tenant_info['target_schema_name']))
        except ProgrammingError as e:
            # if exception raised because table already exists, remove table and try again
            if 'schema "ftest_test_schema" already exists' in str(e):
                self.target_connection.execute(DropSchema(self.tenant_info['target_schema_name'], cascade=True))
                self.target_connection.execute(CreateSchema(self.tenant_info['target_schema_name']))
            else:
                raise

        self.target_metadata = generate_ed_metadata(schema_name=self.tenant_info['target_schema_name'],
                                                    bind=self.target_engine)
        self.target_metadata.create_all(self.target_engine)

        # get the udl db connection and engine objects
        self.udl2_conn, self.udl_engine = connect_db(udl2_conf['udl2_db']['db_driver'], udl2_conf['udl2_db']['db_user'],
                                                     udl2_conf['udl2_db']['db_pass'], udl2_conf['udl2_db']['db_host'],
                                                     udl2_conf['udl2_db']['db_port'], udl2_conf['udl2_db']['db_name'])

        # get the master_metadata table objects
        self.master_data_table = get_sqlalch_table_object(self.udl_engine, udl2_conf['udl2_db']['db_schema'],
                                                          udl2_conf['udl2_db']['master_metadata_table'])
        # insert tenant information into the master_metadata table
        self.udl2_conn.execute(self.master_data_table.insert(), [self.tenant_info])

        # other table objects that will be needed later
        self.get_table_objects()

        self.empty_int_tables()

    def tearDown(self):
        self.empty_int_tables()
        self.target_metadata.drop_all(self.target_engine)
        self.target_connection.execute(DropSchema(self.tenant_info['target_schema_name'], cascade=True))

        delete_cmd = self.master_data_table.delete().\
            where(self.master_data_table.c.tenant_code == self.tenant_info['tenant_code'])
        self.udl2_conn.execute(delete_cmd)
        self.udl2_conn.close()
        self.target_connection.close()
        self.target_engine.dispose()
        self.udl_engine.dispose()

    def get_table_objects(self):
        self.int_asmt_table = get_sqlalch_table_object(self.udl_engine, udl2_conf['udl2_db']['db_schema'],
                                                       'INT_SBAC_ASMT')
        self.int_asmt_outcome_table = get_sqlalch_table_object(self.udl_engine, udl2_conf['udl2_db']['db_schema'],
                                                               'INT_SBAC_ASMT_OUTCOME')
        self.target_dim_inst = get_sqlalch_table_object(self.target_engine, self.tenant_info['target_schema_name'],
                                                        'dim_inst_hier')
        self.target_fact = get_sqlalch_table_object(self.target_engine, self.tenant_info['target_schema_name'],
                                                    'fact_asmt_outcome')
        self.target_dim_student = get_sqlalch_table_object(self.target_engine, self.tenant_info['target_schema_name'],
                                                           'dim_student')
        self.target_dim_asmt = get_sqlalch_table_object(self.target_engine, self.tenant_info['target_schema_name'],
                                                        'dim_asmt')

    def empty_int_tables(self):
        self.udl2_conn.execute(self.int_asmt_table.delete())
        self.udl2_conn.execute(self.int_asmt_outcome_table.delete())

    ##
    # Test kickoff and tests
    ##
    def test_multi_tenant_target_database(self):
        self.check1_get_tenant_target_db_information_multi_tenant_on()
        self.check2_get_tenant_target_db_information_multi_tenant_off()
        self.check3_entire_load_to_star_stage_with_multi_tenancy()

    def check1_get_tenant_target_db_information_multi_tenant_on(self):
        udl2_conf['multi_tenant']['active'] = True

        expected = {
            mk.TARGET_DB_NAME: self.tenant_info['target_db_name'],
            mk.TARGET_DB_USER: self.tenant_info['target_schema_user_name'],
            mk.TARGET_DB_SCHEMA: self.tenant_info['target_schema_name'],
            mk.TARGET_DB_PASSWORD: self.tenant_info['target_schema_passwd']
        }
        result = get_tenant_target_db_information(self.tenant_info['tenant_code'])

        self.assertDictEqual(result, expected)

    def check2_get_tenant_target_db_information_multi_tenant_off(self):
        udl2_conf['multi_tenant']['active'] = False
        expected = {
            mk.TARGET_DB_NAME: udl2_conf['target_db_conn']['edware']['db_database'],
            mk.TARGET_DB_USER: udl2_conf['target_db_conn']['edware']['db_user'],
            mk.TARGET_DB_SCHEMA: udl2_conf['target_db_conn']['edware']['db_schema'],
            mk.TARGET_DB_PASSWORD: udl2_conf['target_db_conn']['edware']['db_pass']
        }
        result = get_tenant_target_db_information(self.tenant_info['tenant_code'])

        self.assertDictEqual(result, expected)

    def check3_entire_load_to_star_stage_with_multi_tenancy(self):
        udl2_conf['multi_tenant']['active'] = True
        self.verify_target_schema(True)
        self.read_csv_data_to_dict()
        msg = self.create_msg()
        explode_to_dims(msg)
        explode_to_fact(msg)
        self.verify_target_schema(False)

    ##
    # Helper methods
    ##
    def verify_target_schema(self, is_empty=False):
        counts = self.get_counts()
        if is_empty:
            self.assertEqual(counts, (0, 0, 0, 0))
        else:
            self.assertEqual(counts, (99, 1, 71, 94))
        return

    def get_counts(self):
        new_conn = self.target_engine.connect()
        print('*****')
        fact_select = select([func.count()]).select_from(self.target_fact)
        asmt_selct = select([func.count()]).select_from(self.target_dim_asmt)
        inst_select = select([func.count()]).select_from(self.target_dim_inst)
        stud_select = select([func.count()]).select_from(self.target_dim_student)

        fact_count = new_conn.execute(fact_select).fetchall()[0][0]
        asmt_count = new_conn.execute(asmt_selct).fetchall()[0][0]
        inst_count = new_conn.execute(inst_select).fetchall()[0][0]
        stud_count = new_conn.execute(stud_select).fetchall()[0][0]
        new_conn.close()

        return fact_count, asmt_count, inst_count, stud_count

    def read_csv_data_to_dict(self):
        asmt_outcome_dict_list = get_csv_dict_list(ASMT_OUTCOME_FILE)
        asmt_dict_list = get_csv_dict_list(ASMT_FILE)

        self.udl2_conn.execute(self.int_asmt_table.insert(), asmt_dict_list)
        self.udl2_conn.execute(self.int_asmt_outcome_table.insert(), asmt_outcome_dict_list)

    def create_msg(self):
        return {
            mk.BATCH_TABLE: udl2_conf['udl2_db']['batch_table'],
            mk.GUID_BATCH: BATCH_GUID,
            mk.LOAD_TYPE: 'assessment',
            mk.PHASE: 4,
            mk.TENANT_NAME: self.tenant_info['tenant_code'],
        }


def get_csv_dict_list(filename):
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
            clean_row = clean_dictionary_values(row)
            row_dict_list.append(clean_row)
    return row_dict_list


def clean_dictionary_values(val_dict):
    """
    Take a row dictionary and replace all empty strings with None value
    :param val_dict: The dictionary for the given row
    :return: A cleaned dictionary
    """
    for k, v in val_dict.items():
        if v == '':
            val_dict[k] = None

    return val_dict

if __name__ == '__main__':
    unittest.main()
