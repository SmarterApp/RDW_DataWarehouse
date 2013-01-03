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

    def testAllReportParameters(self):
          
        try:
            resultlist = ReportUtility.getGradeList(self)
            for row in resultlist:
                print(row)
            pass
        except Exception as err:
            raise AssertionError("Exception occurred when running testGradeList : ", str(err))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testQueryBuilder']
    unittest.main()