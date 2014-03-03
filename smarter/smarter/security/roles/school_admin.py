'''
Created on May 9, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.base import BaseRole, verify_context


# Temp disable context security registration
#@ContextRoleMap.register([RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_1, RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_2])
class SchoolAdmin(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    @verify_context
    def get_context(self, tenant, user):
        '''
        Returns a sqlalchemy binary expression representing school_guid that user has context to
        If Context is an empty list, return none, which will return Forbidden Error
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        context = []
        expr = None
#        if guid:
#            dim_staff = self.connector.get_table(Constants.DIM_STAFF)
#            context_query = select([dim_staff.c.school_guid],
#                                   from_obj=[dim_staff])
#            context_query = context_query.where(and_(dim_staff.c.staff_guid == guid, dim_staff.c.most_recent))
#            results = self.connector.get_result(context_query)
#            for result in results:
#                context.append(result[Constants.SCHOOL_GUID])
        if context:
            expr = fact_asmt_outcome.c.school_guid.in_(context)
        return expr

    def check_context(self, tenant, user, student_guids):
        '''
        Returns true if school_admin has context to the list of student guids
        '''
        query = super().get_students(student_guids)
        query = query.where(self.get_context(user))

        results = self.connector.get_result(query)

        return len(student_guids) == len(results)
