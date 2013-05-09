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

    def append_context(self, query, guid):
        '''
        Appends to WHERE cause of the query with student context
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = self.get_context(guid)
        return query.where(fact_asmt_outcome.c.student_guid.in_(context))

    @verify_context
    def get_context(self, guid):
        '''
        Returns student_guid
        '''
        context = []
        if guid is not None:
            dim_student = self.connector.get_table(Constants.DIM_STUDENT)
            context_query = select([dim_student.c.student_guid],
                                   from_obj=[dim_student], limit=1)
            context_query = context_query.where(dim_student.c.student_guid == guid)
            results = self.connector.get_result(context_query)
            if results:
                context.append(results[0][Constants.STUDENT_GUID])
        return context
