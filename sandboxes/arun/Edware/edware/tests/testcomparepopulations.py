'''
Created on Dec 28, 2012

@author: V5102883
'''
import unittest
from edware.services.comparepopulations import generateComparePopulationsReport

class Test(unittest.TestCase):

#    def testQueryBuilder(self):
#        params = {"segment_by":"student","grades":["1"],"year_range":["ALL"],"district_filter":[],"time_period":["ALL"],"school_filter":["ALL"],"teacher_filter" : ["ALL"]}
#        sql = getComparePopulationsQuery(params)
#        assert sql is not None
#        #print(sql)
#        pass

    keys = ("segment_by","grades","year_range","time_period","teacher_filter","district_filter","school_filter","student_id","subject_code","grade_divider","report_level","school_group_type")

    def testComparePopulationsQueryALL(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"], "student_id" : "6190",'district_filter': ["677","678"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsQueryALL : ", str(err))
        

    def testComparePopulationsDistrictFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ELA"],"student_id" : "6201",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)      
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsDistrictFilter : ", str(err))

    def testComparePopulationsSchoolFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6201",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ['6601','6621'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsSchoolFilter : ", str(err))

    def testComparePopulationsTeacherFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsTeacherFilter : ", str(err))

    def testComparePopulationsGradesFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6201",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["K","3"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsGradesFilter : ", str(err))

    def testComparePopulationsTimePeriod(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6195",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsTimePeriod : ", str(err))
        
    def testComparePopulationsYearRange(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6187",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['2388','2389'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ["2012-2013","2011-2012"]}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsYearRange : ", str(err))        

    def testComparePopulationsAllValues(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],"student_id" : "6201","district_filter": ["677","678"], "segment_by": "student", "school_filter": ["6601","6621"], "teacher_filter": ["2388","2389"], "grades": ["K","6"], "time_period": ["MOY"], "year_range": ["2012-2013","2011-2012"]}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsYearRange : ", str(err)) 

    def testComparePopulationsGroupByTeacher(self):
        params = {"grade_divider" : "true","subject_code": ["ELA"],'district_filter': ["ALL"], 'segment_by': 'teacher', 'school_filter': ['ALL'], 'teacher_filter': ['135'], 'grades': ["3"], 'time_period': ["MOY"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsDistrictFilter : ", str(err))
        
    def testComparePopulationsGroupBySchool(self):
        params = {"grade_divider" : "false","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'school', 'school_filter': ['7652'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsDistrictFilter : ", str(err))


    def testComparePopulationsGroupBySchoolGroup(self):
        params = {"grade_divider" : "false","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'school_grp', 'school_filter': ['7652'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(Test.keys)
        try:
            resultlist = generateComparePopulationsReport(params)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testComparePopulationsDistrictFilter : ", str(err))        

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testQueryBuilder']
    unittest.main()