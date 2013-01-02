'''
Created on Dec 28, 2012

@author: V5102883
'''
import unittest
from edware.services.comparepopulations import generateComparePopulationsReport
from edware.utils.databaseconnections import getDatabaseConnection

class ComparePopulationsReportTest(unittest.TestCase):

    keys = ("segment_by","grades","year_range","time_period","teacher_filter","district_filter","school_filter","student_id","subject_code","grade_divider","report_level","school_group_type")

    _dbConnection = getDatabaseConnection()

    @classmethod
    def setUpClass(self):
        assert self._dbConnection
        with open('comPopSetupData.sql', 'r') as f:
            for line in f:
                statement = self._dbConnection.prepare(line)
                statement()
        print("setup complete")

    @classmethod
    def tearDownClass(self):
        assert self._dbConnection
        with open('comPopTearDownData.sql', 'r') as f:
            for line in f:
                statement = self._dbConnection.prepare(line)
                statement()
        print("teardown complete") 


    def testComparePopulationsQueryALL(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"], "student_id" : "6190",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsQueryALL : {0}".format(str(err)))
        

    def testComparePopulationsDistrictFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ELA"],"student_id" : "6201",'district_filter': ["677","678"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)      
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))

    def testComparePopulationsSchoolFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6201",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ['6601','6621'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsSchoolFilter : {0}".format(str(err)))

    def testComparePopulationsTeacherFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsTeacherFilter : {0}".format(str(err)))

    def testComparePopulationsGradesFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6201",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["K","3"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsGradesFilter : {0}".format(str(err)))

    def testComparePopulationsTimePeriod(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6195",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsTimePeriod : {0}".format(str(err)))
        
    def testComparePopulationsYearRange(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6187",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ["2012-2013","2011-2012"]}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsYearRange : {0}".format(str(err)))       

    def testComparePopulationsAllValues(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6201","district_filter": ["677","678"], "segment_by": "student", "school_filter": ["6601","6621"], "teacher_filter": ["2388","2389"], "grades": ["K","6"], "time_period": ["MOY"], "year_range": ["2012-2013","2011-2012"]}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsYearRange : {0}".format(str(err)))

    def testComparePopulationsGroupByTeacher(self):
        params = {"grade_divider" : "true","subject_code": ["ELA"],'district_filter': ["ALL"], 'segment_by': 'teacher', 'school_filter': ['ALL'], 'teacher_filter': ['135'], 'grades': ["3"], 'time_period': ["MOY"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))
        
    def testComparePopulationsGroupBySchool(self):
        params = {"grade_divider" : "false","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'school', 'school_filter': ['7652'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))


    def testComparePopulationsGroupBySchoolGroup(self):
        params = {"grade_divider" : "false","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'school_grp', 'school_filter': ['7652'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))      

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testQueryBuilder']
    unittest.main()