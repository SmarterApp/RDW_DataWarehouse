__author__ = 'npandey'

import unittest
from smarter.extracts.student_reg_statistics import get_headers


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
        self.assertEqual('AY1999 Count', headers[5])
        self.assertEqual('AY1999 Percent of Total', headers[6])
        self.assertEqual('AY2000 Count', headers[7])
        self.assertEqual('AY2000 Percent of Total', headers[8])
        self.assertEqual('Change in Count', headers[9])
        self.assertEqual('Percent Difference in Count', headers[10])
        self.assertEqual('Change in Percent of Total', headers[11])
        self.assertEqual('AY2000 Matched IDs to AY1999 Count', headers[12])
        self.assertEqual('AY2000 Matched IDs Percent of AY1999 Count', headers[13])
