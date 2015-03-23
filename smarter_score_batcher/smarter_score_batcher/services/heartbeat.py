'''
Created on Jan 21, 2015

'''
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPServerError
from smarter_score_batcher.tasks import health_check
import pyramid.threadlocal
from sqlalchemy.sql.expression import select
from smarter_score_batcher.database.tsb_connector import TSBDBConnection


@view_config(route_name='heartbeat', permission=NO_PERMISSION_REQUIRED, request_method='GET')
def heartbeat(request):
    '''
    service end point for heartbeat
    '''
    results = [check_celery(request), check_datasource()]
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
        queue = pyramid.threadlocal.get_current_registry().settings.get('smarter_score_batcher.health_check.job.queue')
        timeout = float(pyramid.threadlocal.get_current_registry().settings.get('smarter_score_batcher.celery_timeout'))
    else:
        queue = 'health_check'
        timeout = 10.0
    try:
        celery_response = health_check.apply_async(queue=queue)
        heartbeat_message = celery_response.get(timeout=timeout)
    except Exception as e:
        return HTTPServerError()

    if heartbeat_message[0:9] == 'heartbeat':
        return HTTPOk()
    else:
        return HTTPServerError()


def check_datasource():
    '''
    GET request that executes a Select 1 and returns status of 200 if database returns results

    :param request:  Pyramid request object
    '''
    try:
        results = None
        with TSBDBConnection() as connector:
            query = select([1])
            results = connector.get_result(query)
    except Exception:
        results = None

    if results and len(results) > 0:
        return HTTPOk()
    return HTTPServerError()
