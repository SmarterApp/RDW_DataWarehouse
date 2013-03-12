'''
Created on Mar 8, 2013

@author: dip
'''
from sqlalchemy.sql import and_, select
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import true


def get_breadcrumbs_context(state_id=None, district_id=None, school_id=None, asmt_grade=None, student_name=None):
    '''
    Given certain known information, returns breadcrumbs context
    '''
    with SmarterDBConnection() as connector:
        dim_inst_hier = connector.get_table('dim_inst_hier')

        # Limit result count to one
        query = select([dim_inst_hier.c.state_name.label('state_name'),
                        dim_inst_hier.c.state_code.label('state_code'),
                        dim_inst_hier.c.district_name.label('district_name'),
                        dim_inst_hier.c.school_name.label('school_name')],
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
        result = results[0]

        # return an hierarchical ordered list
        formatted_results = []
        formatted_results.append({'type': 'state', 'name': result['state_name'], 'id': result['state_code']})
        if district_id is not None:
            formatted_results.append({'type': 'district', 'name': result['district_name'], 'id': district_id})
            if school_id is not None:
                formatted_results.append({'type': 'school', 'name': result['school_name'], 'id': school_id})
                if asmt_grade is not None:
                    formatted_results.append({'type': 'grade', 'name': asmt_grade})
                    if student_name is not None:
                        formatted_results.append({'type': 'student', 'name': student_name})

    return {'items': formatted_results}
