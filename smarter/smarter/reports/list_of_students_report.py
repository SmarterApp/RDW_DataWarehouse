'''
Created on Jan 24, 2013

@author: tosako
'''

from edapi.utils import report_config
from .connector import DBConnector
from sqlalchemy.orm.query import Query
from sqlalchemy.schema import Table
from sqlalchemy.sql.expression import func


@report_config(name="list_of_students",
               params={"districtId": {
                                      "type": "integer",
                                      "required": True
                                      },
                       "schoolId": {
                                   "type": "integer",
                                   "required": True
                                   },
                       "asmtGrade": {
                                    "type": "integer",
                                    "required": True
                                    },
                       "asmtSubject": {
                                      "type": "array",
                                      "required": False,
                                      "minLength": 0,
                                      "maxLength": 2,
                                      "items":{
                                               "type": "string"
                                               }
                                      }
                       }
               )
def get_list_of_students_report(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    districtId = params['districtId']
    schoolId = params['schoolId']
    asmtGrade = params['asmtGrade']

    # asmtSubject is optional. 
    # TODO: make sure get it as an array
    asmtSubject = None
    if 'asmtSubject' in params:
        asmtSubject = params['asmtSubject']

    # get sql session
    connector.open_session()


    '''
    Output:
    Student last name
    student first name
    student middle initial
    student assessment grade
    student enrollment grade
    assessment array [teacher full name, assmt subject, claim scores and descriptions ]
    '''

    dim_student = connector.get_table('dim_student')
    dim_stdnt_tmprl_data = connector.get_table('dim_stdnt_tmprl_data')
    dim_grade = connector.get_table('dim_grade')
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    dim_asmt_type = connector.get_table('dim_asmt_type')

    #TODO: find out where can we get enrollment grade
    #TODO: missing dim_teacher from the DB


    #I use label function as experimental.  to eliminate ambiguous column namez
    if isinstance(dim_student, Table) and isinstance(dim_stdnt_tmprl_data, Table) and isinstance(dim_grade, Table) and isinstance(fact_asmt_outcome, Table) and isinstance(dim_asmt_type, Table):
        query = Query([dim_student.c.first_name.label('first_name'),
                            func.substr(dim_student.c.middle_name,1,1).label('middle_name'),
                            dim_student.c.last_name.label('last_name'),
                            dim_asmt_type.c.asmt_grade.label('asmt_grade'),
                            dim_asmt_type.c.asmt_subject.label('asmt_subject'),
                            fact_asmt_outcome.c.asmt_score.label('asmt_score'),
                            fact_asmt_outcome.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                            fact_asmt_outcome.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                            fact_asmt_outcome.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                            fact_asmt_outcome.c.asmt_claim_4_name.label('asmt_claim_4_name'),
                            fact_asmt_outcome.c.asmt_claim_1_score.label('asmt_claim_1_score'),
                            fact_asmt_outcome.c.asmt_claim_2_score.label('asmt_claim_2_score'),
                            fact_asmt_outcome.c.asmt_claim_3_score.label('asmt_claim_3_score'),
                            fact_asmt_outcome.c.asmt_claim_4_score.label('asmt_claim_4_score')])\
                            .join(dim_student, dim_student.c.student_id == fact_asmt_outcome.c.student_id)\
                            .join(dim_asmt_type, dim_asmt_type.c.asmt_type_id == fact_asmt_outcome.c.asmt_type_id)
