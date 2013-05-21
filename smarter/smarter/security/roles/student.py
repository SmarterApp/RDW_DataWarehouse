'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from smarter.security.constants import RolesConstants
from smarter.security.roles.base import BaseRole, verify_context
from smarter.security.context_role_map import ContextRoleMap


@ContextRoleMap.register([RolesConstants.STUDENT])
class Student(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    @verify_context
    def get_context(self, guid):
        '''
        Returns a sqlalchemy binary expression representing student_guid that user has context to
        If Context is an empty list, return none, which will return Forbidden Error
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        return (fact_asmt_outcome.c.student_guid == guid)

    def check_context(self, guid, student_guids):
        '''
        Given a list of student guids, return true if user guid is in the list
        '''
        for student_guid in student_guids:
            if not guid == student_guid:
                return False
        return True
