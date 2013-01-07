'''
Created on Dec 28, 2012

@author: V5102883
'''
import unittest
from smarter.services.comparepopulations import generateComparePopulationsReportAlchemy
from smarter.utils.databaseconnections import getSQLAlchemyConnection

class ComparePopulationsReportTest(unittest.TestCase):

    keys = ("segment_by","grades","year_range","time_period","teacher_filter","district_filter","school_filter","student_id","subject_code","grade_divider","report_level","school_group_type")

    _dbConnection = getSQLAlchemyConnection()

    @classmethod
    def insertTestData(self):
        assert self._dbConnection
        with open('smarter/tests/comPopSetupData.sql', 'r') as f:
            for line in f:
                self._dbConnection.execute(line)
    @classmethod
    def deleteTestData(self):
        assert self._dbConnection
        with open('smarter/tests/comPopTearDownData.sql', 'r') as f:
            for line in f:
                self._dbConnection.execute(line)

    @classmethod
    def setUpClass(self):
        #Clean up test data first, if any
        ComparePopulationsReportTest.deleteTestData()
        #Insert test data
        ComparePopulationsReportTest.insertTestData()
        print("setup complete")

    @classmethod
    def tearDownClass(self):
        ComparePopulationsReportTest.deleteTestData()
        print("teardown complete") 


    def testComparePopulationsQueryALL(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"], "student_id" : "9888881",'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 2 records have been returned because this student only has two assessment results
            assert len(resultlist)==2
            #check if the returned student id is the input student
            for row in resultlist:
                print(row)
                assert row[0]==9888881            
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsQueryALL : {0}".format(str(err)))
        

    def testComparePopulationsDistrictFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["999980"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)      
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 8 records have been returned because this school group only has 8 records
            assert len(resultlist)==8
            #check if the returned school group id is the input id
            for row in resultlist:
                print(row)
                assert row[9]==999980  
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))

    def testComparePopulationsSchoolFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["999993","999991"], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 4 records have been returned - 2 for each school
            assert len(resultlist)==4
            #check if the returned school id is the input id
            s1=0
            s2=0
            for row in resultlist:
                print(row)
                if row[7]==999993:
                    s1=s1+1
                elif row[7]==999991:
                    s2=s2+1
            assert s1==2
            assert s2==2
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsSchoolFilter : {0}".format(str(err)))

    def testComparePopulationsTeacherFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ['999990','999991'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 4 records have been returned - 2 for each teacher
            assert len(resultlist)==4
            #check if the returned teacher id is the input id
            s1=0
            s2=0
            for row in resultlist:
                print(row)
                if row[5]==999990:
                    s1=s1+1
                elif row[5]==999991:
                    s2=s2+1
            assert s1==2
            assert s2==2
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsTeacherFilter : {0}".format(str(err)))

    def testComparePopulationsGradesFilter(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["ALL"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ["ALL"], 'grades': ["T-1","T-2"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 4 records have been returned - 2 for each grade
            assert len(resultlist)==4
            #check if the returned grade id is the input id
            s1=0
            s2=0
            for row in resultlist:
                print(row)
                if row[13]=="T-1":
                    s1=s1+1
                elif row[13]=="T-2":
                    s2=s2+1
            assert s1==2
            assert s2==2
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsGradesFilter : {0}".format(str(err)))

    def testComparePopulationsTimePeriod(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["999980"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ["ALL"], 'grades': ["ALL"], 'time_period': ["BOY","MOY"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 8 records have been returned - 4 for each period
            assert len(resultlist)==8
            #check if the returned period id is the input id
            s1=0
            s2=0
            for row in resultlist:
                print(row)
                if row[15]=="BOY":
                    s1=s1+1
                elif row[15]=="MOY":
                    s2=s2+1
            assert s1==4
            assert s2==4
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsTimePeriod : {0}".format(str(err)))
        
    def testComparePopulationsYearRange(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["999980"], 'segment_by': 'student', 'school_filter': ["ALL"], 'teacher_filter': ["ALL"], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ["2012-2013","2011-2012"]}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 8 records have been returned - 4 for each range
            assert len(resultlist)==8
            #check if the returned range id is the input id
            s1=0
            s2=0
            for row in resultlist:
                print(row)
                if row[16]=="2012-2013":
                    s1=s1+1
                elif row[16]=="2011-2012":
                    s2=s2+1
            assert s1==4
            assert s2==4
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsYearRange : {0}".format(str(err)))       

    def testComparePopulationsSubjectFilter(self):
        params = {"grade_divider" : "true","subject_code": ["T-ELA","T-MATH"],'district_filter': ["999980"], 'segment_by': 'student', 'school_filter': ['ALL'], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)      
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 8 records have been returned - 4 for each subject
            assert len(resultlist)==8
            #check if the returned subject id is the input id
            s1=0
            s2=0
            for row in resultlist:
                print(row)
                if row[14]=="T-ELA":
                    s1=s1+1
                elif row[14]=="T-MATH":
                    s2=s2+1
            assert s1==4
            assert s2==4 
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))


    def testComparePopulationsAllValues(self):
        params = {"grade_divider" : "true","subject_code": ["T-ELA","T-MATH"],"district_filter": ["999980"], "segment_by": "student", "school_filter": ["999993","999991"], "teacher_filter": ["999992","999993"], "grades": ["T-K","T-Pre-K","T-2","T-1"], "time_period": ["BOY","MOY"], "year_range": ["2012-2013","2011-2012"]}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 4 records have been returned
            assert len(resultlist)==4
            #check if the returned values are consistent with the input
            year_range_12=0
            year_range_13=0
            time_period_moy=0
            time_period_boy=0
            grade_k=0
            grade_1=0
            grade_pk=0
            grade_2=0
            teacher_999992=0
            teacher_999993=0
            school_999993=0
            school_999991=0
            sub_ela=0
            sub_math=0
            for row in resultlist:
                print(row)
                #check district
                assert row[9]==999980
                #check all other criteria                
                if row[16]=="2012-2013":
                    year_range_13=year_range_13+1
                elif row[16]=="2011-2012":
                    year_range_12=year_range_12+1
                if row[15]=="BOY":
                    time_period_boy=time_period_boy+1
                elif row[15]=="MOY":
                    time_period_moy=time_period_moy+1   
                if row[13]=="T-1":
                    grade_1=grade_1+1
                elif row[13]=="T-2":
                    grade_2=grade_2+1 
                elif row[13]=="T-Pre-K":
                    grade_pk=grade_pk+1
                elif row[13]=="T-K":
                    grade_k=grade_k+1 
                if row[5]==999992:
                    teacher_999992=teacher_999992+1
                elif row[5]==999993:
                    teacher_999993=teacher_999993+1
                if row[7]==999993:
                    school_999993=school_999993+1
                elif row[7]==999991:
                    school_999991=school_999991+1
                if row[14]=="T-ELA":
                    sub_ela=sub_ela+1
                elif row[14]=="T-MATH":
                    sub_math=sub_math+1                                                                                                                                  
            assert year_range_12==2
            assert year_range_13==2
            assert time_period_moy==2
            assert time_period_boy==2
            assert grade_k==1
            assert grade_1==1
            assert grade_pk==1
            assert grade_2==1
            assert teacher_999992==2
            assert teacher_999993==2
            assert school_999993==2
            assert school_999991==2
            assert sub_ela==2
            assert sub_math==2            
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsYearRange : {0}".format(str(err)))

    def testComparePopulationsGroupByTeacher(self):
        params = {"grade_divider" : "true","subject_code": ["ALL"],'district_filter': ["999980"], 'segment_by': 'teacher', 'school_filter': ['ALL'], 'teacher_filter': ["ALL"], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['ALL']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 8 records have been returned
            assert len(resultlist)==8
            #check if the returned values are consistent with the input
            teacher_999992=0
            teacher_999993=0
            teacher_999991=0
            teacher_999990=0
            for row in resultlist:
                print(row)
                #check if student details are not returned as the query is grouped at teacher level
                assert row[0]==None
                assert row[1]==None
                assert row[2]==None
                if row[5]==999992:
                    teacher_999992=teacher_999992+1
                elif row[5]==999993:
                    teacher_999993=teacher_999993+1
                elif row[5]==999991:
                    teacher_999991=teacher_999991+1
                elif row[5]==999990:
                    teacher_999990=teacher_999990+1                    
            assert teacher_999992==2
            assert teacher_999993==2
            assert teacher_999991==2
            assert teacher_999990==2
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))
        
    def testComparePopulationsGroupBySchool(self):
        params = {"grade_divider" : "false","subject_code": ["ALL"],'district_filter': ["999980"], 'segment_by': 'school', 'school_filter': ["ALL"], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ['2011-2012']}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 4 records have been returned
            assert len(resultlist)==4
            #check if the returned values are consistent with the input
            school_999992=0
            school_999993=0
            school_999991=0
            school_999990=0
            for row in resultlist:
                print(row)
                #check if student/teacher details are not returned as the query is grouped at teacher level
                assert row[0]==None
                assert row[1]==None
                assert row[2]==None
                assert row[5]==None
                assert row[6]==None                
                if row[7]==999992:
                    school_999992=school_999992+1
                elif row[7]==999993:
                    school_999993=school_999993+1
                elif row[7]==999991:
                    school_999991=school_999991+1
                elif row[7]==999990:
                    school_999990=school_999990+1                    
            assert school_999992==1
            assert school_999993==1
            assert school_999991==1
            assert school_999990==1
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))


    def testComparePopulationsGroupBySchoolGroup(self):
        params = {"grade_divider" : "false","subject_code": ["ALL"],'district_filter': ["999980"], 'segment_by': 'school_grp', 'school_filter': ["ALL"], 'teacher_filter': ['ALL'], 'grades': ["ALL"], 'time_period': ["ALL"], 'year_range': ["ALL"]}
        assert set(params.keys()).issubset(self.keys)
        try:
            resultlist = generateComparePopulationsReportAlchemy(params)
            #check if only 5 records have been returned
            assert len(resultlist)==5
            rows_checked=0
            #check if the returned values are consistent with the input
            for row in resultlist:
                print(row)
                #check if student/teacher/school details are not returned as the query is grouped at teacher level
                assert row[0]==None
                assert row[1]==None
                assert row[2]==None
                assert row[5]==None
                assert row[6]==None
                assert row[7]==None
                assert row[8]==None                
                #check if the calculated scores are correct
                if (row[14]=="T-MATH" and row[15]=="MOY" and row[21]=="Benchmark"):
                    assert row[3]==52.5 #assessment score
                    assert row[4]==2 # student count
                    rows_checked=rows_checked+1
                elif (row[14]=="T-MATH" and row[15]=="MOY" and row[21]=="Below Benchmark"):
                    assert row[3]==36 #assessment score
                    assert row[4]==1 # student count
                    rows_checked=rows_checked+1
                elif (row[14]=="T-MATH" and row[15]=="MOY" and row[21]=="Above Benchmark"):
                    assert row[3]==74 #assessment score
                    assert row[4]==1 # student count
                    rows_checked=rows_checked+1
                elif (row[14]=="T-ELA" and row[15]=="BOY" and row[21]=="Below Benchmark"):
                    assert row[3]==44 #assessment score
                    assert row[4]==2 # student count
                    rows_checked=rows_checked+1
                elif (row[14]=="T-ELA" and row[15]=="BOY" and row[21]=="Above Benchmark"):
                    assert row[3]==87 #assessment score
                    assert row[4]==2 # student count
                    rows_checked=rows_checked+1
            #check if all 5 rows have been checked
            assert rows_checked==5
        except Exception as err:
            raise Exception("Exception occurred when running testComparePopulationsDistrictFilter : {0}".format(str(err)))      

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testQueryBuilder']
    unittest.main()