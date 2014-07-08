from pyramid.view import notfound_view_config, view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPMovedPermanently
from pyramid.response import Response
import os
from pyramid.security import NO_PERMISSION_REQUIRED
__author__ = 'okrook'


def includeme(config):
    '''
    Routes to service endpoints
    '''

    # Add File Download end point
    config.add_route('download', '/download/{reg_id}')
    config.add_route('error', 'error')

    here = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.abspath(os.path.join(os.path.join(here, '..', '..'), 'assets'))
    config.add_static_view('assets/images', os.path.join(assets_dir, 'images'))


@view_config(route_name='error', renderer='../../assets/templates/hpz_error.pt')
def hpz_error(request):
    return {}
