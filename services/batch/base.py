'''
Created on Jun 19, 2013

@author: dip
'''
from edauth.security.batch_user_session import create_batch_user_session


class BatchBase(object):
    '''
    A base class for batch processes
    '''

    def __init__(self, settings, tenant):
        '''
        :param settings:  a python dict containing configurations
        :param string tenant:  name of the tenant used to send batch processes
        '''
        self.settings = settings
        self.tenant = tenant

        self.__init_cookie()

    def __init_cookie(self):
        '''
        Creates a cookie for accessing smarter application
        '''
        # get current session cookie and request for pdf
        roles = ['SUPER_USER', 'PII']
        (self.cookie_name, self.cookie_value) = create_batch_user_session(self.settings, roles, self.tenant)
