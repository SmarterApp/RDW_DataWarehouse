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

import unittest
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import os
from edudl2.rule_maker.rules.udl_transformation_config import transform_rules
from edudl2.rule_maker.rules import transformation_code_generator
from sqlalchemy.exc import ProgrammingError
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.database.udl2_connector import initialize_db_udl, get_udl_connection


class RuleGeneratorFTest(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        udl2_conf = conf_tup[0]
        initialize_db_udl(udl2_conf)
        self.rule_names = transform_rules.keys()
        self.rule_conf = transform_rules
        self.rule_list = transformation_code_generator.generate_transformations(self.rule_names, rule_conf=self.rule_conf)

        with get_udl_connection() as conn:
            trans = conn.get_transaction()
            for rule in self.rule_list:
                try:
                    conn.execute(rule[2])
                except ProgrammingError as e:
                    raise AssertionError('UNABLE TO CREATE FUNCTION: %s, Error: "%s"' % (rule[0], e))
                    trans.rollback()
            trans.commit()

    def test_rule_with_inlist_outlist(self):
        for rule in self.rule_list:
            rule_def = self.rule_conf[rule[0]]
            if 'inlist' in rule_def and 'outlist' in rule_def:
                with get_udl_connection() as conn:
                    for (input_val, output_val) in zip(rule_def['inlist'], rule_def['outlist']):
                        result = conn.execute("SELECT %s('%s')" % (rule[1], input_val))
                        self.assertEqual(result.fetchone()[0], output_val)

    def test_rule_with_inlist_compare_length(self):
        for rule in self.rule_list:
            rule_def = self.rule_conf[rule[0]]
            if 'inlist' in rule_def and 'outlist' not in rule_def and 'compare_length' in rule_def:
                with get_udl_connection() as conn:
                    for input_val in rule_def['inlist']:
                        test_val = input_val[:int(rule_def['compare_length'])]
                        test_val += 'asdf'
                        result = conn.execute("SELECT %s('%s')" % (rule[1], input_val))
                        self.assertEqual(result.fetchone()[0], input_val)

    def test_rule_with_lookup(self):
        for rule in self.rule_list:
            rule_def = self.rule_conf[rule[0]]
            if 'lookup' in rule_def.keys():
                with get_udl_connection() as conn:
                    for lookup_val in rule_def['lookup'].keys():
                        for possible_val in rule_def['lookup'][lookup_val]:
                            if possible_val is None:
                                result = conn.execute("SELECT %s(NULL)" % (rule[1]))
                            else:
                                result = conn.execute("SELECT %s('%s')" % (rule[1], possible_val))
                        self.assertEqual(result.fetchone()[0], lookup_val)

    def test_cleanup_rules(self):
        clean_rules = [('sp_clean', 'this \nshould be cleaned. ', 'this should be cleaned.'),
                       ('sp_cleanUpper', 'this \nshould be cleaned. ', 'THIS SHOULD BE CLEANED.'),
                       ('sp_cleanLower', 'ThIs \nShouLd Be cLeaNed. ', 'this should be cleaned.')]

        for each in clean_rules:
            with get_udl_connection() as conn:
                result = conn.execute("SELECT %s('%s')" % (each[0], each[1]))
                temp = result.fetchone()[0]
                self.assertEqual(temp, each[2])

    def test_rule_definitions(self):
        for each in self.rule_conf:
            if 'INLIST' in each:
                self.assertTrue('OUTLIST' in each or 'COMPARE_LENGTH' in each)
