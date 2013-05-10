'''
Created on May 9, 2013

@author: dip
'''
from smarter.security.roles.base import BaseRole
from smarter.security.context_role_map import ContextRoleMap


@ContextRoleMap.register(["default"])
class DefaultRole(BaseRole):

    def __init__(self, connector):
        super().__init__(connector)

    def get_context(self, guid):
        '''
        no-op
        '''
        pass
