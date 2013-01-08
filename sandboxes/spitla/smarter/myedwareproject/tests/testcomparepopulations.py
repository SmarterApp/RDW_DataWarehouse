'''
Created on Dec 28, 2012

@author: V5102883
'''
import unittest
from myedwareproject.libs.report_utility import ReportUtility

class Test(unittest.TestCase):

#    def testQueryBuilder(self):
#        params = {"segment_by":"student","grades":["1"],"year_range":["ALL"],"district_filter":[],"time_period":["ALL"],"school_filter":["ALL"],"teacher_filter" : ["ALL"]}
#        sql = getComparePopulationsQuery(params)
#        assert sql is not None
#        #print(sql)
#        pass

    
    def testGradeList(self):
          
        try:
            resultlist = ReportUtility.getGradeList(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testGradeList : ", str(err))

    def testAssessmentList(self):
          
        try:
            resultlist = ReportUtility.getAssessmentList(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testAssessmentList : ", str(err))
        
    def testAssessmentCourseList(self):
          
        try:
            resultlist = ReportUtility.getAssessmentCourseList(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testAssessmentCourseList : ", str(err))
        
    def testSchoolYear(self):
          
        try:
            resultlist = ReportUtility.getSchoolYear(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testSchoolYear : ", str(err))
        
    def testStudentAttributeName(self):
          
        try:
            resultlist = ReportUtility.getStudentAttributeName(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testStudentAttributeName : ", str(err))
        
    def testBars(self):
          
        try:
            resultlist = ReportUtility.getBars(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testBars : ", str(err))
        
    def testReportsFor(self):
          
        try:
            resultlist = ReportUtility.getReportsFor(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testReportsFor : ", str(err))
        
    def testStudentsEnrolled(self):
          
        try:
            resultlist = ReportUtility.getStudentsEnrolled(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testStudentsEnrolled : ", str(err))
        
    def testSchoolGroupType(self):
          
        try:
            resultlist = ReportUtility.getSchoolGroupType(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testSchoolGroupType : ", str(err))
        
    def testMeasureType(self):
          
        try:
            resultlist = ReportUtility.getMeasureType(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testMeasureType : ", str(err))

    def testMeasure(self):
          
        try:
            resultlist = ReportUtility.getMeasure(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testMeasure : ", str(err))

    def testPerformanceMeasurement(self):
          
        try:
            resultlist = ReportUtility.getPerformanceMeasurement(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testPerformanceMeasurement : ", str(err))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testQueryBuilder']
    unittest.main()