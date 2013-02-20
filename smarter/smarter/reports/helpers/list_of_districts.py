'''
Created on Feb 2, 2013

@author: tosako
'''
from edapi.utils import report_config
from database.connector import DBConnector
from sqlalchemy.sql import select


__state_code = 'state_code'
__dim_inst_hier = 'dim_inst_hier'


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

    dim_district = connector.get_table(__dim_inst_hier)

    query = select([dim_district.c.district_id.label('district_id'),
                    dim_district.c.district_name.label('district_name')]).distinct()
    query = query.where(dim_district.c.state_code == state_code).order_by(dim_district.c.district_name)
    result = connector.get_result(query)
    connector.close_connection()
    return result
