import csv
import os
from edudl2.udl2_util.database_util import execute_queries
from edudl2.move_to_target import move_to_target, move_to_target_setup
from edudl2.tests.functional_tests.util import UDLTestHelper


class IntToStarFTest(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(IntToStarFTest, cls).setUpClass()

    def test_load_int_to_star(self):
        table = 'INT_SBAC_ASMT'
        insert_sql = """INSERT INTO "{staging_schema}"."{staging_table}" VALUES({value_string});"""
        insert_array = []
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        with open(os.path.join(data_dir, 'INT_SBAC_ASMT.csv')) as f:
            cf = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            next(cf)
            for row in cf:
                values = '"' + '", "'.join(row) + '"'
                values = """'7', \'""" + """', '""".join(row) + """'"""
                values = values.replace('""', '"0"')
                values = values.replace("''", "'0'")
                values = values.replace("'DEFAULT'", "DEFAULT")
                insert_string = insert_sql.format(staging_schema=self.udl2_conf['udl2_db']['integration_schema'], staging_table=table, value_string=values)
                insert_array.append(insert_string)
            except_msg = "Unable to insert into %s" % table
            execute_queries(self.udl2_conn, insert_array, except_msg)
        table = 'INT_SBAC_ASMT_OUTCOME'
        insert_array = []
        with open(os.path.join(data_dir, 'INT_SBAC_ASMT_OUTCOME.csv')) as f:
            cf = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            next(cf)
            for row in cf:
                values = '"' + '", "'.join(row) + '"'
                values = """DEFAULT, \'""" + """', '""".join(row) + """'"""
                values = values.replace('""', '"0"')
                values = values.replace("''", "'0'")
                values = values.replace("'DEFAULT'", "DEFAULT")
                insert_string = insert_sql.format(staging_schema=self.udl2_conf['udl2_db']['integration_schema'], staging_table=table, value_string=values)
                insert_array.append(insert_string)
            except_msg = "Unable to insert into %s" % table
            execute_queries(self.udl2_conn, insert_array, except_msg)

        # explode to dim tables
        guid_batch = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'
        conf = move_to_target_setup.generate_conf(guid_batch, 4, 'Assessment', 'edware')
        table_map, column_map = move_to_target_setup.get_table_and_column_mapping(conf, 'dim_')
        for target in table_map.keys():
            target_columns = column_map[target]
            column_types = move_to_target.get_table_column_types(conf, target, list(target_columns.keys()))
            move_to_target.explode_data_to_dim_table(conf, table_map[target], target, target_columns, column_types)
        # explode to fact table
        table_map, column_map = move_to_target_setup.get_table_and_column_mapping(conf, 'fact_')
        column_types = move_to_target.get_table_column_types(conf, list(table_map.keys())[0], list(column_map['fact_asmt_outcome'].keys()))
        move_to_target.explode_data_to_fact_table(conf, list(table_map.values())[0], list(table_map.keys())[0], column_map['fact_asmt_outcome'], column_types)

        # check star schema table counts
        count_template = """ SELECT COUNT(*) FROM "{schema}"."{table}" """
        tables_to_check = {'dim_asmt': 1, 'dim_inst_hier': 71, 'dim_student': 94, 'fact_asmt_outcome': 99}
        for entry in tables_to_check.keys():
            sql = count_template.format(schema=self.udl2_conf['target_db']['db_schema'], table=entry)
            result = self.target_conn.execute(sql)
            count = 0
            for row in result:
                count = row[0]
            self.assertEqual(int(count), tables_to_check[entry])

        # check asmt score avgs
        int_asmt_avgs = self.get_integration_asmt_score_avgs()
        star_asmt_avgs = self.get_edware_asmt_score_avgs()

        assert int_asmt_avgs == star_asmt_avgs

        # check demographic counts
        int_demo_dict = self.get_integration_demographic_counts()
        star_demo_dict = self.get_star_schema_demographic_counts()

        assert int_demo_dict == star_demo_dict
