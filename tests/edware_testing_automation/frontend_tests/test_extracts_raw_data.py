# -*- coding: UTF-8 -*-
'''
Created on December 5, 2013

@author: nparoha
'''
import csv
import fnmatch
import json
import os
import shutil
import time
import zipfile

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.utils.test_base import DOWNLOADS, UNZIPPED

UNZIPPED_FILES = UNZIPPED + '/'
DOWNLOAD_FILES = DOWNLOADS + '/'


# @unittest.skip("skipping this test temporarily.")
class RawDataExtract(ComparingPopulationsHelper, LosHelper, ApiHelper, ExtractsHelper):
    '''
    Raw Data Extract Tests for Comparing Population 'School View' report
    '''

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)
        ApiHelper.__init__(self, *args, **kwargs)
        ExtractsHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open web page after redirecting after logging in as a teacher'''

    def setUp(self):
        self.driver = self.get_driver()
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")
        if os.path.exists(UNZIPPED_FILES):
            shutil.rmtree(UNZIPPED_FILES)
        os.makedirs(UNZIPPED_FILES)
        if not os.path.exists(DOWNLOAD_FILES):
            os.makedirs(DOWNLOAD_FILES)
        self.files_to_cleanup_at_end = []

    def tearDown(self):
        self.driver.quit()
        if os.path.exists(UNZIPPED_FILES):
            shutil.rmtree(UNZIPPED_FILES)
        if os.path.exists(DOWNLOAD_FILES):
            shutil.rmtree(DOWNLOAD_FILES)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    def test_extract_raw_data_cpop_school(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.check_default_academic_year("2015 - 2016")

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.select_extract_option(export_popup, 'Student assessment results')

        file_name = None
        for file in os.listdir(DOWNLOAD_FILES):
            if file.endswith(".zip"):
                file_name = file
        filepath = DOWNLOAD_FILES + file_name
        self.files_to_cleanup_at_end.append(filepath)
        self.unzip_file_to_directory(filepath, UNZIPPED_FILES)
        filenames = self.get_file_names(UNZIPPED_FILES)
        csv_filenames = filenames[0]
        json_filenames = filenames[1]

        grade7_ela = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_07_ELA_SUMMATIVE')
        grade7_math = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_07_MATH_SUMMATIVE')
        grade8_ela = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_08_ELA_SUMMATIVE')
        grade8_math = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_08_MATH_SUMMATIVE')

        metadata_json_gr7_ela = self.check_file_exists(json_filenames,
                                                       'METADATA_ASMT_2016_NC_GRADE_07_ELA_SUMMATIVE_3b10d26b-b013-4cdd-a916-5d577e895ed4')
        metadata_json_gr7_math = self.check_file_exists(json_filenames,
                                                        'METADATA_ASMT_2016_NC_GRADE_07_MATH_SUMMATIVE_7d10d26b-b013-4cdd-a916-5d577e895cff')
        metadata_json_gr8_ela = self.check_file_exists(json_filenames,
                                                       'METADATA_ASMT_2016_NC_GRADE_08_ELA_SUMMATIVE_3b10d26b-b013-4cdd-a916-5d577e895ed4')
        metadata_json_gr8_math = self.check_file_exists(json_filenames,
                                                        'METADATA_ASMT_2016_NC_GRADE_08_MATH_SUMMATIVE_7d10d26b-b013-4cdd-a916-5d577e895cff')

        # # TODO: Add expected 'num_rows'(int) in the function calls
        self.validate_csv_file(grade7_ela, 9)
        self.validate_csv_file(grade7_math, 9)
        self.validate_csv_file(grade8_ela, 2)
        self.validate_csv_file(grade8_math, 3)

        identification = {'Guid': '7d10d26b-b013-4cdd-a916-5d577e895cff', 'Type': 'SUMMATIVE', 'Year': '2016',
                          'Period': 'Spring 2016', 'Version': 'V1', 'Subject': 'Math', 'EffectiveDate': '20160404'}
        overall = {'MinScore': '1200', 'MaxScore': '2400'}
        perf_level = {'Level1': {'Name': 'Minimal Understanding'},
                      'Level2': {'Name': 'Partial Understanding',
                                 'CutPoint': '1400'},
                      'Level3': {'Name': 'Adequate Understanding',
                                 'CutPoint': '1800'},
                      'Level4': {'Name': 'Thorough Understanding',
                                 'CutPoint': '2100'},
                      'Level5': {'Name': '', 'CutPoint': ''}}
        claims = {'Claim1': {'Name': 'Concepts & Procedures',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim2': {'Name': 'Problem Solving and Modeling & Data Analysis',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim3': {'Name': 'Communicating Reasoning',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim4': {'Name': '',
                             'MinScore': '',
                             'MaxScore': ''}}

        json_data = self.validate_json_file(metadata_json_gr7_math)
        self.check_fields_and_values(json_data, "Identification", identification)
        self.check_fields_and_values(json_data, "Overall", overall)
        self.check_fields_and_values(json_data, "PerformanceLevels", perf_level)
        self.check_fields_and_values(json_data, 'Claims', claims)

        json_data = self.validate_json_file(metadata_json_gr8_math)
        self.check_fields_and_values(json_data, "Identification", identification)
        self.check_fields_and_values(json_data, "Overall", overall)
        self.check_fields_and_values(json_data, "PerformanceLevels", perf_level)
        self.check_fields_and_values(json_data, 'Claims', claims)

    def test_extract_raw_data_los(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("942", "ui-jqgrid-ftable")
        self.drill_down_navigation("12", "jqgfirstrow")

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.select_extract_option(export_popup, 'Student assessment results')

        file_name = None
        for file in os.listdir(DOWNLOAD_FILES):
            if file.endswith(".zip"):
                file_name = file
        filepath = DOWNLOAD_FILES + file_name
        self.files_to_cleanup_at_end.append(filepath)
        self.unzip_file_to_directory(filepath, UNZIPPED_FILES)
        filenames = self.get_file_names(UNZIPPED_FILES)
        csv_filenames = filenames[0]
        json_filenames = filenames[1]

        grade12_ela = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_12_ELA_SUMMATIVE')
        grade12_math = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_12_MATH_SUMMATIVE')
        self.validate_csv_file(grade12_ela, 3)
        self.validate_csv_file(grade12_math, 3)

        metadata_json_gr12_math = self.check_file_exists(json_filenames,
                                                         'METADATA_ASMT_2016_NC_GRADE_12_MATH_SUMMATIVE_7d10d26b-b013-4cdd-a916-5d577e895cff')
        metadata_json_gr12_ela = self.check_file_exists(json_filenames,
                                                        'METADATA_ASMT_2016_NC_GRADE_12_ELA_SUMMATIVE_3b10d26b-b013-4cdd-a916-5d577e895ed4')

        identification = {'Guid': '7d10d26b-b013-4cdd-a916-5d577e895cff', 'Type': 'SUMMATIVE', 'Year': '2016',
                          'Period': 'Spring 2016', 'Version': 'V1', 'Subject': 'Math', 'EffectiveDate': '20160404'}
        overall = {'MinScore': '1200', 'MaxScore': '2400'}
        perf_level = {'Level1': {'Name': 'Minimal Understanding'},
                      'Level2': {'Name': 'Partial Understanding',
                                 'CutPoint': '1400'},
                      'Level3': {'Name': 'Adequate Understanding',
                                 'CutPoint': '1800'},
                      'Level4': {'Name': 'Thorough Understanding',
                                 'CutPoint': '2100'},
                      'Level5': {'Name': '', 'CutPoint': ''}}
        claims = {'Claim1': {'Name': 'Concepts & Procedures',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim2': {'Name': 'Problem Solving and Modeling & Data Analysis',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim3': {'Name': 'Communicating Reasoning',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim4': {'Name': '',
                             'MinScore': '',
                             'MaxScore': ''}}
        json_data = self.validate_json_file(metadata_json_gr12_math)
        self.check_fields_and_values(json_data, "Identification", identification)
        self.check_fields_and_values(json_data, "Overall", overall)
        self.check_fields_and_values(json_data, "PerformanceLevels", perf_level)
        self.check_fields_and_values(json_data, 'Claims', claims)

        identification = {'Guid': '3b10d26b-b013-4cdd-a916-5d577e895ed4', 'Type': 'SUMMATIVE', 'Year': '2016',
                          'Period': 'Spring 2016', 'Version': 'V1', 'Subject': 'ELA', 'EffectiveDate': '20160404'}
        overall = {'min_score': '1200', 'max_score': '2400'}
        overall = {'MinScore': '1200', 'MaxScore': '2400'}
        perf_level = {'Level1': {'Name': 'Minimal Understanding'},
                      'Level2': {'Name': 'Partial Understanding',
                                 'CutPoint': '1400'},
                      'Level3': {'Name': 'Adequate Understanding',
                                 'CutPoint': '1800'},
                      'Level4': {'Name': 'Thorough Understanding',
                                 'CutPoint': '2100'},
                      'Level5': {'Name': '', 'CutPoint': ''}}
        claims = {'Claim1': {'Name': 'Reading',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim2': {'Name': 'Writing',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim3': {'Name': 'Listening',
                             'MinScore': '1200',
                             'MaxScore': '2400'},
                  'Claim4': {'Name': 'Research & Inquiry',
                             'MinScore': '1200',
                             'MaxScore': '2400'}}
        ela_json_data = self.validate_json_file(metadata_json_gr12_ela)
        self.check_fields_and_values(ela_json_data, "Identification", identification)
        self.check_fields_and_values(ela_json_data, "Overall", overall)
        self.check_fields_and_values(ela_json_data, "PerformanceLevels", perf_level)
        self.check_fields_and_values(ela_json_data, 'Claims', claims)

    def test_multi_asmt_per_grade(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.select_academic_year("2015")
        self.drill_down_navigation("07", "jqgfirstrow")

        export_popup = self.open_file_download_popup()
        self.select_extract_option(export_popup, 'Student assessment results')

        file_name = None
        for file in os.listdir(DOWNLOAD_FILES):
            if file.endswith(".zip"):
                file_name = file
        filepath = DOWNLOAD_FILES + file_name
        self.files_to_cleanup_at_end.append(filepath)
        self.unzip_file_to_directory(filepath, UNZIPPED_FILES)
        filenames = self.get_file_names(UNZIPPED_FILES)
        csv_filenames = filenames[0]
        json_filenames = filenames[1]

        csv_filenames, json_filenames = self.unzip_raw_extract_file(filepath)
        self.assertEqual(len(csv_filenames), 3)
        self.assertEqual(len(json_filenames), 3)
        self.check_file_exists(json_filenames,
                               'METADATA_ASMT_2015_NC_GRADE_07_MATH_SUMMATIVE_5adb5efb-d4cb-43c4-bbdf-602794b0e4ef')
        self.check_file_exists(json_filenames,
                               'METADATA_ASMT_2015_NC_GRADE_07_MATH_SUMMATIVE_8d10d26b-b013-4cdd-a916-5d577e895cce')

    def test_extract_sar_los_iab(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")

        self.select_academic_year_los(6, "2014 - 2015")
        self.check_current_selected_opportunity('2014 - 2015 · Summative')
        self.total_los_records(5)
        self.check_opportunity_selectors(['Summative', 'Interim Comprehensive', 'Interim Assessment Blocks'])
        self.select_opportunity_los('Interim Assessment Blocks')
        self.check_iab_column_headers(['Students', 'Algebra and Functions - Line...', 'Algebra and Functions - Quad...',
                                       'Geometry - Right Triangle Ra...', 'Algebra and Functions - Expo...',
                                       'Algebra and Functions - Poly...', 'Algebra and Functions - Radi...',
                                       'Algebra and Functions - Rati...', 'Algebra and Functions - Trig...',
                                       'Geometry - Transformations i...', 'Geometry - Three - Dimension...',
                                       'Geometry - Proofs', 'Geometry - Circles', 'Geometry - Applications',
                                       'Interpreting Categorical and...', 'Probability',
                                       'Making Inferences and Justif...', 'Mathematics Performance Task...'])
        # self.check_iab_column_headers (['Students', 'Algebra and Functions - Line...', 'Algebra and Functions - Quad...', 'Geometry - Right Triangle Ra...', 'Algebra and Functions - Expo...', 'Algebra and Functions - Poly...'])
        self.check_current_subject_view("Mathematics")
        self.validate_interim_disclaimer()
        time.sleep(5)
        students = ["Sanders, Rachel"]
        self.check_student_record(students)
        self.total_iab_los_records(1)
        ela_headers = ["Students", "Read Literary Texts", "Read Informational Texts", "Edit/Revise", "Brief Writes",
                       "Listen/Interpret",
                       "Research", "Narrative Performance Task", "Explanatory Performance Task...",
                       "Argument Performance Task"]
        self.select_los_view_iab("ELA/Literacy", ela_headers)
        students = ["Patterson, Verna",
                    "Sanders, Rachel"]
        self.check_student_record(students)
        self.total_iab_los_records(2)

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup,
                                  ['Current view', 'Student assessment results', 'Printable student reports',
                                   'State Downloads'])
        self.select_extract_option(export_popup, 'Student assessment results')

        file_name = None
        for file in os.listdir(DOWNLOAD_FILES):
            if file.endswith(".zip"):
                file_name = file
        filepath = DOWNLOAD_FILES + file_name
        self.files_to_cleanup_at_end.append(filepath)
        self.unzip_file_to_directory(filepath, UNZIPPED_FILES)
        filenames = self.get_file_names(UNZIPPED_FILES)
        csv_filenames = filenames[0]
        json_filenames = filenames[1]
        print(len(csv_filenames))
        print(len(json_filenames))

    #        grade12_ela = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_12_ELA_SUMMATIVE')
    #        grade12_math = self.check_file_exists(csv_filenames, 'ASMT_2016_GRADE_12_MATH_SUMMATIVE')
    #        self.validate_csv_file(grade12_ela, 3)
    #        self.validate_csv_file(grade12_math, 3)
    #
    #        metadata_json_gr12_math = self.check_file_exists(json_filenames, 'METADATA_ASMT_2016_NC_GRADE_12_MATH_SUMMATIVE_7d10d26b-b013-4cdd-a916-5d577e895cff')
    #        metadata_json_gr12_ela = self.check_file_exists(json_filenames, 'METADATA_ASMT_2016_NC_GRADE_12_ELA_SUMMATIVE_3b10d26b-b013-4cdd-a916-5d577e895ed4')
    #
    #        identification = {'Guid': '7d10d26b-b013-4cdd-a916-5d577e895cff', 'Type': 'SUMMATIVE', 'Year': '2016', 'Period': 'Spring 2016', 'Version': 'V1', 'Subject': 'Math', 'EffectiveDate': '20160404'}
    #        overall = {'MinScore': '1200', 'MaxScore': '2400'}
    #        perf_level = {'Level1': {'Name': 'Minimal Understanding'},
    #                      'Level2': {'Name': 'Partial Understanding',
    #                                 'CutPoint': '1400'},
    #                      'Level3': {'Name': 'Adequate Understanding',
    #                                 'CutPoint': '1800'},
    #                      'Level4': {'Name': 'Thorough Understanding',
    #                                 'CutPoint': '2100'},
    #                      'Level5': {'Name': '', 'CutPoint': ''}}
    #        claims = {'Claim1': {'Name': 'Concepts & Procedures',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'},
    #                  'Claim2': {'Name': 'Problem Solving and Modeling & Data Analysis',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'},
    #                  'Claim3': {'Name': 'Communicating Reasoning',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'},
    #                  'Claim4': {'Name': '',
    #                             'MinScore': '',
    #                             'MaxScore': ''}}
    #        json_data = self.validate_json_file(metadata_json_gr12_math)
    #        self.check_fields_and_values(json_data, "Identification", identification)
    #        self.check_fields_and_values(json_data, "Overall", overall)
    #        self.check_fields_and_values(json_data, "PerformanceLevels", perf_level)
    #        self.check_fields_and_values(json_data, 'Claims', claims)
    #
    #        identification = {'Guid': '3b10d26b-b013-4cdd-a916-5d577e895ed4', 'Type': 'SUMMATIVE', 'Year': '2016', 'Period': 'Spring 2016', 'Version': 'V1', 'Subject': 'ELA', 'EffectiveDate': '20160404'}
    #        overall = {'min_score': '1200', 'max_score': '2400'}
    #        overall = {'MinScore': '1200', 'MaxScore': '2400'}
    #        perf_level = {'Level1': {'Name': 'Minimal Understanding'},
    #                      'Level2': {'Name': 'Partial Understanding',
    #                                 'CutPoint': '1400'},
    #                      'Level3': {'Name': 'Adequate Understanding',
    #                                 'CutPoint': '1800'},
    #                      'Level4': {'Name': 'Thorough Understanding',
    #                                 'CutPoint': '2100'},
    #                      'Level5': {'Name': '', 'CutPoint': ''}}
    #        claims = {'Claim1': {'Name': 'Reading',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'},
    #                  'Claim2': {'Name': 'Writing',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'},
    #                  'Claim3': {'Name': 'Listening',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'},
    #                  'Claim4': {'Name': 'Research & Inquiry',
    #                             'MinScore': '1200',
    #                             'MaxScore': '2400'}}
    #        ela_json_data = self.validate_json_file(metadata_json_gr12_ela)
    #        self.check_fields_and_values(ela_json_data, "Identification", identification)
    #        self.check_fields_and_values(ela_json_data, "Overall", overall)
    #        self.check_fields_and_values(ela_json_data, "PerformanceLevels", perf_level)
    #        self.check_fields_and_values(ela_json_data, 'Claims', claims)

    def check_raw_zipfile_present(self, prefix):
        '''
        Check that the csv file is downloaded in the DOWNLOAD_FILES directory
        return file: Filename
        type file: string
        '''
        found = False
        for _file in os.listdir(DOWNLOAD_FILES):
            if fnmatch.fnmatch(_file, '*.zip'):
                if prefix in _file:
                    found = True
                    break
        self.assertTrue(found, "No CSV files found with the given prefix and suffix")
        return _file

    def unzip_raw_extract_file(self, zip_file_path):
        '''
        Unzips the zip file inside the UNZIPPED_FILES directory
        '''
        csv_file_names = []
        json_file_names = []
        # unzip the file
        with zipfile.ZipFile(zip_file_path, "r") as unzipped_file:
            unzipped_file.extractall(UNZIPPED_FILES)
        for _file in os.listdir(UNZIPPED_FILES):
            if fnmatch.fnmatch(_file, '*.csv'):
                csv_file_names.append(str(_file))
            elif fnmatch.fnmatch(_file, '*.json'):
                json_file_names.append(str(_file))
        print("Unzipped the raw data extract files")
        return csv_file_names, json_file_names

    def check_file_exists(self, all_file_names, prefix):
        found = False
        for _file in all_file_names:
            if (prefix in _file):
                found = True
                break
        self.assertTrue(found, "No CSV files found with the given prefix and suffix")
        return _file

    def validate_csv_file(self, filename, num_rows):
        expected_headers = ['AssessmentGuid', 'AssessmentSessionLocationId', 'AssessmentSessionLocation',
                            'AssessmentLevelForWhichDesigned',
                            'StateAbbreviation', 'ResponsibleDistrictIdentifier', 'OrganizationName',
                            'ResponsibleSchoolIdentifier',
                            'NameOfInstitution', 'StudentIdentifier', 'FirstName', 'MiddleName', 'LastOrSurname',
                            'Sex', 'Birthdate', 'ExternalSSID', 'GradeLevelWhenAssessed', 'Group1Id', 'Group1Text',
                            'Group2Id', 'Group2Text', 'Group3Id', 'Group3Text', 'Group4Id', 'Group4Text',
                            'Group5Id', 'Group5Text', 'Group6Id', 'Group6Text', 'Group7Id', 'Group7Text',
                            'Group8Id', 'Group8Text', 'Group9Id', 'Group9Text', 'Group10Id', 'Group10Text',
                            'AssessmentAdministrationFinishDate', 'AssessmentSubtestResultScoreValue',
                            'AssessmentSubtestMinimumValue', 'AssessmentSubtestMaximumValue',
                            'AssessmentPerformanceLevelIdentifier',
                            'AssessmentSubtestResultScoreClaim1Value', 'AssessmentClaim1PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim1MinimumValue', 'AssessmentSubtestClaim1MaximumValue',
                            'AssessmentSubtestResultScoreClaim2Value', 'AssessmentClaim2PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim2MinimumValue', 'AssessmentSubtestClaim2MaximumValue',
                            'AssessmentSubtestResultScoreClaim3Value', 'AssessmentClaim3PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim3MinimumValue', 'AssessmentSubtestClaim3MaximumValue',
                            'AssessmentSubtestResultScoreClaim4Value', 'AssessmentClaim4PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim4MinimumValue', 'AssessmentSubtestClaim4MaximumValue',
                            'HispanicOrLatinoEthnicity', 'AmericanIndianOrAlaskaNative', 'Asian',
                            'BlackOrAfricanAmerican',
                            'NativeHawaiianOrOtherPacificIslander', 'White', 'DemographicRaceTwoOrMoreRaces',
                            'IDEAIndicator',
                            'LEPStatus', 'Section504Status', 'EconomicDisadvantageStatus', 'MigrantStatus',
                            'AssessmentType', 'AssessmentYear', 'AssessmentAcademicSubject',
                            'AccommodationAmericanSignLanguage',
                            'AccommodationNoiseBuffer', 'AccommodationPrintOnDemandItems', 'AccommodationBraille',
                            'AccommodationClosedCaptioning',
                            'AccommodationTextToSpeech', 'AccommodationAbacus', 'AccommodationAlternateResponseOptions',
                            'AccommodationCalculator', 'AccommodationMultiplicationTable', 'AccommodationPrintOnDemand',
                            'AccommodationReadAloud', 'AccommodationScribe', 'AccommodationSpeechToText',
                            'AccommodationStreamlineMode',
                            'AdministrationCondition', 'CompleteStatus']

        file_path = UNZIPPED_FILES + filename
        all_rows = []
        with open(file_path) as f:
            each = csv.reader(f)
            for row in each:
                all_rows.append(row)
        self.assertEqual(all_rows[0], expected_headers)
        self.assertEqual(len(all_rows), num_rows, "Incorrect number of rows found in the CSV raw data extract.")

    def validate_json_file(self, filename):
        file_path = UNZIPPED_FILES + filename
        with open(file_path) as f:
            json_data = json.load(f)
            self.assertEqual(json_data['content'], 'assessment')
        return json_data
