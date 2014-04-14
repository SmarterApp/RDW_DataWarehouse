import csv
import os
from edudl2.move_to_target import move_to_target, move_to_target_setup
from edudl2.tests.functional_tests.util import UDLTestHelper
from sqlalchemy.sql.expression import text, bindparam, select
from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
from unittest import skip
from edudl2.database.udl2_connector import get_udl_connection,\
    get_target_connection, get_prod_connection
from sqlalchemy.sql.functions import count


class MatchAndDeleteFTest(UDLTestHelper):

    matched_prod_values = None
    guid_batch = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'
    tenant_code = 'edware'

    @classmethod
    def setUpClass(cls):
        super(MatchAndDeleteFTest, cls).setUpClass()
        cls.create_schema_for_target(cls.tenant_code, cls.guid_batch)

    @classmethod
    def tearDownClass(cls):
        super(MatchAndDeleteFTest, cls).tearDownClass()
        cls.drop_target_schema(cls.tenant_code, cls.guid_batch)

    def setUp(self):
        super(MatchAndDeleteFTest, self).setUp()
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.phase_number = 4
        self.load_type = 'assessment'
        self.conf = move_to_target_setup.generate_conf(self.guid_batch, self.phase_number,
                                                       self.load_type, MatchAndDeleteFTest.tenant_code,
                                                       target_schema=MatchAndDeleteFTest.guid_batch)
        self.load_to_dim_task_name = "udl2.W_load_from_integration_to_star.explode_data_to_dim_table_task"
        self.load_to_fact_task_name = "udl2.W_load_from_integration_to_star.explode_data_to_fact"
        self.dim_table_prefix = 'dim_'
        self.fact_table_prefix = 'fact_'
        self.insert_sql = 'INSERT INTO "{staging_schema}"."{staging_table}" ({columns_string}) VALUES ({value_string});'

    def tearDown(self):
        pass

    def generate_insert_items(self, header, row):
        row = [r if str(r) != '' else '0' for r in row]
        columns_values = dict(zip(header, row))
        columns = [k for k, v in columns_values.items()]
        values = [":{k}".format(k=k) for k, v in columns_values.items()]
        params = [bindparam(k, v) for k, v in columns_values.items()]
        return (columns, values, params)

    def load_int_sbac_asmt(self):
        table = 'int_sbac_asmt'
        with open(os.path.join(self.data_dir, 'INT_SBAC_ASMT_DELETE.csv')) as f, get_udl_connection() as conn:
            cf = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            header = next(cf)
            header.insert(0, 'record_sid')
            for row in cf:
                # set record_sid = 7 in this func test
                row.insert(0, str(7))
                (columns, values, params) = self.generate_insert_items(header, row)
                insert_query = text(self.insert_sql.format(staging_schema=self.udl2_conf['udl2_db']['db_schema'],
                                                           staging_table=table,
                                                           columns_string=", ".join(columns),
                                                           value_string=", ".join(values)),
                                    bindparams=params)
                conn.execute(insert_query)

    def load_int_sbac_asmt_outcome(self):
        table = 'int_sbac_asmt_outcome'
        with open(os.path.join(self.data_dir, 'INT_SBAC_ASMT_OUTCOME_DELETE.csv')) as f, get_udl_connection() as conn:
            cf = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            header = next(cf)
            for row in cf:
                (columns, values, params) = self.generate_insert_items(header, row)
                insert_query = text(self.insert_sql.format(staging_schema=self.udl2_conf['udl2_db']['db_schema'],
                                                           staging_table=table,
                                                           columns_string=", ".join(columns),
                                                           value_string=", ".join(values)),
                                    bindparams=params)
                conn.execute(insert_query)

    def load_int_to_star(self):
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

    def count_rows(self, status=None):
        with get_target_connection(MatchAndDeleteFTest.tenant_code, MatchAndDeleteFTest.guid_batch) as conn:
            fact = conn.get_table('fact_asmt_outcome')
            query = select([count(fact.c.asmnt_outcome_rec_id).label('count')], from_obj=fact)
            if status:
                query = query.where(fact.c.rec_status == status)
            result = conn.get_result(query)
            return int(result[0]['count'])

    def test_get_records_for_deletion(self):
        self.load_int_to_star()
        self.assertEqual(4, self.count_rows())
        with get_target_connection(MatchAndDeleteFTest.tenant_code, MatchAndDeleteFTest.guid_batch) as target_conn:
            records_to_be_deleted = move_to_target.get_records_marked_for_deletion(self.conf, target_conn, 'fact_asmt_outcome')
            self.assertEqual(4, len(records_to_be_deleted))

    def test_match_all_records_to_be_deleted_with_prod(self):
        with get_target_connection(MatchAndDeleteFTest.tenant_code, MatchAndDeleteFTest.guid_batch) as target_conn, get_prod_connection() as prod_conn:
            records_to_be_deleted = move_to_target.get_records_marked_for_deletion(self.conf, target_conn, 'fact_asmt_outcome')
            proxy_rows = move_to_target.yield_records_to_be_deleted(prod_conn, 'fact_asmt_outcome', records_to_be_deleted, batch_size=10)
            result = []
            for rows in proxy_rows:
                result.extend(rows)
            # the below count should be 4 but there are multiple (3)
            # 'C' records in the SDS for student '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
            # when SDS is fixed, this count should be asserted for 4
            self.assertEqual(6, len(result))

    def test_update_pre_prod_for_records_to_be_deleted(self):
        with get_target_connection(MatchAndDeleteFTest.tenant_code, MatchAndDeleteFTest.guid_batch) as target_conn, get_prod_connection() as prod_conn:
            records_to_be_deleted = move_to_target.get_records_marked_for_deletion(self.conf, target_conn, 'fact_asmt_outcome')
            proxy_rows = move_to_target.yield_records_to_be_deleted(prod_conn, 'fact_asmt_outcome', records_to_be_deleted, batch_size=10)
            for rows in proxy_rows:
                move_to_target.update_rec_id_for_records_to_delete(self.conf, target_conn, 'fact_asmt_outcome', rows)
            mismatches = move_to_target.get_records_marked_for_deletion(self.conf, target_conn, 'fact_asmt_outcome')
            self.assertEqual(0, len(mismatches))

    def test_check_mismatched_deletions(self):
        with get_target_connection(self.tenant_code, self.guid_batch) as conn:
            self.assertRaises(DeleteRecordNotFound, move_to_target.check_mismatched_deletions(self.conf, conn, 'fact_asmt_outcome'))
