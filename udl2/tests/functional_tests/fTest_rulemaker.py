import unittest
import csv
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2 import database
import imp
import os
from rule_maker.rules.udl_transformation_config import transform_rules
from rule_maker.rules import transformation_code_generator
from sqlalchemy import func
from udl2_util.database_util import create_sqlalch_session
from sqlalchemy.exc import ProgrammingError
from udl2_util.config_reader import read_ini_file


class RuleGeneratorFTest(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        udl2_conf = conf_tup[0]
        self.conn, self.engine = database._create_conn_engine(udl2_conf['udl2_db'])
        self.rule_names = transform_rules.keys()
        self.rule_conf = transform_rules
        self.rule_list = transformation_code_generator.generate_transformations(self.rule_names, rule_conf=self.rule_conf)

        session = create_sqlalch_session(self.engine)

        for rule in self.rule_list:
            try:
                session.execute(rule[2])
            except ProgrammingError as e:
                raise AssertionError('UNABLE TO CREATE FUNCTION: %s, Error: "%s"' % (rule[0], e))

        session.commit()

    def tearDown(self):
        self.conn.close()

    def test_rule_with_inlist_outlist(self):
        for rule in self.rule_list:
            rule_def = self.rule_conf[rule[0]]
            if 'inlist' in rule_def and 'outlist' in rule_def:
                for (input_val, output_val) in zip(rule_def['inlist'], rule_def['outlist']):
                    result = self.engine.execute("SELECT %s('%s')" % (rule[1], input_val))
                    assert result.fetchone()[0] == output_val

    def test_rule_with_inlist_compare_length(self):
        for rule in self.rule_list:
            rule_def = self.rule_conf[rule[0]]
            if 'inlist' in rule_def and 'outlist' not in rule_def and 'compare_length' in rule_def:
                for input_val in rule_def['inlist']:
                    test_val = input_val[:int(rule_def['compare_length'])]
                    test_val += 'asdf'
                    result = self.engine.execute("SELECT %s('%s')" % (rule[1], input_val))
                    assert result.fetchone()[0] == input_val

    def test_rule_with_lookup(self):
        for rule in self.rule_list:
            rule_def = self.rule_conf[rule[0]]
            if 'lookup' in rule_def.keys():
                print('FOUND A RULE WITHLOOKUP')
                for lookup_val in rule_def['lookup'].keys():
                    for possible_val in rule_def['lookup'][lookup_val]:
                        result = self.engine.execute("SELECT %s('%s')" % (rule[1], possible_val))
                        assert result.fetchone()[0] == lookup_val

    def test_cleanup_rules(self):
        clean_rules = [('sp_clean', 'this \nshould be cleaned. ', 'this should be cleaned.'),
                       ('sp_cleanUpper', 'this \nshould be cleaned. ', 'THIS SHOULD BE CLEANED.'),
                       ('sp_cleanLower', 'ThIs \nShouLd Be cLeaNed. ', 'this should be cleaned.')]

        for each in clean_rules:
            result = self.engine.execute("SELECT %s('%s')" % (each[0], each[1]))
            temp = result.fetchone()[0]
            assert temp == each[2]

    def test_rule_definitions(self):
        for each in self.rule_conf:
            if 'INLIST' in each:
                assert 'OUTLIST' in each or 'COMPARE_LENGTH' in each
