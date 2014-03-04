'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.default import BaseRole
from smarter.security.roles.base import verify_context
from smarter.security.context_role_map import ContextRoleMap
from smarter.security.constants import RolesConstants


@ContextRoleMap.register([RolesConstants.TEACHER])
class Teacher(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    @verify_context
    def get_context(self, tenant, user):
        '''
        Returns a sqlalchemy binary expression representing section_guid that user has context to
        If Context is an empty list, return none, which will return Forbidden Error
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = user.get_context().get_schools(tenant, RolesConstants.TEACHER)
        expr = None
        if context:
            expr = fact_asmt_outcome.c.school_guid.in_(context)
        return expr

    def check_context(self, tenant, user, student_guids):
        '''
        Given a list of student guids, return true if user guid has access to those students
        '''
        query = super().get_students(tenant, student_guids)
        query = query.where(self.get_context(tenant, user))

        results = self.connector.get_result(query)

        return len(student_guids) == len(results)
