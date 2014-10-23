'''
Created on May 9, 2013

@author: dip
'''
from edapi.exceptions import ForbiddenError
from sqlalchemy.sql.expression import distinct, and_, select
from smarter.reports.helpers.constants import Constants
from edschema.metadata.util import get_selectable_by_table_name


class BaseRole(object):
    '''
    Base Class Role
    '''
    def __init__(self, connector, name):
        self.connector = connector
        self.name = name

    def get_context(self, tenant, user):
        pass

    def add_context(self, tenant, user, query):
        pass

    def check_context(self, tenant, user, student_ids):
        return False

    def get_students(self, tenant, student_ids):
        '''
        Returns a query that gives a list of distinct student guids given that a list of student guids are supplied
        '''
        fact_asmt_outcome_vw = self.connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        query = select([distinct(fact_asmt_outcome_vw.c.student_id)],
                       from_obj=[fact_asmt_outcome_vw])
        query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT, fact_asmt_outcome_vw.c.student_id.in_(student_ids)))
        return query

    def get_context_tables(self, query):
        '''
        Get a list of context tables from the query
        '''
        return {obj for (obj, name) in get_selectable_by_table_name(query).items() if name in (Constants.STUDENT_REG, Constants.FACT_ASMT_OUTCOME_VW, Constants.FACT_BLOCK_ASMT_OUTCOME)}


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
