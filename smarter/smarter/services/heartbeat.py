'''
Created on Apr 17, 2013

@author: dip
'''
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPServerError
from sqlalchemy.sql.expression import select
from database.connector import DBConnection
from services.tasks import health_check
import pyramid.threadlocal
from edcore.database import get_data_source_names


@view_config(route_name='heartbeat', permission=NO_PERMISSION_REQUIRED, request_method='GET')
def heartbeat(request):
    check_list = [check_datasource, check_celery]
    results = [check_task(request) for check_task in check_list]
    results = map(lambda x: isinstance(x, HTTPServerError().__class__), results)
    if True in results:
        return HTTPServerError()
    else:
        return HTTPOk()


def check_celery(request):
    '''
    GET request that executes a task via celery and retrieve result to verify celery service
    is functioning

    :param request:  Pyramid request object
    '''
    if pyramid.threadlocal.get_current_registry().settings is not None:
        queue = pyramid.threadlocal.get_current_registry().settings.get('pdf.health_check.job.queue')
        timeout = pyramid.threadlocal.get_current_registry().settings.get('pdf.celery_timeout')
    else:
        queue = 'health_check'
        timeout = 10
    try:
        celery_response = health_check.apply_async(queue=queue)
        heartbeat_message = celery_response.get(timeout=timeout)
    except Exception:
        return HTTPServerError()

    if heartbeat_message[0:9] == 'heartbeat':
        return HTTPOk()
    else:
        return HTTPServerError()


def check_datasource(request):
    '''
    GET request that executes a Select 1 and returns status of 200 if database returns results

    :param request:  Pyramid request object
    '''
    try:
        results = None
        for datasource_name in get_data_source_names():
            with DBConnection(name=datasource_name) as connector:
                query = select([1])
                results = connector.get_result(query)
    except Exception:
        results = None

    if results and len(results) > 0:
        return HTTPOk()
    return HTTPServerError()
