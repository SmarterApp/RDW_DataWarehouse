__author__ = 'npandey'

import unittest
from smarter.extracts.student_reg_completion import get_headers


class TestStudentRegCompletion(unittest.TestCase):

    def test_get_headers(self):
        academic_year = 2000

        headers = get_headers(academic_year)
        self.assertEqual(14, len(headers))
        self.assertEqual('State', headers[0])
        self.assertEqual('District', headers[1])
        self.assertEqual('School', headers[2])
        self.assertEqual('Category', headers[3])
        self.assertEqual('Value', headers[4])
        self.assertEqual('AY2000 Count of Registered Students', headers[5])
        self.assertEqual('AY2000 Count of Students Assessed by Summative Math', headers[6])
        self.assertEqual('AY2000 Percent of Registered Students Assessed by Summative Math', headers[7])
        self.assertEqual('AY2000 Count of Students Assessed by Summative ELA', headers[8])
        self.assertEqual('AY2000 Percent of Registered Students Assessed by Summative ELA', headers[9])
        self.assertEqual('AY2000 Count of Students Assessed by Interim Comprehensive Math', headers[10])
        self.assertEqual('AY2000 Percent of Registered Students Assessed by Interim Comprehensive Math', headers[11])
        self.assertEqual('AY2000 Count of Students Assessed by Interim Comprehensive ELA', headers[12])
        self.assertEqual('AY2000 Percent of Registered Students Assessed by Interim Comprehensive ELA', headers[13])
