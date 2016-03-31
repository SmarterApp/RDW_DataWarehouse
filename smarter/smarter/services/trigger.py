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
Created on Jun 27, 2013

@author: dip
'''
from pyramid.view import view_config
from smarter.trigger.pre_pdf_generator import prepdf_task
from smarter.trigger.pre_cache_generator import precached_task
from edapi.httpexceptions import EdApiHTTPNotFound


@view_config(route_name='trigger', request_method='GET', renderer='json', permission='super_admin_rights')
def trigger(request):
    '''
    Request for on demand batch generation for pdf and recache

    :param request:  Pyramid request object
    '''
    trigger_name = request.matchdict['trigger_type']
    if trigger_name == 'pdf':
        prepdf_task(request.registry.settings)
    elif trigger_name == 'cache':
        precached_task(request.registry.settings)
    else:
        msg = '%s is not defined as a trigger' % trigger_name
        return EdApiHTTPNotFound(msg)
    return {'result': 'OK'}
