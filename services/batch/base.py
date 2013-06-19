'''
Created on Jun 19, 2013

@author: dip
'''
from edauth.security.batch_user_session import create_batch_user_session


class BatchBase(object):

    def __init__(self, settings, tenant):
        self.settings = settings
        self.tenant = tenant

        self.__init_cookie()

    def __init_cookie(self):
        '''
        Creates cookie for accessing smarter application
        '''
        # get current session cookie and request for pdf
        roles = ['SUPER_USER']
        (self.cookie_name, self.cookie_value) = create_batch_user_session(self.settings, roles, self.tenant)
