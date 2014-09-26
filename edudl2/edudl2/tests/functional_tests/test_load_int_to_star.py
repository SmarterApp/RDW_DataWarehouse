import csv
import os
from edudl2.move_to_target import move_to_target, move_to_target_setup
from edudl2.tests.functional_tests.util import UDLTestHelper
from sqlalchemy.sql.expression import text, bindparam, select
from edudl2.database.udl2_connector import get_udl_connection,\
    get_target_connection
from sqlalchemy.sql.functions import count


class IntToStarFTest(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(IntToStarFTest, cls).setUpClass()

    def setUp(self):
        super(IntToStarFTest, self).setUp()
        self.guid_batch = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'
        self.phase_number = 4
        self.load_type = 'assessment'
        self.tenant_code = 'cat'
        self.conf = move_to_target_setup.generate_conf(self.guid_batch, self.phase_number,
                                                       self.load_type, self.tenant_code, target_schema=self.guid_batch)
        self.load_to_dim_task_name = "udl2.W_load_from_integration_to_star.explode_data_to_dim_table_task"
        self.load_to_fact_task_name = "udl2.W_load_from_integration_to_star.explode_data_to_facts"
        self.dim_table_prefix = 'dim_'
        self.fact_table_prefix = 'fact_'
        self.insert_sql = 'INSERT INTO "{staging_schema}"."{staging_table}" ({columns_string}) VALUES ({value_string});'
        self.create_schema_for_target(self.tenant_code, self.guid_batch)

    def tearDown(self):
        super(IntToStarFTest, self).tearDown()
        self.drop_target_schema(self.tenant_code, self.guid_batch)

    def generate_insert_items(self, header, row):
        row = [r if str(r) != '' else '0' for r in row]
        columns_values = dict(zip(header, row))
        columns = [k for k, v in columns_values.items()]
        values = [":{k}".format(k=k) for k, v in columns_values.items()]
        params = [bindparam(k, v) for k, v in columns_values.items()]
        return (columns, values, params)

    def load_int_sbac_asmt(self):
        table = 'int_sbac_asmt'
        with open(os.path.join(self.data_dir, 'INT_SBAC_ASMT.csv')) as f, get_udl_connection() as conn:
            cf = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            header = next(cf)
            header.insert(0, 'record_sid')
            for row in cf:
                # set record_sid = 7 in this func test
                row.insert(0, str(7))
                (columns, values, params) = self.generate_insert_items(header, row)
                insert_query = text(self.insert_sql.format(staging_schema=self.udl2_conf['udl2_db_conn']['db_schema'],
                                                           staging_table=table,
                                                           columns_string=", ".join(columns),
                                                           value_string=", ".join(values)),
                                    bindparams=params)
                conn.execute(insert_query)

    def load_int_sbac_asmt_outcome(self):
        table = 'int_sbac_asmt_outcome'
        with open(os.path.join(self.data_dir, 'INT_SBAC_ASMT_OUTCOME.csv')) as f, get_udl_connection() as conn:
            cf = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            header = next(cf)
            for row in cf:
                (columns, values, params) = self.generate_insert_items(header, row)
                insert_query = text(self.insert_sql.format(staging_schema=self.udl2_conf['udl2_db_conn']['db_schema'],
                                                           staging_table=table,
                                                           columns_string=", ".join(columns),
                                                           value_string=", ".join(values)),
                                    bindparams=params)
                conn.execute(insert_query)

    def test_1_load_int_to_star(self):
        self.load_int_sbac_asmt()
        self.load_int_sbac_asmt_outcome()

        # explode to dim tables

        table_map, column_map = move_to_target_setup.get_table_and_column_mapping(self.conf,
                                                                                  self.load_to_dim_task_name,
                                                                                  self.dim_table_prefix)
        for target in table_map.keys():
            target_columns = column_map[target]
            column_types = move_to_target_setup.get_table_column_types(self.conf, target, list(target_columns.keys()))
            move_to_target.explode_data_to_dim_table(self.conf, table_map[target], target, target_columns, column_types)

        # explode to fact table
        table_map, column_map = move_to_target_setup.get_table_and_column_mapping(self.conf,
                                                                                  self.load_to_fact_task_name,
                                                                                  self.fact_table_prefix)

        for fact_table, source_table in table_map.items():
            column_types = move_to_target_setup.get_table_column_types(self.conf,
                                                                       fact_table,
                                                                       list(column_map[fact_table].keys()))
            move_to_target.explode_data_to_fact_table(self.conf,
                                                      source_table,
                                                      fact_table,
                                                      column_map[fact_table],
                                                      column_types)

        # handle deletion case
        move_to_target.handle_updates_and_deletes(self.conf)

        # check star schema table counts
        with get_target_connection(self.tenant_code, self.guid_batch) as conn:
            tables_to_check = {'dim_asmt': 1, 'dim_inst_hier': 99, 'dim_student': 94, 'fact_asmt_outcome_vw': 71}
            for entry in tables_to_check.keys():
                table = conn.get_table(entry)
                query = select([count()], from_obj=table)
                result = conn.execute(query)
                #self.assertEqual(int(result.fetchall()[0][0]), tables_to_check[entry])

        # check asmt score avgs
        int_asmt_avgs = self.get_integration_asmt_score_avgs()
        star_asmt_avgs = self.get_edware_asmt_score_avgs(self.tenant_code, self.guid_batch)

        self.assertEqual(int_asmt_avgs, star_asmt_avgs)

        # check demographic counts
        int_demo_dict = self.get_integration_demographic_counts()
        star_demo_dict = self.get_star_schema_demographic_counts(self.tenant_code, self.guid_batch)

        self.assertEqual(int_demo_dict, star_demo_dict)
