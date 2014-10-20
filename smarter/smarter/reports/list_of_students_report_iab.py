'''
Created on Oct 20, 2014

@author: tosako
'''
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants


def get_list_of_students_iab(stateCode, districtId, schoolId, asmtGrade, asmtSubject, asmtYear):
    pass

def get_query(stateCode):
    with EdCoreDBConnection(state_code=stateCode) as connector:
        dim_student = connector.get_table(Constants.DIM_STUDENT)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)