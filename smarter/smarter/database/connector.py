'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection
from smarter.database.datasource import get_datasource_name
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request


class SmarterDBConnection(DBConnection):
    '''
    DBConnector for Smarter Project
    a name is required for tenancy database connection lookup
    '''
    def __init__(self, name=None):

        if name is None:
            # Get user's tenant from session
            __user = authenticated_userid(get_current_request())
            if __user:
                name = get_datasource_name(__user.get_tenant())
            else:
                # TODO: have to fix this edge case
                pass
        super().__init__(name=name)
