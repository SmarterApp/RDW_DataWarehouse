'''
Created on Feb 2, 2013

@author: tosako
'''
from edapi.utils import report_config
from database.connector import DBConnector
from sqlalchemy.sql import select


__state_code = 'state_code'
__dim_district = 'dim_district'


@report_config(name="list_of_districts",
               params={
                    __state_code: {
                    "type": "string",
                    "maxLength": 2,
                    "required": True
                    }
               }
               )
def get_districts(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    state_code = params[__state_code]

    # get sql session
    connector.open_connection()

    dim_district = connector.get_table(__dim_district)

    query = None

    if dim_district is not None:
        query = select([dim_district.c.district_id.lable('district_id'),
                        dim_district.c.district_name.label('district_name')])
        query = query.where(dim_district.c.state_code == state_code)
    result = connector.get_result(query)
    connector.close_connection()
    return result
