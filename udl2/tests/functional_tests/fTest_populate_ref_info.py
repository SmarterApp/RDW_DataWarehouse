'''
Created on Jun 19, 2013

@author: swimberly
'''

import unittest
import os

from sqlalchemy.sql.expression import select
from udl2 import database
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.database_util import connect_db, get_sqlalch_table_object
from udl2.populate_ref_info import populate_stored_proc
from rule_maker.rules.udl_transformation_config import transform_rules
from rule_maker.rules import transformation_code_generator
from udl2_util.config_reader import read_ini_file


class PopulateRefInfoFTest(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE

        conf_tup = read_ini_file(config_path)
        udl2_conf = conf_tup[0]
        self.conn, self.engine = database._create_conn_engine(udl2_conf['udl2_db'])
        self.ref_schema = udl2_conf['udl2_db']['reference_schema']
        self.ref_table_name = udl2_conf['udl2_db']['ref_table_name']
        self.ref_table = get_sqlalch_table_object(self.engine, self.ref_schema, self.ref_table_name)

        # Testable Rules
        self.rule_names = transform_rules.keys()
        self.rule_conf = transform_rules
        self.rule_list = transformation_code_generator.generate_transformations(self.rule_names, rule_conf=self.rule_conf)
        self.testable_rules = []
        for rule in self.rule_list:
            self.testable_rules.append(rule[0])

        test_rows = []
        for rule in self.testable_rules:
            ins_dict = {
                'phase': -999,
                'source_table': 'ftest_table',
                'source_column': 'ftest_column',
                'target_table': 'ftest_table1',
                'target_column': 'ftest_column1',
                'transformation_rule': rule,
            }
            test_rows.append(ins_dict)
        self.conn.execute(self.ref_table.insert(), test_rows)

    def tearDown(self):
        self.conn.execute(self.ref_table.delete().where(self.ref_table.c.phase == -999))
        self.conn.close()

    def test_stored_procedures_exist_in_db(self):

        populate_stored_proc(self.engine, self.conn, self.ref_schema, self.ref_table_name)

        for rule in self.testable_rules:
            stored_proc_query = "SELECT proname FROM pg_proc WHERE proname = 'sp_{0}';".format(rule.lower())
            res = self.conn.execute(stored_proc_query).fetchall()[0][0]
            expected = 'sp_{0}'.format(rule)
            self.assertEqual(res.lower(), expected.lower())

    def test_rules_populate(self):

        proc_map_list = populate_stored_proc(self.engine, self.conn, self.ref_schema, self.ref_table_name)
        proc_map = dict(proc_map_list)

        select_cols = [self.ref_table.c.transformation_rule, self.ref_table.c.stored_proc_name, self.ref_table.c.stored_proc_created_date]
        select_stmt = select(select_cols).where(self.ref_table.c.phase == -999)

        results = self.conn.execute(select_stmt)

        for res in results:
            self.assertEqual(res[1], proc_map[res[0]], 'Each row should have matching stored_proc and rule name')
            self.assertIsNotNone(res[2], 'Stored proc created date should not be null')
