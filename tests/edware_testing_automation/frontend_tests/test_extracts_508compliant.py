# -*- coding: utf-8 -*-
"""
Created on December 5, 2013

@author: nparoha
"""
import csv
import fnmatch
import os
import shutil

import allure

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.utils.test_base import DOWNLOADS

INSIDE_DOWNLOADS_FOLDER = DOWNLOADS + '/'


@allure.story('Download reports')
class Extract508CompliantTable(ComparingPopulationsHelper, LosHelper):
    """
    Raw Data Extract Tests for Comparing Population 'School View' report
    """

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open web page after redirecting after logging in as a teacher"""
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")
        if os.path.exists(DOWNLOADS):
            try:
                shutil.rmtree(DOWNLOADS)
            except:
                raise AssertionError("Unable to delete the downloads directory.")

    @allure.feature('Smarter: Stave view')
    def test_508_state_level(self):
        os.system("mkdir " + DOWNLOADS)

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results', 'State Downloads'])
        self.select_extract_option(export_popup, 'Current view')

        filepath = INSIDE_DOWNLOADS_FOLDER + self.check_508_csv_present("cpop")
        actual_rows = self.csv_file_validation(filepath, 17)
        # Validate the report info headers avalable above the grid
        self.assertEqual(['Report Name', "Districts in North Carolina"], actual_rows[0],
                         "Report Name incorrectly displayed on 508 download.")
        self.assertEqual(['Report Info', 'North Carolina'], actual_rows[2],
                         "Report info incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Assessment Type', 'Summative'], actual_rows[5],
                         "Assessment Type incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Total Count', '5'], actual_rows[6],
                         "Total Count incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Academic year', '2015 - 2016'], actual_rows[7],
                         "Academic Year incorrectly displayed on 508 compliant download.")
        # Validate the grid data
        grid_headers = ['District Name', 'Mathematics Level 1 Count', 'Mathematics Level 1 Percentage',
                        'Mathematics Level 2 Count',
                        'Mathematics Level 2 Percentage', 'Mathematics Level 3 Count', 'Mathematics Level 3 Percentage',
                        'Mathematics Level 4 Count', 'Mathematics Level 4 Percentage', 'Mathematics Total Assessed',
                        'ELA/Literacy Level 1 Count', 'ELA/Literacy Level 1 Percentage', 'ELA/Literacy Level 2 Count',
                        'ELA/Literacy Level 2 Percentage', 'ELA/Literacy Level 3 Count',
                        'ELA/Literacy Level 3 Percentage',
                        'ELA/Literacy Level 4 Count', 'ELA/Literacy Level 4 Percentage', 'ELA/Literacy Total Assessed']
        self.assertEqual(grid_headers, actual_rows[10], "Grid Headers incorrectly displayed")
        grid_overall = ['NC State Overall', '10', '11%', '35', '39%', '32', '36%', '12', '14%', '89', '15', '20%', '31',
                        '40%', '18', '23%', '13', '17%', '77']
        self.assertEqual(grid_overall, actual_rows[11], "Grid Overall row data incorrectly displayed.")
        first_row = ['Daybreak School District', '0', '0%', '10', '72%', '2', '14%', '2', '14%', '14', '3', '21%', '4',
                     '29%', '3', '21%', '4', '29%', '14']
        self.assertEqual(first_row, actual_rows[12], "First row in the grid incorrectly displayed.")

    @allure.feature('Smarter: District view')
    def test_508_district_level(self):
        self.select_academic_year("2015")
        self.drill_down_navigation("2ce72d77-1de2-4137-a083-77935831b817", "ui-jqgrid-ftable")
        os.system("mkdir " + DOWNLOADS)

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.select_extract_option(export_popup, 'Current view')

        filepath = INSIDE_DOWNLOADS_FOLDER + self.check_508_csv_present("cpop")
        actual_rows = self.csv_file_validation(filepath, 16)
        # Validate the report info headers available above the grid
        self.assertEqual(['Report Name', "Schools in Dealfish Pademelon SD"], actual_rows[0],
                         "Report Name incorrectly displayed on 508 download.")
        self.assertEqual(['Report Info', 'North Carolina,Dealfish Pademelon SD'], actual_rows[2],
                         "Report info incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Assessment Type', 'Summative'], actual_rows[5],
                         "Assessment Type incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Total Count', '4'], actual_rows[6],
                         "Total Count incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Academic year', '2014 - 2015'], actual_rows[7],
                         "Academic Year incorrectly displayed on 508 compliant download.")

        ## Validate the grid data
        grid_headers = ['School Name', 'Mathematics Level 1 Count', 'Mathematics Level 1 Percentage',
                        'Mathematics Level 2 Count', 'Mathematics Level 2 Percentage', 'Mathematics Level 3 Count',
                        'Mathematics Level 3 Percentage', 'Mathematics Level 4 Count', 'Mathematics Level 4 Percentage',
                        'Mathematics Total Assessed', 'ELA/Literacy Level 1 Count', 'ELA/Literacy Level 1 Percentage',
                        'ELA/Literacy Level 2 Count', 'ELA/Literacy Level 2 Percentage', 'ELA/Literacy Level 3 Count',
                        'ELA/Literacy Level 3 Percentage', 'ELA/Literacy Level 4 Count',
                        'ELA/Literacy Level 4 Percentage', 'ELA/Literacy Total Assessed']
        self.assertEqual(grid_headers, actual_rows[10], "Grid Headers incorrectly displayed")
        grid_overall = ['Dealfish Pademelon SD District Overall', '7', '7%', '33', '34%', '42', '43%', '15', '16%',
                        '97', '6', '9%', '31', '47%', '29', '44%', '0', '0%', '66']
        self.assertEqual(grid_overall, actual_rows[11], "Grid overall row incorrectly displayed.")
        nyala_row = ['Nyala Aurochs High School', 'Interim Data Only', 'Interim Data Only', 'Interim Data Only',
                     'Interim Data Only', 'Interim Data Only', 'Interim Data Only', 'Interim Data Only',
                     'Interim Data Only', 'Interim Data Only', 'Interim Data Only', 'Interim Data Only',
                     'Interim Data Only', 'Interim Data Only', 'Interim Data Only', 'Interim Data Only',
                     'Interim Data Only', 'Interim Data Only', 'Interim Data Only']
        self.assertEqual(nyala_row, actual_rows[14], "Nyala row in the grid incorrectly displayed.")

    @allure.feature('Smarter: School view')
    def test_508_school_level_summative(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        os.system("mkdir " + DOWNLOADS)

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.select_extract_option(export_popup, 'Current view')

        filepath = INSIDE_DOWNLOADS_FOLDER + self.check_508_csv_present("cpop")
        actual_rows = self.csv_file_validation(filepath, 14)
        # Validate the report info headers avalable above the grid
        self.assertEqual(['Report Name', "Grades in Daybreak - Western Middle"], actual_rows[0],
                         "Report Name incorrectly displayed on 508 download.")
        self.assertEqual(['Report Info', 'North Carolina,Daybreak School District,Daybreak - Western Middle'],
                         actual_rows[2], "Report info incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Assessment Type', 'Summative'], actual_rows[5],
                         "Assessment Type incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Total Count', '2'], actual_rows[6],
                         "Total Count incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Academic year', '2015 - 2016'], actual_rows[7],
                         "Academic year incorrectly displayed on 508 compliant download.")

        # Validate the grid data
        grid_headers = ['Grade', 'Mathematics Level 1 Count', 'Mathematics Level 1 Percentage',
                        'Mathematics Level 2 Count', 'Mathematics Level 2 Percentage', 'Mathematics Level 3 Count',
                        'Mathematics Level 3 Percentage', 'Mathematics Level 4 Count', 'Mathematics Level 4 Percentage',
                        'Mathematics Total Assessed', 'ELA/Literacy Level 1 Count', 'ELA/Literacy Level 1 Percentage',
                        'ELA/Literacy Level 2 Count', 'ELA/Literacy Level 2 Percentage', 'ELA/Literacy Level 3 Count',
                        'ELA/Literacy Level 3 Percentage', 'ELA/Literacy Level 4 Count',
                        'ELA/Literacy Level 4 Percentage', 'ELA/Literacy Total Assessed']
        self.assertEqual(grid_headers, actual_rows[10], "Grid Headers incorrectly displayed")
        grid_overall = ['Daybreak - Western Middle School Overall', '0', '0%', '6', '67%', '2', '22%', '1', '11%', '9',
                        '1', '11%', '3', '33%', '2', '22%', '3', '34%', '9']
        self.assertEqual(grid_overall, actual_rows[11], "Grid overall row incorrectly displayed.")
        first_row = ['Grade 07', '0', '0%', '5', '71%', '2', '29%', '0', '0%', '7', '1', '12%', '3', '38%', '2', '25%',
                     '2', '25%', '8']
        self.assertEqual(first_row, actual_rows[12], "First row in the grid incorrectly displayed.")

    @allure.feature('Smarter: Grade view')
    def test_508_grade_level_math_summative(self):
        # Daybreak - Western Middle
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        self.select_los_view("Mathematics")
        os.system("mkdir " + DOWNLOADS)

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.select_extract_option(export_popup, 'Current view')

        filepath = INSIDE_DOWNLOADS_FOLDER + self.check_508_csv_present("los")
        actual_rows = self.csv_file_validation(filepath, 19)
        # Validate the report info headers avalable above the grid
        self.assertEqual(['Report Name', "Assessment Results for Grade 07"], actual_rows[0],
                         "Report Name incorrectly displayed on 508 download.")
        self.assertEqual(['Report Info', 'North Carolina,Daybreak School District,Daybreak - Western Middle,Grade 07'],
                         actual_rows[2], "Report info incorrectly displayed on 508 compliant download.")
        # self.assertEqual(['Assessment Type', '2012 · Grade 7 · Summative · Math Details'], actual_rows[5], "LOS view info incorrectly displayed.")
        self.assertEqual(['Total Count', '8'], actual_rows[6],
                         "Total Count incorrectly displayed on 508 compliant download.")
        self.assertEqual(['Academic year', '2015 - 2016'], actual_rows[7],
                         "Academic Year incorrectly displayed on 508 compliant download.")

        # Validate the grid data
        grid_headers = ['Students', 'Mathematics Overall', 'Mathematics Error Band', 'Mathematics Performance Level',
                        'Mathematics Performance Level Number', 'Status',
                        'Mathematics - Concepts & Procedures - Performance Level Number',
                        'Mathematics - Concepts & Procedures - Performance Level',
                        'Mathematics - Problem Solving and Modeling & Data Analysis - Performance Level Number',
                        'Mathematics - Problem Solving and Modeling & Data Analysis - Performance Level',
                        'Mathematics - Communicating Reasoning - Performance Level Number',
                        'Mathematics - Communicating Reasoning - Performance Level']
        first_row = ['Asbury, Theodore ', '1680', '1610-1750', 'Level 2', '2', '', '1', 'Below Standard', '1',
                     'Below Standard', '3', 'Above Standard']
        self.assertEqual(grid_headers, actual_rows[10], "Grid Headers incorrectly displayed")
        self.assertEqual(first_row, actual_rows[11], "First row in the grid incorrectly displayed.")

    def check_508_csv_present(self, report):
        """
        Check that the csv file is downloaded in the /tmp/downloads/ directory
        return file: Filename
        type file: string
        """
        found = False
        file_path = DOWNLOADS
        if report == "cpop":
            prefix = "comparing_populations"
        elif report == "los":
            prefix = "list_of_students"
        for file in os.listdir(file_path):
            is_part_file = fnmatch.fnmatch(file, '*.part')
            if fnmatch.fnmatch(file, '*.csv') or is_part_file:
                if prefix in file or is_part_file:
                    found = True
                    break
        self.assertTrue(found, "No CSV files found with the given prefix and suffix")
        return file

    def csv_file_validation(self, file, row_count):
        num_rows = len(list(csv.reader(open(file))))
        self.assertIsNotNone(num_rows, "Rawdata CSV file is Empty")
        self.assertEqual(num_rows, row_count, "Could not find expected number of rows in the CSV file.")
        all_rows = []
        with open(file) as f:
            each = csv.reader(f)
            for row in each:
                all_rows.append(row)
        return all_rows

    def tearDown(self):
        if os.path.exists(DOWNLOADS):
            try:
                # shutil.rmtree(DOWNLOADS)
                pass
            except:
                raise AssertionError("Unable to delete the downloads directory.")
