import unittest
from mytestproject.datatojson.comparing_populations import comparing_populations
from mytestproject.utils.test_utils import make_data

class Test(unittest.TestCase):
        
    def testDataToJson_district_teacher_gradeOff(self):      
        params = {
            'subject_code': ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            'report_level':'district', 
            'segment_by': 'teacher',
            'school_group_type' : 'Districts', 
            'grade_divider': 'false'
         }
        
        values = [
                  (None, None, None, 63.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, None, None, 'ELA', 'BOY', '2012-2013', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Above Benchmark'),
                  (None, None, None, 65.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, None, None, 'ELA', 'EOY', '2012-2013', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Above Benchmark')
                  ]
        
        rows = make_data(values)
        actual_data = comparing_populations(params, rows)
        expected_data = {'scope_groups': [
                                          {'school_group_type': {'name': 'Districts', 'code': '3'}, 
                                           'grade_groups': [
                                                            {'bar_groups': [
                                                                            {'bars': [
                                                                                      {'period': {'name': 'BOY', 'code': None}, 
                                                                                       'student_count': 1, 
                                                                                       'year': {'name': '2012-2013', 'code': None}, 
                                                                                       'segments': [
                                                                                                    {'score': 63, 
                                                                                                     'student_percentage': 100, 
                                                                                                     'student_count': 1, 
                                                                                                     'performance_level': {'name': 'Above Benchmark', 'code': 'Above Benchmark'}}
                                                                                                    ]
                                                                                       }, 
                                                                                      {'period': {'name': 'EOY', 'code': None}, 
                                                                                       'student_count': 1, 
                                                                                       'year': {'name': '2012-2013', 'code': None}, 
                                                                                       'segments': [
                                                                                                    {'score': 65, 
                                                                                                     'student_percentage': 100, 
                                                                                                     'student_count': 1, 
                                                                                                     'performance_level': {'name': 'Above Benchmark', 'code': 'Above Benchmark'}}
                                                                                                    ]
                                                                                       }
                                                                                      ],
                                                                             'state': {'name': 'Alabama', 'code': 'AL'}, 
                                                                             'teacher': {'name': 'COPELAND, JOHN', 'code': 2077}, 
                                                                             'state_group': {'name': 'Smarter Balanced Assessment Consortium', 'code': 'SBAC'}, 
                                                                             'student': None, 
                                                                             'school': {'name': 'School258', 'code': 6405}, 
                                                                             'grade': None, 
                                                                             'school_group': {'name': 'ALSchoolGroup1', 'code': 625}}], 
                                                             'grade': {'name': None, 'code': None}}], 
                                           'state': {'name': 'Alabama', 'code': 'AL'}, 
                                           'teacher': None, 
                                           'state_group': {'name': 'Smarter Balanced Assessment Consortium', 'code': 'SBAC'}, 
                                           'school': None, 'school_group': {'name': 'ALSchoolGroup1', 'code': 625}}]
                         }
        self.assertTrue((actual_data) == (expected_data))
        
    def testDataToJson_district_teacher_gradeOn(self):
        params = {
            'subject_code': ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            'report_level':'district', 
            'segment_by': 'teacher',
            'school_group_type' : 'Districts', 
            'grade_divider': 'true'
         }
        
        values = [
                  (None, None, None, 59.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, 1, 'Pre-K', 'ELA', 'EOY', '2013-2014', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Benchmark'),
                  (None, None, None, 61.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, 3, '1', 'ELA', 'MOY', '2013-2014', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Above Benchmark'),
                  (None, None, None, 60.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, 4, '2', 'MATH', 'MOY', '2012-2013', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Above Benchmark')
                 ]
        
        rows = make_data(values)
        actual_data = comparing_populations(params, rows)
        print(actual_data)
        expected_data = {'scope_groups': [
                                          {'state': {'code': 'AL', 'name': 'Alabama'}, 
                                           'school': None, 
                                           'school_group_type': {'code': '3', 'name': 'Districts'}, 
                                           'teacher': None, 
                                           'state_group': {'code': 'SBAC', 'name': 'Smarter Balanced Assessment Consortium'}, 
                                           'grade_groups': [
                                                            {'bar_groups': [
                                                                            {'state': {'code': 'AL', 'name': 'Alabama'}, 
                                                                             'school': {'code': 6405, 'name': 'School258'}, 
                                                                             'bars': [
                                                                                      {'period': {'code': None, 'name': 'EOY'}, 
                                                                                       'student_count': 1, 
                                                                                       'year': {'code': None, 'name': '2013-2014'}, 
                                                                                       'segments': [
                                                                                                    {'score': 59, 
                                                                                                     'student_percentage': 100, 
                                                                                                     'performance_level': {'code': 'Benchmark', 'name': 'Benchmark'}, 
                                                                                                     'student_count': 1}]
                                                                                       }], 
                                                                             'grade': None, 
                                                                             'student': None, 
                                                                             'teacher': {'code': 2077, 'name': 'COPELAND, JOHN'}, 
                                                                             'state_group': {'code': 'SBAC', 'name': 'Smarter Balanced Assessment Consortium'}, 
                                                                             'school_group': {'code': 625, 'name': 'ALSchoolGroup1'}}
                                                                            ], 
                                                             'grade': {'code': 1, 'name': 'Pre-K'}
                                                             }, 
                                                            {'bar_groups': [
                                                                            {'state': {'code': 'AL', 'name': 'Alabama'}, 
                                                                             'school': {'code': 6405, 'name': 'School258'}, 
                                                                             'bars': [
                                                                                      {'period': {'code': None, 'name': 'MOY'}, 
                                                                                       'student_count': 1, 
                                                                                       'year': {'code': None, 'name': '2013-2014'}, 
                                                                                       'segments': [
                                                                                                    {'score': 61, 
                                                                                                     'student_percentage': 100, 
                                                                                                     'performance_level': {'code': 'Above Benchmark', 'name': 'Above Benchmark'}, 
                                                                                                     'student_count': 1}]
                                                                                       }], 
                                                                             'grade': None, 
                                                                             'student': None, 
                                                                             'teacher': {'code': 2077, 'name': 'COPELAND, JOHN'}, 
                                                                             'state_group': {'code': 'SBAC', 'name': 'Smarter Balanced Assessment Consortium'}, 
                                                                             'school_group': {'code': 625, 'name': 'ALSchoolGroup1'}}
                                                                            ], 
                                                             'grade': {'code': 3, 'name': '1'}
                                                             }, 
                                                            {'bar_groups': [
                                                                            {'state': {'code': 'AL', 'name': 'Alabama'}, 
                                                                             'school': {'code': 6405, 'name': 'School258'}, 
                                                                             'bars': [
                                                                                      {'period': {'code': None, 'name': 'MOY'}, 
                                                                                       'student_count': 1, 
                                                                                       'year': {'code': None, 'name': '2012-2013'}, 
                                                                                       'segments': [
                                                                                                    {'score': 60, 
                                                                                                     'student_percentage': 100, 
                                                                                                     'performance_level': {'code': 'Above Benchmark', 'name': 'Above Benchmark'}, 
                                                                                                     'student_count': 1}]
                                                                                       }], 
                                                                             'grade': None, 
                                                                             'student': None, 
                                                                             'teacher': {'code': 2077, 'name': 'COPELAND, JOHN'}, 
                                                                             'state_group': {'code': 'SBAC', 'name': 'Smarter Balanced Assessment Consortium'}, 
                                                                             'school_group': {'code': 625, 'name': 'ALSchoolGroup1'}}
                                                                            ], 
                                                             'grade': {'code': 4, 'name': '2'}
                                                             }], 
                                           'school_group': {'code': 625, 'name': 'ALSchoolGroup1'}}
                                          ]
                         }
        self.assertTrue((actual_data) == (expected_data))
        
    def testDataToJson_invalid_params(self):
        param1 = {
            'subject_code': ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            'report_level':'invalid_report_level', 
            'segment_by': 'teacher',
            'school_group_type' : 'Districts', 
            'grade_divider': 'true'
         }
        param2 = {
            'subject_code': ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            'report_level':'district', 
            'segment_by': 'invalid_segment_by',
            'school_group_type' : 'Districts', 
            'grade_divider': 'true'
         }
        
        param3 = {
            'subject_code': ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            'report_level':'district', 
            'segment_by': 'teacher',
            'school_group_type' : 'invalid_school_group_type', 
            'grade_divider': 'true'
         }
        
        param4 = {
            'subject_code': ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            'report_level':'district', 
            'segment_by': 'teacher',
            'school_group_type' : 'Districts', 
            'grade_divider': 'invalid_grade_divider'
         }
        
        values = [
                  (None, None, None, 59.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, 1, 'Pre-K', 'ELA', 'EOY', '2013-2014', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Benchmark'),
                  (None, None, None, 61.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, 3, '1', 'ELA', 'MOY', '2013-2014', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Above Benchmark'),
                  (None, None, None, 60.0, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, 4, '2', 'MATH', 'MOY', '2012-2013', 'Smarter Balanced Assessment Consortium', 'SBAC', 'Alabama', 'AL', 'Above Benchmark')
                 ]
        
        rows = make_data(values)
        
        actual_data1 = comparing_populations(param1, rows)
        actual_data2 = comparing_populations(param2, rows)
        actual_data3 = comparing_populations(param3, rows)
        actual_data4 = comparing_populations(param4, rows)

        expected_data = "Input is wrong, please try it again"
        self.assertTrue((actual_data1) == (expected_data))
        self.assertTrue((actual_data2) == (expected_data))
        self.assertTrue((actual_data3) == (expected_data))
        self.assertTrue((actual_data4) == (expected_data))
