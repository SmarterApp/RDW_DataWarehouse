__author__ = 'swimberly'

import os
import csv
import shutil
import unittest
from datetime import date
from tempfile import mkdtemp

from DataGeneration.src.writers.output_asmt_outcome import (initialize_csv_file, get_header_from_file, write_csv_rows,
                                                            get_value_from_object, create_output_csv_dict, output_data)


class TestOutputAssessmentOutcome(unittest.TestCase):

    def setUp(self):
        self.output_dir = mkdtemp()
        self.conf_dict = {
            'test': {
                'csv': {
                    'REALDATA': {
                        'guid_asmt': 'student_info.asmt_guids',
                        'guid_asmt_location': 'school.school_guid',
                        'name_asmt_location': 'school.school_name',
                        'grade_asmt': 'student_info.grade',
                        'name_state': 'state_population.state_name',
                        'code_state': 'state_population.state_code',
                    },
                    'dim_test': {
                        'address_student_line1': 'student_info.address_1',
                        'address_student_line2': 'student_info.address_2',
                        'address_student_city': 'student_info.city',
                        'address_student_zip': 'student_info.zip_code',
                        'gender_student': 'student_info.gender',
                    }
                }
            },
            'test2': {
                'csv': {
                    'NON_REALDATA': {
                        'guid_district': 'school.district_guid',
                        'name_district': 'school.district_name',
                        'guid_school': 'school.school_guid',
                        'name_school': 'school.school_name',
                        'type_school': 'school.school_category',
                    }
                }
            },
            'test3': {
                'csv': {
                    'NON_REALDATA': {
                        'guid_district': 'school.district_guid',
                        'name_district': 'school.district_name',
                        'claim_1_score': 'claim_scores.1.claim_score',
                        'asmt_score': 'asmt_scores.overall_score',
                    }
                }
            },
            'test_error': {
                'csv': {
                    'ERROR': {
                        'guid_district': 'school_error.district_guid',
                        'name_district': 'school_error.district_name',
                    }
                }
            }
        }

        self.state_population = Dummy(state_name='New York', state_code="NY")
        self.school1 = Dummy(school_guid=123, school_name='school123', district_name='district1', district_guid='d123',
                             school_category='elementary')
        self.student_info1 = Dummy(asmt_guids=1, student_guid=2, first_name='bill', last_name='nye', middle_name='tom',
                                   address_1='1 bob st.', address_2='', city='new york', zip_code=12345, gender='m',
                                   email='b.n@email.com', dob='11111999', grade=4, asmt_dates_taken=date.today(),
                                   asmt_scores={'math': Dummy(overall_score=1900,
                                                              claim_scores=[Dummy(claim_score=1201), Dummy(claim_score=1202),
                                                                            Dummy(claim_score=1203), Dummy(claim_score=1204)]),
                                                'ela': Dummy(overall_score=1800,
                                                             claim_scores=[Dummy(claim_score=1301), Dummy(claim_score=1302),
                                                                           Dummy(claim_score=1303)])})

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test_initialize_csv_file_value_returned(self):
        output_path = self.output_dir
        output_keys = ['test']

        result = initialize_csv_file(self.conf_dict, output_keys, output_path)
        expected = {
            'REALDATA': os.path.join(self.output_dir, 'REALDATA.csv'),
            'dim_test': os.path.join(self.output_dir, 'dim_test.csv'),
        }

        self.assertDictEqual(result, expected)

    def test_initialize_csv_file_value_returned_2(self):
        output_path = self.output_dir
        output_keys = ['test2']

        result = initialize_csv_file(self.conf_dict, output_keys, output_path)
        expected = {
            'NON_REALDATA': os.path.join(self.output_dir, 'NON_REALDATA.csv'),
        }

        self.assertDictEqual(result, expected)

    def test_initialize_csv_file_check_files_output(self):
        output_path = self.output_dir
        output_keys = ['test']

        initialize_csv_file(self.conf_dict, output_keys, output_path)

        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'REALDATA.csv')))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'dim_test.csv')))

    def test_initialize_csv_file_check_files_output_content(self):
        output_path = self.output_dir
        output_keys = ['test']

        initialize_csv_file(self.conf_dict, output_keys, output_path)

        with open(os.path.join(self.output_dir, 'REALDATA.csv'), 'r') as fp:
            reader = csv.reader(fp)
            header = next(reader)
            expected_header = self.conf_dict['test']['csv']['REALDATA'].keys()
            self.assertEqual(len(header), len(expected_header))
            self.assertSetEqual(set(header), set(expected_header))

        with open(os.path.join(self.output_dir, 'dim_test.csv'), 'r') as fp:
            reader = csv.reader(fp)
            header = next(reader)
            expected_header = self.conf_dict['test']['csv']['dim_test'].keys()
            self.assertEqual(len(header), len(expected_header))
            self.assertSetEqual(set(header), set(expected_header))

    def test_get_header_from_file(self):
        output_path = self.output_dir

        with open(os.path.join(output_path, 'test_csv.csv'), 'w') as fp:
            fp.write('v1,v2,v3,v4,v5\n')

        result = get_header_from_file(os.path.join(self.output_dir, 'test_csv.csv'))
        self.assertListEqual(result, ['v1', 'v2', 'v3', 'v4', 'v5'])

    def test_write_csv_rows(self):
        output_path = os.path.join(self.output_dir, 'test_csv.csv')
        with open(output_path, 'w') as fp:
            fp.write('v1,v2,v3,v4,v5\n')

        row_dict_list = [{'v1': 'tom', 'v2': 'bob', 'v3': 'tim', 'v4': 'sam', 'v5': 'jim'},
                         {'v1': 'tommy', 'v2': 'bobby', 'v3': 'timmy', 'v4': 'sammy', 'v5': 'jimmy'}]

        write_csv_rows(output_path, row_dict_list)
        result = []
        with open(output_path, 'r') as fp:
            c_reader = csv.DictReader(fp)
            for row in c_reader:
                result.append(row)

        self.assertListEqual(row_dict_list, result)

    def test_get_value_from_object(self):
        data_object = Dummy(time='good morning', fun='fun')
        attr_name = 'time'
        subject = 'Math'

        result = get_value_from_object(data_object, attr_name, subject)
        self.assertEqual(result, 'good morning')

    def test_get_value_from_object_subject_dict(self):
        data_object = Dummy(time={'Math': 'good morning', 'ELA': 'good night'}, fun='fun')
        attr_name = 'time'
        subject = 'ELA'

        result = get_value_from_object(data_object, attr_name, subject)
        self.assertEqual(result, 'good night')

    def test_get_value_from_object_time(self):
        some_date = date(2014, 11, 8)
        data_object = Dummy(time={'Math': 'good morning', 'ELA': 'good night'}, fun=some_date)
        attr_name = 'fun'
        subject = 'ELA'

        result = get_value_from_object(data_object, attr_name, subject)
        self.assertEqual(result, '20141108')

    def test_create_output_csv_dict(self):
        table_conf_dict = self.conf_dict['test']['csv']['REALDATA']

        expected = {
            'guid_asmt': 1,
            'guid_asmt_location': 123,
            'name_asmt_location': 'school123',
            'grade_asmt': 4,
            'name_state': 'New York',
            'code_state': 'NY',
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1, self.student_info1, 'math')
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_2(self):
        table_conf_dict = self.conf_dict['test3']['csv']['NON_REALDATA']

        expected = {
            'guid_district': 'd123',
            'name_district': 'district1',
            'claim_1_score': 1201,
            'asmt_score': 1900,
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1, self.student_info1, 'math')
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_3(self):
        table_conf_dict = self.conf_dict['test3']['csv']['NON_REALDATA']

        expected = {
            'guid_district': 'd123',
            'name_district': 'district1',
            'claim_1_score': 1301,
            'asmt_score': 1800,
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1, self.student_info1, 'ela')
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_error(self):
        table_conf_dict = self.conf_dict['test_error']['csv']['ERROR']

        with self.assertRaises(NotImplementedError):
            create_output_csv_dict(table_conf_dict, self.state_population, self.school1, self.student_info1, 'ela')

    def test_output_data_row_counts(self):
        output_keys = ['test', 'test2']
        output_files = initialize_csv_file(self.conf_dict, output_keys, self.output_dir)

        output_data(self.conf_dict, output_keys, output_files, self.state_population, self.school1, self.student_info1)

        self.assertEqual(len(output_files), 3)

        for file in output_files:
            count = 0
            with open(output_files[file], 'r') as fp:
                for _ in csv.reader(fp):
                    count += 1
            self.assertEqual(count, 3, 'header + 1 row for each subject')

    def test_output_data_content(self):
        output_keys = ['test', 'test2']
        output_files = initialize_csv_file(self.conf_dict, output_keys, self.output_dir)

        output_data(self.conf_dict, output_keys, output_files, self.state_population, self.school1, self.student_info1)

        expected = {
            'REALDATA': {
                'guid_asmt': '1',
                'guid_asmt_location': '123',
                'name_asmt_location': 'school123',
                'grade_asmt': '4',
                'name_state': 'New York',
                'code_state': 'NY',
            },
            'dim_test': {
                'address_student_line1': '1 bob st.',
                'address_student_line2': '',
                'address_student_city': 'new york',
                'address_student_zip': '12345',
                'gender_student': 'm',
            },
            'NON_REALDATA': {
                'guid_district': 'd123',
                'name_district': 'district1',
                'guid_school': '123',
                'name_school': 'school123',
                'type_school': 'elementary',
            }
        }

        for file in output_files:
            with open(output_files[file], 'r') as fp:
                for c_dict in csv.DictReader(fp):
                    self.assertDictEqual(c_dict, expected[file])


class Dummy(object):
    def __init__(self, **kwargs):
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])


if __name__ == '__main__':
    unittest.main()
