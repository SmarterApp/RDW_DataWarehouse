'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import select, and_
from smarter.security.context_factory import ContextFactory
from smarter.security.constants import RolesConstants


@ContextFactory.register(RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_1)
@ContextFactory.register(RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_2)
def append_school_admin_context(connector, query, guid):
    '''
    Appends to WHERE cause of the query with school admin context
    '''
    fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
    context = get_school_admin_context(connector, guid)
    return query.where(fact_asmt_outcome.c.school_guid.in_(context))


def get_school_admin_context(connector, guid):
    '''
    Returns all school_guid that admin is associated to
    '''
    context = []
    if guid is not None:
        dim_staff = connector.get_table(Constants.DIM_STAFF)
        context_query = select([dim_staff.c.school_guid],
                               from_obj=[dim_staff])
        context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
        results = connector.get_result(context_query)
        for result in results:
            context.append(result[Constants.SCHOOL_GUID])
    return context
