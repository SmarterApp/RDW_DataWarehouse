'''
Created on Apr 17, 2013

@author: dip
'''
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPServerError
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import select
from smarter.database import get_data_source_names


@view_config(route_name='heartbeat', permission=NO_PERMISSION_REQUIRED, request_method='GET')
def heartbeat(request):
    '''
    Returns 200 when we get results from db
    '''
    try:
        results = None
        for datasource_name in get_data_source_names():
            with SmarterDBConnection(name=datasource_name) as connector:
                query = select([1])
                results = connector.get_result(query)
    except Exception:
        results = None

    if results and len(results) > 0:
        return HTTPOk()
    return HTTPServerError()
