'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import and_, select
from smarter.security.constants import RolesConstants
from smarter.security.roles.default import BaseRole
from smarter.security.context_role_map import ContextRoleMap


@ContextRoleMap.register([RolesConstants.TEACHER])
class Teacher(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    def append_context(self, query, guid):
        '''
        Appends to WHERE cause of the query with teacher context
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = self.get_context(guid)
        return query.where(fact_asmt_outcome.c.section_guid.in_(context))

    def get_context(self, guid):
        '''
        Returns all the sections that the teacher is associated to
        '''
        context = []
        if guid is not None:
            dim_staff = self.connector.get_table(Constants.DIM_STAFF)
            context_query = select([dim_staff.c.section_guid],
                                   from_obj=[dim_staff])
            context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
            results = self.connector.get_result(context_query)
            for result in results:
                context.append(result[Constants.SECTION_GUID])
        return context
