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
from sqlalchemy.sql.expression import and_, or_
from smarter.security.roles.default import BaseRole
from smarter.security.roles.base import verify_context
from smarter.security.context_role_map import ContextRoleMap
from smarter_common.security.constants import RolesConstants


# PII and SAR Extracts have the same context
@ContextRoleMap.register([RolesConstants.PII, RolesConstants.SAR_EXTRACTS])
class PII(BaseRole):

    def __init__(self, connector, name):
        super().__init__(connector, name)

    @verify_context
    def add_context(self, tenant, user, query):
        '''
        Updates a query adding context
        If Context is an empty list, return None, which will return Forbidden Error
        '''
        context = user.get_context().get_all_context(tenant, self.name)
        if not context:
            # context returned is empty, therefore no context
            return None
        expr = []
        for k, v in context.items():
            if v:
                expr.append(*[table.c[k].in_(v) for table in self.get_context_tables(query)])
        return query.where(and_(or_(*expr)))

    def check_context(self, tenant, user, student_ids):
        '''
        Given a list of student guids, return true if user guid has access to those students
        '''
        return super().check_context(tenant, user, student_ids)
