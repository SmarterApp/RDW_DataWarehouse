# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
