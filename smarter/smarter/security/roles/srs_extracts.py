'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.base import BaseRole, verify_context
from smarter.security.context_role_map import ContextRoleMap
from smarter.security.constants import RolesConstants
from sqlalchemy.sql.expression import or_


@ContextRoleMap.register([RolesConstants.SRS_EXTRACTS])
class SRSExtracts(BaseRole):

    def __init__(self, connector, name):
        super().__init__(connector, name)

    @verify_context
    def get_context(self, tenant, user):
        '''
        Returns a sqlalchemy binary expression representing school_guid that user has context to
        If Context is an empty list, return none, which will return Forbidden Error
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = user.get_context().get_states(tenant, self.name)
        expr = []
        if context:
            expr.append(fact_asmt_outcome.c.state_code.in_(context))
        return expr

    def check_context(self, tenant, user, student_guids):
        '''
        Returns true if it has context to the list of student guids
        '''
        query = super().get_students(tenant, student_guids)
        query = query.where(or_(*self.get_context(tenant, user)))
        results = self.connector.get_result(query)
        return len(student_guids) == len(results)
