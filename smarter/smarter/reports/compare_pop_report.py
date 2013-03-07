'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.utils import report_config
from smarter.reports.helpers.name_formatter import format_full_name_rev
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from sqlalchemy import func
from sqlalchemy.sql import case
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
#     asmt subject
#     achievement level name
#     number of students
#     total number of students


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
def get_comparing_populations_report(params):

    state_id = str(params[__stateId])

    # district_id is optional.
    district_id = None
    if district_id in params:
        district_id = params[district_id]

    # school_id is optional.
    school_id = None
    if school_id in params:
        school_id = params[school_id]

    # run query
    results = __run_query(state_id, district_id, school_id)

    # arrange results
    results = __arrange_results(results)

    return results


def __run_query(state_id, district_id, school_id):
    '''
    Run comparing populations query and return the results
    '''

    with SmarterDBConnection() as connector:

        # get handle to tables
        dim_inst_hier = connector.get_table('dim_inst_hier')
        dim_asmt = connector.get_table('dim_asmt')
        fact_asmt_outcome = connector.get_table('fact_asmt_outcome')

        query = select([dim_inst_hier.c.district_name.label('district_name'),
                        dim_asmt.c.asmt_subject.label('asmt_subject'),
                        func.count(case([(fact_asmt_outcome.c.asmt_perf_lvl == 1, fact_asmt_outcome.c.student_id)])).label('level1'),
                        func.count(case([(fact_asmt_outcome.c.asmt_perf_lvl == 2, fact_asmt_outcome.c.student_id)])).label('level2'),
                        func.count(case([(fact_asmt_outcome.c.asmt_perf_lvl == 3, fact_asmt_outcome.c.student_id)])).label('level3'),
                        func.count(case([(fact_asmt_outcome.c.asmt_perf_lvl == 4, fact_asmt_outcome.c.student_id)])).label('level4'),
                        func.count(fact_asmt_outcome.c.student_id).label('total')],
                       from_obj=[fact_asmt_outcome
                                 .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id, dim_asmt.c.asmt_type == 'SUMMATIVE', dim_asmt.c.most_recent == True, fact_asmt_outcome.c.most_recent == True))
                                 .join(dim_inst_hier, and_(dim_inst_hier.c.inst_hier_rec_id == fact_asmt_outcome.c.inst_hier_rec_id, dim_inst_hier.c.most_recent == True))])
        query = query.group_by(dim_inst_hier.c.district_name)
        query = query.group_by(dim_asmt.c.asmt_subject)
        query = query.order_by(dim_inst_hier.c.district_name).order_by(dim_asmt.c.asmt_subject.desc())

        results = connector.get_result(query)

    return results


def __arrange_results(results):
    '''
    Arrange the results in optimal way to be consumed by front-end
    '''
    return results
