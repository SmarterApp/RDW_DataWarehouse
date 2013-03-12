'''
Created on Mar 8, 2013

@author: dip
'''
from sqlalchemy.sql import and_, select
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import true
from smarter.reports.helpers.constants import Constants


def get_breadcrumbs_context(state_id=None, district_id=None, school_id=None, asmt_grade=None, student_name=None):
    '''
    Given certain known information, returns breadcrumbs context
    '''
    formatted_results = []
    with SmarterDBConnection() as connector:
        dim_inst_hier = connector.get_table('dim_inst_hier')

        # Limit result count to one
        # We limit the results to zero since we'll get multiple rows with the same values
        # Think of the case of querying for state name and id, we'll get all the schools in that state
        query = select([dim_inst_hier.c.state_name.label(Constants.STATE_NAME),
                        dim_inst_hier.c.state_code.label(Constants.STATE_CODE),
                        dim_inst_hier.c.district_name.label(Constants.DISTRICT_NAME),
                        dim_inst_hier.c.school_name.label(Constants.SCHOOL_NAME)],
                       from_obj=[dim_inst_hier], limit=1)

        query = query.where(and_(dim_inst_hier.c.most_recent == true()))
        # Currently, we only have state_id from comparing population report
        if state_id is not None:
            query = query.where(and_(dim_inst_hier.c.state_code == state_id))
        if district_id is not None:
            query = query.where(and_(dim_inst_hier.c.district_id == district_id))
            if school_id is not None:
                query = query.where(and_(dim_inst_hier.c.school_id == school_id))

        # run it and format the results
        results = connector.get_result(query)
        if results:
            result = results[0]

            # return an hierarchical ordered list
            formatted_results.append({'type': 'state', 'name': result[Constants.STATE_NAME], 'id': result[Constants.STATE_CODE]})
            if district_id is not None:
                formatted_results.append({'type': 'district', 'name': result[Constants.DISTRICT_NAME], 'id': district_id})
                if school_id is not None:
                    formatted_results.append({'type': 'school', 'name': result[Constants.SCHOOL_NAME], 'id': school_id})
                    if asmt_grade is not None:
                        formatted_results.append({'type': 'grade', 'name': asmt_grade})
                        if student_name is not None:
                            formatted_results.append({'type': 'student', 'name': student_name})

    return {'items': formatted_results}
