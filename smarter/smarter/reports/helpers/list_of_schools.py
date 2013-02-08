'''
Created on Feb 2, 2013

@author: tosako
'''
from edapi.utils import report_config
from database.connector import DBConnector
from sqlalchemy.sql import select
#######################
# This function is available after branch edware_schema_20130201 is merged into master
#######################


__district_name = 'district_name'
__dim_school = 'dim_school'


#######################
# TODO: should we have a district id in order to seachr school id?
#######################


@report_config(name="list_of_schools",
               params={
                    __district_name: {
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

    district_name = params[__district_name]
    dim_school = connector.get_table(__dim_school)

    query = None

    if dim_school is not None:
        query = select([dim_school.c.school_id.lable('school_id'),
                        dim_school.c.school_name.label('school_name')])
        query = query.where(dim_school.c.district_name == district_name)
    result = connector.get_result(query)
    connector.close_connection()
    return result
