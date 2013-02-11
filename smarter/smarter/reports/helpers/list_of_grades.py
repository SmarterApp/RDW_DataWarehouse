'''
Created on Feb 2, 2013

@author: tosako
'''
from edapi.utils import report_config
from database.connector import DBConnector
from sqlalchemy.sql import select


__dim_grade = 'dim_grade'


@report_config(name="list_of_grades")
def get_grades(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    # get sql session
    connector.open_connection()

    dim_grade = connector.get_table(__dim_grade)

    query = select([dim_grade.c.grade_id.label('grade_id'),
                    dim_grade.c.grade_code.label('grade_code'),
                    dim_grade.c.grade_desc.label('grade_desc')])
    query = query.order_by(dim_grade.c.grade_code)
    result = connector.get_result(query)
    connector.close_connection()
    return result
