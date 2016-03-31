# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
    config.add_route('file_download', '/file/{reg_id}')
    config.add_route('error', 'error')
    config.add_route('validate', '/validate/{reg_id}')
    config.add_route('web_download', '/download/{reg_id}')

    here = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.abspath(os.path.join(os.path.join(here, '..', '..'), 'assets'))
    config.add_static_view('assets/images', os.path.join(assets_dir, 'images'))
    config.add_static_view('js', os.path.join(assets_dir, 'js'))


@view_config(route_name='error', renderer='../../assets/templates/hpz_error.pt')
def hpz_error(request):
    return {}
