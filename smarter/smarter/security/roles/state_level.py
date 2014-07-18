'''
Created on May 9, 2013

@author: dip
'''
from sqlalchemy.sql.expression import or_

from smarter.reports.helpers.constants import Constants
from smarter.security.roles.base import BaseRole, verify_context
from smarter.security.context_role_map import ContextRoleMap
from smarter_common.security.constants import RolesConstants


# Access is bound to state level
@ContextRoleMap.register([RolesConstants.SRS_EXTRACTS, RolesConstants.SRC_EXTRACTS, RolesConstants.AUDIT_XML_EXTRACTS, RolesConstants.ITEM_LEVEL_EXTRACTS])
class StateLevel(BaseRole):

    def __init__(self, connector, name):
        super().__init__(connector, name)

    @verify_context
    def get_context(self, tenant, user):
        '''
        Returns a sqlalchemy binary expression representing state_code that user has context to
        '''
        student_reg = self.connector.get_table(Constants.STUDENT_REG)
        context = user.get_context().get_states(tenant, self.name)
        # context of none means that user has no access
        if context is None:
            return None
        else:
            return [student_reg.c.state_code.in_(context)] if context else []

    @verify_context
    def add_context(self, tenant, user, query):
        '''
        Updates a query adding context.  Tenant level context returns an empty set.
        In that case, we don't need to append any where clauses
        '''
        context = user.get_context().get_states(tenant, self.name)
        # context can be None, an empty set, or non-empty set
        if context is None:
            query = None
        elif context:
            query = query.where(or_(*[table.columns.state_code.in_(context) for table in self.get_context_tables(query)]))
        return query

    def check_context(self, tenant, user, student_ids):
        '''
        Returns true if it has context to the list of student guids
        '''
        query = super().get_students(tenant, student_ids)
        query = query.where(or_(*self.get_context(tenant, user)))
        results = self.connector.get_result(query)
        return len(student_ids) == len(results)
