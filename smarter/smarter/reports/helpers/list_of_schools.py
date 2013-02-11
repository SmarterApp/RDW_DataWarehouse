'''
Created on Feb 2, 2013

@author: tosako
'''
from edapi.utils import report_config
from database.connector import DBConnector
from sqlalchemy.sql import select

__district_id = 'district_id'
__dim_school = 'dim_school'


@report_config(name="list_of_schools",
               params={
                    __district_id: {
                    "type": "string",
                    "required": True
                    }
               }
               )
def get_schools(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    # get sql session
    connector.open_connection()

    district_id = params[__district_id]
    dim_school = connector.get_table(__dim_school)

    query = select([dim_school.c.school_id.label('school_id'),
                    dim_school.c.school_name.label('school_name')])
    query = query.where(dim_school.c.district_id == district_id)
    query = query.order_by(dim_school.c.school_name)
    result = connector.get_result(query)
    connector.close_connection()
    return result
