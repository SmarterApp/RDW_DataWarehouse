'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import select, and_
from smarter.security.constants import RolesConstants
from smarter.security.roles.base import BaseRole, verify_context
from smarter.security.context_role_map import ContextRoleMap


@ContextRoleMap.register([RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_1, RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_2])
class SchoolAdmin(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    def append_context(self, query, guid):
        '''
        Appends to WHERE cause of the query with school admin context
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = self.get_context(guid)
        return query.where(fact_asmt_outcome.c.school_guid.in_(context))

    @verify_context
    def get_context(self, guid):
        '''
        Returns all school_guid that admin is associated to
        '''
        context = []
        if guid is not None:
            dim_staff = self.connector.get_table(Constants.DIM_STAFF)
            context_query = select([dim_staff.c.school_guid],
                                   from_obj=[dim_staff])
            context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
            results = self.connector.get_result(context_query)
            for result in results:
                context.append(result[Constants.SCHOOL_GUID])
        return context
