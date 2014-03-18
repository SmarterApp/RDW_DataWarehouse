__author__ = 'tshewchuk'

"""
Module containing Student Registration report generator unit tests.
"""

import unittest

from edextract.student_reg_report_generation.student_reg_report_generator import (generate_sr_statistics_report_data,
                                                                                  generate_sr_completion_report_data)


class TestStudentRegReportGenerator(unittest.TestCase):

    def test_generate_sr_statistics_report_data_no_data(self):
        header, data = generate_sr_statistics_report_data('NJ', 2014)
        self.assertEqual(header, ('State', 'District', 'School', 'Category', 'Value', '2013 Count', '2013 Percent of Total',
                                  '2014 Count', '2014 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                  'Change in Percent of Total','2014 Matched IDs to 2013 Count', '2014 Matched IDs Percent of 2013 count'))
        self.assertEquals(data, [])

    def test_generate_sr_completion_report_data_no_data(self):
        header, data = generate_sr_completion_report_data('NJ', 2014)
        self.assertEquals(data, [])
        self.assertEqual(header, ('State', 'District', 'School', 'Grade', 'Category', 'Value', 'Assessment Subject',
                                  'Assessment Type', 'Assessment Date', 'Academic Year', 'Count of Students Registered',
                                  'Count of Students Assessed', 'Percent of Students Assessed'))
