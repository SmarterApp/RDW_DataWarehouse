'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import select
from smarter.security.context_factory import ContextFactory
from smarter.security.constants import RolesConstants


@ContextFactory.register(RolesConstants.STUDENT)
def append_student_context(connector, query, guid):
        '''
        Appends to WHERE cause of the query with student context
        '''
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = get_student_context(connector, guid)
        return query.where(fact_asmt_outcome.c.student_guid.in_(context))


def get_student_context(connector, guid):
    '''
    Returns student_guid
    '''
    context = []
    if guid is not None:
        dim_student = connector.get_table(Constants.DIM_STUDENT)
        context_query = select([dim_student.c.student_guid],
                               from_obj=[dim_student], limit=1)
        context_query = context_query.where(dim_student.c.student_guid == guid)
        results = connector.get_result(context_query)
        if results:
            context.append(results[0][Constants.STUDENT_GUID])
    return context
