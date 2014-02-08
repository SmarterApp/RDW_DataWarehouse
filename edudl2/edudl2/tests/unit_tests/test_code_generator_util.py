'''
Created on June 17th, 2013

@author: lichen
'''

import edudl2.rule_maker.rules.code_generator_util as cu
import edudl2.rule_maker.rules.code_generator_sql_template as sql_tpl
from edudl2.rule_maker.rules.rule_keys import UPPER, REMNL, TRIM, TO_CHAR, MIN0


import unittest


class TestCodeGeneratorUtil(unittest.TestCase):

    def setUp(self):
        self.code_version = sql_tpl.POSTGRES

    def test_lower(self):
        col_name = 'test_col_1'
        actual_result = cu.lower(self.code_version, col_name)
        expected_result = 'LOWER(test_col_1)'
        self.assertEqual(actual_result, expected_result)

    def test_upper(self):
        col_name = 'test_col_2'
        actual_result = cu.upper(self.code_version, col_name)
        expected_result = 'UPPER(test_col_2)'
        self.assertEqual(actual_result, expected_result)

    def test_remnl(self):
        col_name = 'test_col_3'
        actual_result = cu.remnl(self.code_version, col_name)
        expected_result = 'REGEXP_REPLACE(test_col_3, E\'[\\n\\r]+\', \'\', \'g\')'
        self.assertEqual(actual_result, expected_result)

    def test_trim(self):
        col_name = 'test_col_4'
        actual_result = cu.trim(self.code_version, col_name)
        expected_result = 'TRIM(test_col_4)'
        self.assertEqual(actual_result, expected_result)

    def test_vclean_list(self):
        col_name = 'test_col_5'
        action_list = [UPPER, REMNL, TRIM]
        actual_result = cu.vclean(self.code_version, col_name, action_list)
        expected_result = 't_test_col_5 := TRIM(REGEXP_REPLACE(UPPER(v_test_col_5), E\'[\\n\\r]+\', \'\', \'g\'));'
        self.assertEqual(actual_result, expected_result)

    def test_vclean_single(self):
        col_name = 'test_col_6'
        action_list = UPPER
        actual_result = cu.vclean(self.code_version, col_name, action_list)
        expected_result = 't_test_col_6 := UPPER(v_test_col_6);'
        self.assertEqual(actual_result, expected_result)

    def test_pclean_list(self):
        col_name = 'test_col_7'
        action_list = [REMNL, TRIM, UPPER]
        actual_result = cu.pclean(self.code_version, col_name, action_list)
        expected_result = 'v_test_col_7 := UPPER(TRIM(REGEXP_REPLACE(p_test_col_7, E\'[\\n\\r]+\', \'\', \'g\')));'
        self.assertEqual(actual_result, expected_result)

    def test_pclean_single(self):
        col_name = 'test_col_8'
        action_list = TRIM
        actual_result = cu.pclean(self.code_version, col_name, action_list)
        expected_result = 'v_test_col_8 := TRIM(p_test_col_8);'
        self.assertEqual(actual_result, expected_result)

    def test_rclean_list(self):
        col_name = 'test_col_11'
        action_list = [TO_CHAR, MIN0]
        actual_result = cu.rclean(self.code_version, col_name, action_list)
        expected_result = """v_result := CAST (v_result AS TEXT);
        IF v_result ~ '^[0-9]+$' AND
            CAST(v_result AS BIGINT) < 0 THEN
            v_result := '0';
        END IF;
"""
        self.assertEqual(actual_result, expected_result)

    def test_rclean_single(self):
        col_name = 'test_col_12'
        action_list = MIN0
        actual_result = cu.rclean(self.code_version, col_name, action_list)
        expected_result = """
        IF v_result ~ '^[0-9]+$' AND
            CAST(v_result AS BIGINT) < 0 THEN
            v_result := '0';
        END IF;
"""
        self.assertEqual(actual_result, expected_result)

    def test_lookup(self):
        col_name = 'test_col_10'
        action_list = {'High School': ['HS', 'HIGH SCHOOL'],
                       'Middle School': ['MS', 'MIDDLE SCHOOL'],
                       'Elementary School': ['ES' 'ELEMENTARY SCHOOL']}
        actual_result = cu.lookup(self.code_version, col_name, action_list)
        actual_result_update = actual_result.replace('\t', '    ')
        expected_result = EXPECTED_RESULT_FOR_LOOKUP
        self.assertEqual(actual_result_update, expected_result)

    def test_inlist(self):
        col_name = 'test_col_9'
        inlist = ['Staff', 'Teacher']
        actual_result = cu.inlist(self.code_version, col_name, inlist)
        expected_result = EXPECTED_RESULT_FOR_INLIST
        self.assertEqual(actual_result, expected_result)

    def test_assignment(self):
        left_exp = 'a'
        right_exp = 'b'
        actual_result = cu.assignment(left_exp, right_exp)
        expected_result = 'a := b;'
        self.assertEqual(actual_result, expected_result)

    def test_fun_name(self):
        parts = ['sp_', 'func1']
        actual_result = cu.fun_name(tuple(parts))
        expected_result = 'sp_func1'
        self.assertEqual(actual_result, expected_result)

# expected result
EXPECTED_RESULT_FOR_LOOKUP = """
    IF    SUBSTRING(t_test_col_10, 1, 19) = 'ESELEMENTARY SCHOOL' THEN
        v_result := 'Elementary School';
    ELSIF SUBSTRING(t_test_col_10, 1, 2) = 'HS'
    OR    SUBSTRING(t_test_col_10, 1, 11) = 'HIGH SCHOOL' THEN
        v_result := 'High School';
    ELSIF SUBSTRING(t_test_col_10, 1, 2) = 'MS'
    OR    SUBSTRING(t_test_col_10, 1, 13) = 'MIDDLE SCHOOL' THEN
        v_result := 'Middle School';"""

EXPECTED_RESULT_FOR_INLIST = """v_result := 'NOT FOUND';

    FOR cntr IN array_lower(vals_test_col_9, 1)..array_upper(vals_test_col_9, 1)
    LOOP
        IF SUBSTRING(t_test_col_9, 1, CHAR_LENGTH(vals_test_col_9[cntr])) = vals_test_col_9[cntr] THEN
            v_result := vals_test_col_9[cntr];
            EXIT;
        END IF;
    END LOOP;
"""

if __name__ == "__main__":
    unittest.main()
