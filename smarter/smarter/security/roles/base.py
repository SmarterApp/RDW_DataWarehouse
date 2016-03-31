# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

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

    def add_context(self, tenant, user, query):
        return query

    def check_context(self, tenant, user, student_ids):
        '''
        Given a query, check for context
        '''
        queries = self.get_students(tenant, student_ids)
        for query in queries:
            query = self.add_context(tenant, user, query)
            results = self.connector.get_result(query)
            if len(student_ids) == len(results):
                return True
        return False

    def get_students(self, tenant, student_ids):
        '''
        Returns a query that gives a list of distinct student guids given that a list of student guids are supplied
        '''
        queries = []
        for fact_table_name in [Constants.FACT_ASMT_OUTCOME_VW, Constants.FACT_BLOCK_ASMT_OUTCOME]:
            fact_table = self.connector.get_table(fact_table_name)
            query = select([distinct(fact_table.c.student_id)],
                           from_obj=[fact_table])
            query = query.where(and_(fact_table.c.rec_status == Constants.CURRENT, fact_table.c.student_id.in_(student_ids)))
            queries.append(query)
        return queries

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
