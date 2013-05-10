'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import select
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
        context = []
        expr = None
        if guid:
            dim_student = self.connector.get_table(Constants.DIM_STUDENT)
            context_query = select([dim_student.c.student_guid],
                                   from_obj=[dim_student], limit=1)
            context_query = context_query.where(dim_student.c.student_guid == guid)
            results = self.connector.get_result(context_query)
            if results:
                context.append(results[0][Constants.STUDENT_GUID])

        if context:
            expr = fact_asmt_outcome.c.student_guid.in_(context)
        return expr
