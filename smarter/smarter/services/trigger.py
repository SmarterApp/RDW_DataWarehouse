'''
Created on Jun 27, 2013

@author: dip
'''
from pyramid.view import view_config
from smarter.trigger.pre_pdf_generator import prepdf_task
from smarter.trigger.pre_cache_generator import precached_task
from edapi.httpexceptions import EdApiHTTPNotFound


# TODO
# @view_config(route_name='trigger', request_method='GET', renderer='json', permission='super_admin_rights')
@view_config(route_name='trigger', request_method='GET', renderer='json')
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
