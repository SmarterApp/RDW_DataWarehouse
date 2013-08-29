'''
Created on Aug 29, 2013

@author: dawu
'''
from edapi.decorators import user_info
from pyramid.view import view_config


@view_config(route_name='user_info', request_method='POST', renderer='json')
@user_info
def user_info_service(*args, **kwds):
    '''
    Returns current user information

    :param args: function to accept an arbitrary number of arguments.
    :param kwds: function to accept an arbitrary number of keyword arguments.
    '''
    return {}
