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
Created on Aug 29, 2013

@author: dawu
'''
from edapi.decorators import user_info
from pyramid.view import view_config
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context


@view_config(route_name='user_info', request_method='POST', renderer='json')
@user_info
def user_info_service(*args, **kwds):
    '''
    Returns current user information

    :param args: function to accept an arbitrary number of arguments.
    :param kwds: function to accept an arbitrary number of keyword arguments.
    '''
    context = get_breadcrumbs_context()
    return {'context': context}
