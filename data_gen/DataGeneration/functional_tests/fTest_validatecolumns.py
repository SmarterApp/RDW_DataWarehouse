'''
Created on Aug 28, 2013

@author: bpatel
'''
import unittest
import os
import csv

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

components = __location__.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])
ENTITY_TO_PATH_DICT = {'InstitutionHierarchy': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_inst_hier.csv'),
                       'Section': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_section.csv'),
                       'Assessment': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_asmt.csv'),
                       'AssessmentOutcome': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                       'Staff': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_staff.csv'),
                       'ExternalUserStudent': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'external_user_student_rel.csv'),
                       'Student': os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_student.csv')}


class ColumnValidationFuncTest(unittest.TestCase):

    def create_schema(self):
        pass

    def drop_schema(self):
        pass

    def get_headers_from_csv(self):
        headers = {}
        for entity in ENTITY_TO_PATH_DICT:
            with open(ENTITY_TO_PATH_DICT[entity], "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                headers[entity] = next(csv_reader)
        return headers

    def get_headers_from_database(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
