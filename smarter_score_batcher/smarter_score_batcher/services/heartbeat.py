# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

'''
Created on Jan 21, 2015

'''
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPServerError
from smarter_score_batcher.tasks.health_check import health_check
import pyramid.threadlocal
from pyramid.httpexceptions import HTTPOk
import logging


logger = logging.getLogger('smarter_score_batcher')


@view_config(route_name='heartbeat', permission=NO_PERMISSION_REQUIRED, request_method='GET')
def heartbeat(request):
    '''
    service end point for heartbeat
    '''
    try:
        check_celery(request)
    except Exception as e:
        logger.error("TSB Heartbeat failed. Check TSB worker. %s", str(e))
        return HTTPServerError()
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

    celery_response = health_check.apply_async(queue=queue)
    heartbeat_message = celery_response.get(timeout=timeout)

    if heartbeat_message[0:9] != 'heartbeat':
        raise Exception('TSB Heartbeat Exception. Check TSB worker.')
    return HTTPOk()
