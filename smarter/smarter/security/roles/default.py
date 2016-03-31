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
from smarter.security.roles.base import BaseRole
from smarter.security.context_role_map import ContextRoleMap


@ContextRoleMap.register(["default"])
class DefaultRole(BaseRole):
    '''
    Default role is used when a role doesn't have custom context security rule
    '''

    def __init__(self, connector, name):
        super().__init__(connector, name)

    def check_context(self, tenant, user, student_ids):
        '''
        Has Context to resource
        '''
        return True

    def add_context(self, tenant, user, query):
        '''
        noop
        '''
        pass
