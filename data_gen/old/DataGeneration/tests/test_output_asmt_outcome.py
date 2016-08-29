__author__ = 'swimberly'

import os
import csv
import shutil
import unittest
from datetime import date
from tempfile import mkdtemp

from DataGeneration.src.utils.idgen import IdGen
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
                        'guid_asmt_location': 'school.school_id',
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
                        'guid_district': 'school.district_id',
                        'name_district': 'school.district_name',
                        'guid_school': 'school.school_id',
                        'name_school': 'school.school_name',
                        'type_school': 'school.school_category',
                    }
                }
            },
            'test3': {
                'csv': {
                    'NON_REALDATA': {
                        'guid_district': 'school.district_id',
                        'name_district': 'school.district_name',
                        'claim_1_score': 'claim_scores.1.claim_score',
                        'claim_4_score': 'claim_scores.4.claim_score',
                        'asmt_score': 'asmt_scores.overall_score',
                    }
                }
            },
            'test_date': {
                'csv': {
                    'NON_REALDATA': {
                        'guid_district': 'school.district_id',
                        'name_district': 'school.district_name',
                        'date_taken_day': 'date_taken.day',
                        'date_taken': 'student_info.asmt_dates_taken',
                    }
                }
            },
            'test_error': {
                'csv': {
                    'ERROR': {
                        'status': 'C',
                        'custom': 'custom_val',
                    }
                }
            },
            'star_related': {
                'csv': {
                    'star': {
                        'batch_guid': 'batch_guid',
                        'rec_id': 'UNIQUE_ID',
                        'derived_demographic': 'student_info.derived_demographic',
                        'inst_hier_rec_id': 'inst_hierarchy.inst_hier_rec_id',
                    }
                }
            },
            'other': {
                'csv': {
                    'section': {
                        'section_rec_id': 'section.section_rec_id',
                        'section_guid': 'section.section_guid',
                        'section_name': 'section.section_name',
                        'grade': 'section.grade',
                    },
                    'inst_hier': {
                        'inst_hier_rec_id': 'inst_hierarchy.inst_hier_rec_id',
                        'state_name': 'inst_hierarchy.state_name',
                        'state_code': 'inst_hierarchy.state_code',
                    },
                    'assessment': {
                        'asmt_rec_id': 'assessment.asmt_rec_id',
                        'asmt_guid': 'assessment.asmt_guid',
                        'asmt_type': 'assessment.asmt_type',
                        'asmt_period': 'assessment.asmt_period',
                    }
                }
            }
        }
        self.idgen = IdGen()
        self.state_population = MakeTemp(state_name='North Carolina', state_code="NC")
        self.school1 = MakeTemp(school_id=123, school_name='school123', district_name='district1', district_id='d123',
                                school_category='elementary')
        self.student_info1 = MakeTemp(asmt_guids=1, student_id=2, first_name='bill', last_name='nye', middle_name='tom',
                                      address_1='1 bob st.', address_2='', city='North Carolina', zip_code=12345, gender='m',
                                      email='b.n@email.com', dob='11111999', grade=4,
                                      asmt_dates_taken={'math': date.today(), 'ela': date(2011, 2, 5)},
                                      asmt_scores={'math': MakeTemp(overall_score=1900,
                                                                    claim_scores=[MakeTemp(claim_score=1201), MakeTemp(claim_score=1202),
                                                                                  MakeTemp(claim_score=1203), MakeTemp(claim_score=1204)]),
                                                'ela': MakeTemp(overall_score=1800,
                                                                claim_scores=[MakeTemp(claim_score=1301), MakeTemp(claim_score=1302),
                                                                              MakeTemp(claim_score=1303)])},
                                      asmt_subjects={'math': 'Math', 'ela': 'ELA'})
        self.section = MakeTemp(section_rec_id=123, section_guid='sg123', section_name='section1', grade=4)
        self.inst_hier = MakeTemp(inst_hier_rec_id=456, state_name='Georgia', state_code="GA")
        self.assessment = MakeTemp(asmt_rec_id=789, asmt_guid="gu789", asmt_type='interim', asmt_period='fall')

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test_initialize_csv_file_value_returned(self):
        output_path = self.output_dir
        output_keys = ['test']

        result = initialize_csv_file(self.conf_dict, output_path, output_keys)
        expected = {
            'REALDATA': os.path.join(self.output_dir, 'REALDATA.csv'),
            'dim_test': os.path.join(self.output_dir, 'dim_test.csv'),
        }

        self.assertDictEqual(result, expected)

    def test_initialize_csv_file_value_returned_2(self):
        output_path = self.output_dir
        output_keys = ['test2']

        result = initialize_csv_file(self.conf_dict, output_path, output_keys)
        expected = {
            'NON_REALDATA': os.path.join(self.output_dir, 'NON_REALDATA.csv'),
        }

        self.assertDictEqual(result, expected)

    def test_initialize_csv_file_check_files_output(self):
        output_path = self.output_dir
        output_keys = ['test']

        initialize_csv_file(self.conf_dict, output_path, output_keys)

        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'REALDATA.csv')))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'dim_test.csv')))

    def test_initialize_csv_file_check_files_output_content(self):
        output_path = self.output_dir
        output_keys = ['test']

        initialize_csv_file(self.conf_dict, output_path, output_keys)

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
        data_object = MakeTemp(time='good morning', fun='fun')
        attr_name = 'time'
        subject = 'Math'

        result = get_value_from_object(data_object, attr_name, subject, 'math')
        self.assertEqual(result, 'good morning')

    def test_get_value_from_object_subject_dict(self):
        data_object = MakeTemp(time={'Math': 'good morning', 'ELA': 'good night'}, fun='fun')
        attr_name = 'time'
        subject = 'ELA'

        result = get_value_from_object(data_object, attr_name, subject, "ELA")
        self.assertEqual(result, 'good night')

    def test_get_value_from_object_time(self):
        some_date = date(2014, 11, 8)
        data_object = MakeTemp(time={'Math': 'good morning', 'ELA': 'good night'}, fun=some_date)
        attr_name = 'fun'
        subject = 'ELA'

        result = get_value_from_object(data_object, attr_name, subject, "ELA")
        self.assertEqual(result, '20141108')

    def test_create_output_csv_dict(self):
        table_conf_dict = self.conf_dict['test']['csv']['REALDATA']

        expected = {
            'guid_asmt': 1,
            'guid_asmt_location': 123,
            'name_asmt_location': 'school123',
            'grade_asmt': 4,
            'name_state': 'North Carolina',
            'code_state': 'NC',
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'math', None, None, None, None, None)
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_2(self):
        table_conf_dict = self.conf_dict['test3']['csv']['NON_REALDATA']

        expected = {
            'guid_district': 'd123',
            'name_district': 'district1',
            'claim_1_score': 1201,
            'claim_4_score': 1204,
            'asmt_score': 1900,
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'math', None, None, None, None, None)
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_3(self):
        table_conf_dict = self.conf_dict['test3']['csv']['NON_REALDATA']

        expected = {
            'guid_district': 'd123',
            'name_district': 'district1',
            'claim_1_score': 1301,
            'claim_4_score': None,
            'asmt_score': 1800,
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'ela', None, None, None, None, None)
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_4(self):
        table_conf_dict = self.conf_dict['test_date']['csv']['NON_REALDATA']

        expected = {
            'guid_district': 'd123',
            'name_district': 'district1',
            'date_taken_day': 5,
            'date_taken': '20110205',
        }
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'ela', None, None, None, None, None)
        self.assertDictEqual(expected, res)

    def test_create_output_csv_dict_undefined_object_listed(self):
        table_conf_dict = self.conf_dict['test_error']['csv']['ERROR']

        expected = {
            'status': 'C',
            'custom': 'custom_val',
        }

        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'ela', None, None, None, None, None)
        self.assertDictEqual(res, expected)

    def test_create_output_csv_dict_star_related(self):
        table_conf_dict = self.conf_dict['star_related']['csv']['star']

        self.idgen.next_id = 30
        inst_hier = MakeTemp(inst_hier_rec_id=34)
        #self.student_info1.get_stu_demo_list = lambda: [True, False, False, False, False, False]
        self.student_info1.derived_demographic = lambda: 1
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'ela', inst_hier, 'gu123', None, None, None)

        expected = {
            'batch_guid': 'gu123',
            'rec_id': 30,
            'derived_demographic': 1,
            'inst_hier_rec_id': 34,
        }
        self.assertDictEqual(res, expected)

    def test_create_output_csv_dict_star_related_2(self):
        table_conf_dict = self.conf_dict['star_related']['csv']['star']

        self.idgen.next_id = 100
        table_conf_dict['rec_id'] = 'idgen.get_id'
        inst_hier = MakeTemp(inst_hier_rec_id=34)
        #self.student_info1.get_stu_demo_list = lambda: [True, False, False, False, False, False]
        self.student_info1.derived_demographic = lambda: 1
        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1,
                                     self.student_info1, 'ela', inst_hier, 'gu123', None, None, None)

        expected = {
            'batch_guid': 'gu123',
            'rec_id': 100,
            'derived_demographic': 1,
            'inst_hier_rec_id': 34,
        }
        self.assertDictEqual(res, expected)

    def test_create_output_csv_dict_no_student_info_available__assessment(self):
        table_conf_dict = self.conf_dict['other']['csv']['assessment']

        res = create_output_csv_dict(table_conf_dict, None, None, None, None, None, None, None, self.assessment, None)

        expected = {
            'asmt_rec_id': 789,
            'asmt_guid': "gu789",
            'asmt_type': 'interim',
            'asmt_period': 'fall',
        }

        self.assertDictEqual(res, expected)

    def test_create_output_csv_dict_no_student_info_available__inst_hier(self):
        table_conf_dict = self.conf_dict['other']['csv']['inst_hier']

        res = create_output_csv_dict(table_conf_dict, None, None, None, None, self.inst_hier, None, None, None, None)

        expected = {
            'inst_hier_rec_id': 456,
            'state_name': 'Georgia',
            'state_code': 'GA',
        }

        self.assertDictEqual(res, expected)

    def test_create_output_csv_dict_no_student_info_available__section(self):
        table_conf_dict = self.conf_dict['other']['csv']['section']

        res = create_output_csv_dict(table_conf_dict, self.state_population, self.school1, self.student_info1,
                                     'math', self.inst_hier, 'gu123', self.section, self.assessment, None)

        expected = {
            'section_rec_id': 123,
            'section_guid': 'sg123',
            'section_name': 'section1',
            'grade': 4,
        }

        self.assertDictEqual(res, expected)

    def test_output_data_row_counts(self):
        output_keys = ['test', 'test2']
        output_files = initialize_csv_file(self.conf_dict, self.output_dir, output_keys)

        output_data(self.conf_dict, output_files, output_keys, self.school1, self.student_info1, self.state_population)

        self.assertEqual(len(output_files), 3)

        for file in output_files:
            count = 0
            with open(output_files[file], 'r') as fp:
                for _ in csv.reader(fp):
                    count += 1
            self.assertEqual(count, 3, 'header + 1 row for each subject')

    def test_output_data_content(self):
        output_keys = ['test', 'test2']
        output_files = initialize_csv_file(self.conf_dict, self.output_dir, output_keys)

        output_data(self.conf_dict, output_files, output_keys, self.school1, self.student_info1, self.state_population)

        expected = {
            'REALDATA': {
                'guid_asmt': '1',
                'guid_asmt_location': '123',
                'name_asmt_location': 'school123',
                'grade_asmt': '4',
                'name_state': 'North Carolina',
                'code_state': 'NC',
            },
            'dim_test': {
                'address_student_line1': '1 bob st.',
                'address_student_line2': '',
                'address_student_city': 'North Carolina',
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

    def test_output_data_content_2(self):
        output_keys = ['other']
        output_files = initialize_csv_file(self.conf_dict, self.output_dir, output_keys)

        output_data(self.conf_dict, output_files, output_keys, section=self.section)

        expected = {
            'section': {
                'section_rec_id': '123',
                'section_guid': 'sg123',
                'section_name': 'section1',
                'grade': '4',
            }
        }

        for file in output_files:
            with open(output_files[file], 'r') as fp:
                for c_dict in csv.DictReader(fp):
                    self.assertDictEqual(c_dict, expected[file])

    def test_output_data_content_3(self):
        output_keys = ['other']
        output_files = initialize_csv_file(self.conf_dict, self.output_dir, output_keys)

        output_data(self.conf_dict, output_files, output_keys, section=self.section, assessment=self.assessment)

        expected = {
            'section': {
                'section_rec_id': '123',
                'section_guid': 'sg123',
                'section_name': 'section1',
                'grade': '4',
            },
            'assessment': {
                'asmt_rec_id': '789',
                'asmt_guid': 'gu789',
                'asmt_type': 'interim',
                'asmt_period': 'fall',
            }
        }

        for file in output_files:
            with open(output_files[file], 'r') as fp:
                for c_dict in csv.DictReader(fp):
                    self.assertDictEqual(c_dict, expected[file])


class MakeTemp(object):
    def __init__(self, **kwargs):
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])


if __name__ == '__main__':
    unittest.main()
