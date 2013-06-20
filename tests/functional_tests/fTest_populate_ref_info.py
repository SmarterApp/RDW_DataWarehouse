'''
Created on Jun 19, 2013

@author: swimberly
'''

import unittest
import os
import imp
from importlib import import_module

from sqlalchemy.sql.expression import select

from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.database_util import connect_db, get_sqlalch_table_object
from udl2.populate_ref_info import populate_stored_proc


class PopulateRefInfoFTest(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE

        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        #udl2_conf = import_module(udl2_conf, 'udl2_conf')

        self.user = udl2_conf['udl2_db']['db_user']
        self.password = udl2_conf['udl2_db']['db_pass']
        self.host = udl2_conf['udl2_db']['db_host']
        self.db_name = udl2_conf['udl2_db']['db_database']
        self.ref_schema = udl2_conf['udl2_db']['reference_schema']
        self.ref_table_name = udl2_conf['udl2_db']['ref_table_name']
        db_driver = udl2_conf['udl2_db']['db_driver']
        port = udl2_conf['udl2_db']['db_port']

        # Testable Rules
        # TODO: once all rules are implemented this should just read the rules dict
        self.testable_rules = ['clean', 'cleanUpper', 'cleanLower', 'schoolType', 'yn',
                               'gender', 'staffType', 'asmtType', 'subjectType']

        # connect to db
        conn, engine = connect_db(db_driver, self.user, self.password, self.host, port, self.db_name)
        self.conn = conn
        self.engine = engine
        self.ref_table = get_sqlalch_table_object(self.engine, self.ref_schema, self.ref_table_name)

    def tearDown(self):
        pass

    def test_rules_populate(self):

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
        proc_map_list = populate_stored_proc(self.engine, self.conn, self.ref_schema, self.ref_table_name)
        proc_map = dict(proc_map_list)

        select_cols = [self.ref_table.c.transformation_rule, self.ref_table.c.stored_proc_name, self.ref_table.c.stored_proc_created_date]
        select_stmt = select(select_cols).where(self.ref_table.c.phase == -1)

        results = self.conn.execute(select_stmt)

        for res in results:
            self.assertEqual(res[1], proc_map[res[0]], 'Each row should have matching stored_proc and rule name')
            self.assertIsNotNone(res[2], 'Stored proc created date should not be null')

        # Clean up
        # TODO: If more test added created generic method for cleanup in tearDown
        self.conn.execute(self.ref_table.delete().where(self.ref_table.c.phase == -999))
