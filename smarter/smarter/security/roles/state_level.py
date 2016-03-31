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
from sqlalchemy.sql.expression import or_
from smarter.security.roles.base import BaseRole, verify_context
from smarter.security.context_role_map import ContextRoleMap
from smarter_common.security.constants import RolesConstants


# Access is bound to state level
@ContextRoleMap.register([RolesConstants.SRS_EXTRACTS, RolesConstants.SRC_EXTRACTS, RolesConstants.AUDIT_XML_EXTRACTS, RolesConstants.ITEM_LEVEL_EXTRACTS])
class StateLevel(BaseRole):

    def __init__(self, connector, name):
        super().__init__(connector, name)

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
        return super().check_context(tenant, user, student_ids)
