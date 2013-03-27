'''
Created on Mar 21, 2013

@author: swimberly
'''

import os
import shutil
import unittest
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
        self.assertEqual(len(res), 4)
        for od in res:
            self.assertIsInstance(od, OrderedDict)
            self.assertIn('level', od)
            self.assertIn('name', od)
            self.assertIn('min_score', od)
            self.assertIn('max_score', od)
            self.assertIn('weight', od)

    def test_transform_to_metadata(self):
        id_list = trans.transform_to_metadata(self.dim_asmt_file, self.json_output_dir, self.file_pattern)
        self.assertIsInstance(id_list, list)
        self.assertEqual(len(id_list), 3)
        self.assertIn('111', id_list)
        self.assertIn('222', id_list)
        self.assertIn('333', id_list)
        file_names = [os.path.join(self.json_output_dir, self.file_pattern.format('111')),
                      os.path.join(self.json_output_dir, self.file_pattern.format('222')),
                      os.path.join(self.json_output_dir, self.file_pattern.format('333'))]

        for name in file_names:
            self.assertTrue(os.path.exists(name))

        with self.assertRaises(FileNotFoundError):
            trans.transform_to_metadata('asmt_filename', self.json_output_dir, self.file_pattern)

    def write_json_mock(self, ordered_data, filename):
        self.assertIn('overall', ordered_data)
        self.assertIn('identification', ordered_data)
        self.assertIn('claims', ordered_data)
        self.assertIn('performance_levels', ordered_data)
        self.assertIn('content', ordered_data)

        for key in ordered_data:
            self.assertIsNotNone(ordered_data[key])


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
    claims_dict = OrderedDict()
    claims_dict['level'] = [1, 2, 3, 4]
    claims_dict['name'] = "asmt_claim_{0}_name"
    claims_dict['min_score'] = "asmt_claim_{0}_score_min"
    claims_dict['max_score'] = "asmt_claim_{0}_score_max"
    claims_dict['weight'] = "asmt_claim_{0}_weight"
    return claims_dict


def create_claims_data():
    claims_data = {}

    for  i in range(1, 5):
        claims_data['asmt_claim_{0}_name'.format(i)] = 'name{0}'.format(i)
        claims_data['asmt_claim_{0}_score_min'.format(i)] = 10
        claims_data['asmt_claim_{0}_score_max'.format(i)] = 99
        claims_data['asmt_claim_{0}_weight'.format(i)] = 15

    return claims_data

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
