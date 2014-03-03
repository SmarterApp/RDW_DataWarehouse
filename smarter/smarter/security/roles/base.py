'''
Created on May 9, 2013

@author: dip
'''
from edapi.exceptions import ForbiddenError
from sqlalchemy.sql.expression import distinct, and_, select
from smarter.reports.helpers.constants import Constants


class BaseRole(object):
    '''
    Base Class Role
    '''
    def __init__(self, connector):
        self.connector = connector

    def get_context(self, tenant, user):
        pass

    def check_context(self, tenant, user, student_guids):
        pass

    def get_students(self, tenant, student_guids):
        '''
        Returns a query that gives a list of distinct student guids given that a list of student guids are supplied
        '''
        fact_asmt_outcome = self.connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select([distinct(fact_asmt_outcome.c.student_guid)],
                       from_obj=[fact_asmt_outcome])
        query = query.where(and_(fact_asmt_outcome.c.most_recent, fact_asmt_outcome.c.status == 'C', fact_asmt_outcome.c.student_guid.in_(student_guids)))
        return query


def verify_context(fn):
    '''
    Decorator used to validate that we throw Forbidden error when context is an empty list
    '''
    def wrapped(*args, **kwargs):
        context = fn(*args, **kwargs)
        if context is None:
            raise ForbiddenError
        return context
    return wrapped
