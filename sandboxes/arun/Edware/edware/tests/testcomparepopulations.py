'''
Created on Dec 28, 2012

@author: V5102883
'''
import unittest
from edware.services.querybuilder import getComparePopulationsQuery
from edware.services.comparepopulations import generateComparePopulationsReport

class Test(unittest.TestCase):

#    def testQueryBuilder(self):
#        params = {"segment_by":"student","grades":["1"],"year_range":["ALL"],"district_filter":[],"time_period":["ALL"],"school_filter":["ALL"],"teacher_filter" : ["ALL"]}
#        sql = getComparePopulationsQuery(params)
#        assert sql is not None
#        #print(sql)
#        pass

    def testComparePopulationsQuery(self):
        #params = {"segment_by":"student","grades":["K","7","6"],"year_range":["ALL"],"district_filter":[],"time_period":["MOY"],"school_filter":["ALL"],"teacher_filter" : ["ALL"]}
        params = {'district_filter': [], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        resultlist = generateComparePopulationsReport(params)
        print(resultlist)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testQueryBuilder']
    unittest.main()