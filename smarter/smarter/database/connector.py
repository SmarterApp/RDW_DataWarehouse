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
    '''
    def __init__(self, datasource_name=None):
        if datasource_name is None:
            # Get user's tenant from session
            __user = authenticated_userid(get_current_request())
            if __user:
                datasource_name = get_datasource_name(__user.get_tenant())
            else:
                # TODO: have to fix this edge case
                pass
        super().__init__(name=datasource_name)
