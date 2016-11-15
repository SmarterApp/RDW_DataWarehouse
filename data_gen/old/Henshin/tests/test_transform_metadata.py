'''
Created on Mar 21, 2013

@author: swimberly
'''

import os
import shutil
import unittest
import json
from collections import OrderedDict
import transform_metadata as trans


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Test(unittest.TestCase):

    def setUp(self):
        self.dim_asmt_file = os.path.join(__location__, 'files_for_tests', 'dim_asmt_for_test.csv')
        self.json_output_dir = os.path.join(__location__, 'files_for_tests', 'test_json')
        self.file_pattern = 'METADATA_ASMT_ID_{0}.json'
        self.header = []
        self.row = []

        if not os.path.isdir(self.json_output_dir):
            os.makedirs(self.json_output_dir)

        # header is a list of letters a to z
        # row is a list numbers 0 to 25
        for num in range(ord('a'), ord('z')):
            self.header.append(chr(num))
            self.row.append(num - ord('a'))

        self.claims_dict = create_claims_dict()
        self.claims_data = create_claims_data()
        self.mappings = create_mappings()
        self.data_dict = {'a_col': 'a_data', 'b_col': 'b_data', 'c_col': 'c_data',
                          'd_col': 'd_data', 'e_col': 'e_data', 'f_col': 'f_data',
                          'g_col': 'g_data'}

    def tearDown(self):
        if os.path.isdir(self.json_output_dir):
            shutil.rmtree(self.json_output_dir)

    def test_read_mapping_json(self):
        res = trans.read_mapping_json()
        self.assertIsNotNone(res)
        self.assertIsInstance(res, OrderedDict)

    def test_create_data_dict(self):
        res = trans.create_data_dict(self.header, self.row)
        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertEqual(len(self.header), len(res))
        for k, v in res.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, int)
            self.assertEqual(v, ord(k) - ord('a'))

    def test_create_list_for_section(self):
        res = trans.create_list_for_section(self.claims_dict, self.claims_data)
        self.assertEqual(len(res), 5)
        for values in res.values():
            self.assertIsInstance(values, OrderedDict)
            self.assertIn('name', values)
            self.assertIn('cut_point', values)

    def test_transform_to_metadata(self):
        id_list = trans.transform_to_metadata(self.dim_asmt_file, self.json_output_dir, self.file_pattern)
        self.assertIsInstance(id_list, list)
        self.assertEqual(len(id_list), 3)
        self.assertIn('11111111-1111-1111-1111-111111111111', id_list)
        self.assertIn('22222222-2222-2222-2222-222222222222', id_list)
        self.assertIn('33333333-3333-3333-3333-333333333333', id_list)
        file_names = [os.path.join(self.json_output_dir, self.file_pattern.format('11111111-1111-1111-1111-111111111111')),
                      os.path.join(self.json_output_dir, self.file_pattern.format('22222222-2222-2222-2222-222222222222')),
                      os.path.join(self.json_output_dir, self.file_pattern.format('33333333-3333-3333-3333-333333333333'))]

        for name in file_names:
            self.assertTrue(os.path.exists(name))
            self.verify_json_file(name)

        res = trans.transform_to_metadata('asmt_filename', self.json_output_dir, self.file_pattern)
        self.assertIsNone(res)

    def verify_json_file(self, filename):
        with open(filename, 'r') as f:
            data = json.loads(f.read(), object_pairs_hook=OrderedDict)
            expected_keys = create_mappings()
            for key in expected_keys:
                self.assertIsNotNone(data.get(key))
            for _k, val in data.items():
                self.assertIsNotNone(val)
                if isinstance(val, OrderedDict):
                    for _k, val1 in val.items():
                        self.assertIsNotNone(val1)
                else:
                    self.assertIsNotNone(val)


def create_mappings():
    mappings = OrderedDict({
        'overall': OrderedDict({'min': 'e_col', 'max': 'f_col'}),
        'identification': OrderedDict({'id': 'b_col', 'type': 'g_col'}),
        'performance_levels': OrderedDict(),
        'claims': OrderedDict(),
        'content': 'assessment',
        })
    mappings['performance_levels']['level'] = [1, 2, 3]
    mappings['performance_levels']['name'] = 'c_col'
    mappings['claims']['claim'] = [1, 2]
    mappings['claims']['name'] = 'd_col'
    return mappings


def create_claims_dict():
    claims_dict = OrderedDict([('level_1', OrderedDict([('name', 'asmt_perf_lvl_name_1'), ('cut_point', 'asmt_score_min')])),
                               ('level_2', OrderedDict([('name', 'asmt_perf_lvl_name_2'), ('cut_point', 'asmt_cut_point_1')])),
                               ('level_3', OrderedDict([('name', 'asmt_perf_lvl_name_3'), ('cut_point', 'asmt_cut_point_2')])),
                               ('level_4', OrderedDict([('name', 'asmt_perf_lvl_name_4'), ('cut_point', 'asmt_cut_point_3')])),
                               ('level_5', OrderedDict([('name', 'asmt_perf_lvl_name_5'), ('cut_point', 'asmt_cut_point_4')]))])
    return claims_dict


def create_claims_data():
    claims_data = {'asmt_custom_metadata': '',
                   'asmt_guid': 'f99396c2-7654-43eb-8ee0-f5c3bd95d361',
                   'asmt_rec_id': '1',
                   'asmt_period': '2012',
                   'asmt_period_year': '2012',
                   'asmt_type': 'SUMMATIVE',
                   'asmt_subject': 'Math',
                   'asmt_version': 'V1',
                   'asmt_claim_1_name': 'Concepts & Procedures',
                   'asmt_claim_2_name': 'Problem Solving and Modeling & Data Analysis',
                   'asmt_claim_3_name': 'Communicating Reasoning',
                   'asmt_claim_4_name': '',
                   'asmt_claim_1_score_weight': '0.4',
                   'asmt_claim_2_score_weight': '0.45',
                   'asmt_claim_3_score_weight': '0.15',
                   'asmt_claim_4_score_weight': '0',
                   'asmt_perf_lvl_name_1': 'Minimal Understanding',
                   'asmt_perf_lvl_name_2': 'Partial Understanding',
                   'asmt_perf_lvl_name_3': 'Adequate Understanding',
                   'asmt_perf_lvl_name_4': 'Thorough Understanding',
                   'asmt_perf_lvl_name_5': '',
                   'asmt_cut_point_1': '1400',
                   'asmt_cut_point_2': '1800',
                   'asmt_cut_point_3': '2100',
                   'asmt_cut_point_4': '',
                   'asmt_score_min': '1200',
                   'asmt_score_max': '2400',
                   'asmt_claim_1_score_min': '1200',
                   'asmt_claim_1_score_max': '2400',
                   'asmt_claim_2_score_min': '1200',
                   'asmt_claim_2_score_max': '2400',
                   'asmt_claim_3_score_min': '1200',
                   'asmt_claim_3_score_max': '2400',
                   'asmt_claim_4_score_min': '0',
                   'asmt_claim_4_score_max': '0',
                   'from_date': '20130705',
                   'to_date': '99991231',
                   'most_recent': 'TRUE',
}

    return claims_data

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
