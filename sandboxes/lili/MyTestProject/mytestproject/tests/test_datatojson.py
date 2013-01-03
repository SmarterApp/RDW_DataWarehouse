import unittest
from mytestproject.datatojson.comparing_populations import comparing_populations_json
from mytestproject.tests.test_utils import make_data
class Test(unittest.TestCase):
        
    def testComparePopulationsQuery_district_teacher(self):        
        params = {"subject_code": ["ALL"], 
            'district_filter': ['ALL'], 
            'school_filter': ['ALL'], 
            'teacher_filter': ['ALL'], 
            'grades': ["ALL"], 
            'time_period': ["ALL"], 
            'year_range': ['ALL'], 
            "report_level":"district", 
            'segment_by': 'teacher',
            "school_group_type" : "Districts", 
            "grade_divider":"0"
         }
        
        values = [
                  (None, None, None, 63.0, None, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, None, None, 'ELA', 'BOY', '2012-2013', 'Smarter Balanced Assessment Consortium', 'Alabama', 'Above Benchmark', '3'),
                  (None, None, None, 65.0, None, 1, 2077, 'COPELAND, JOHN', 6405, 'School258', 625, 'ALSchoolGroup1', 143790, None, None, 'ELA', 'EOY', '2012-2013', 'Smarter Balanced Assessment Consortium', 'Alabama', 'Above Benchmark', '3')
                  ]
        
        rows = make_data(values)
        actual_data = comparing_populations_json.comparing_populations(params, rows)
        expected_data = {"scope_groups": [{"school_group": {"code": 625, "name": "ALSchoolGroup1"}, "school": None, "grade_groups": [{"bar_groups": [{"bars": [{"segments": [{"performance_level": {"code": "3", "name": "Above Benchmark"}, 
                         "score": 63, "student_count": 1, "student_percentage": 100}], "student_count": 1, "period": {"code": None, "name": "BOY"}, "year": {"code": None, "name": "2012-2013"}}, {"segments": [{"performance_level": {"code": "3", "name": "Above Benchmark"}, 
                         "score": 65, "student_count": 1, "student_percentage": 100}], "student_count": 1, "period": {"code": None, "name": "EOY"}, "year": {"code": None, "name": "2012-2013"}}], "student": None, "grade": None, 
                         "school_group": {"code": 625, "name": "ALSchoolGroup1"}, "school": {"code": 6405, "name": "School258"}, "teacher": {"code": 2077, "name": "COPELAND, JOHN"}}], "grade": None}], "teacher": None, "school_group_type": {"code": "Districts", "name": "Districts"}}]}
        self.assertTrue((actual_data) == (expected_data))
        