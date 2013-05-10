'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import and_, select
from smarter.security.constants import RolesConstants
from smarter.security.roles.default import BaseRole
from smarter.security.context_role_map import ContextRoleMap
from smarter.security.roles.base import verify_context


@ContextRoleMap.register([RolesConstants.TEACHER])
class Teacher(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    @verify_context
    def get_context(self, guid):
        '''
        Returns a sqlalchemy binary expression representing section_guid that user has context to
        If Context is an empty list, return none, which will return Forbidden Error
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = []
        expr = None
        if guid:
            dim_staff = self.connector.get_table(Constants.DIM_STAFF)
            context_query = select([dim_staff.c.section_guid],
                                   from_obj=[dim_staff])
            context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
            results = self.connector.get_result(context_query)
            for result in results:
                context.append(result[Constants.SECTION_GUID])
        if context:
            expr = fact_asmt_outcome.c.section_guid.in_(context)
        return expr
