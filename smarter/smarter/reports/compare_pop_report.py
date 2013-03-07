'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.utils import report_config
from smarter.reports.helpers.name_formatter import format_full_name_rev
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.database.connector import SmarterDBConnection

__stateId = 'stateId'
__districtId = 'districtId'
__schoolId = 'schoolId'

# Report service for Comparing Populations
# Output:
#    overall context id - state, district, or school
#    overall context name - state, district, or school
#    Array of
#     population id (district, school, or grade)
#     population name (district, school, or grade)
#     Array of
#       asmt subject
#       achievement level name
#       number of students


@report_config(
    name="comparing_populations",
    params={
        __stateId: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        __districtId: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        __schoolId: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        }
    })
def get_list_of_students_report(params):
    pass
