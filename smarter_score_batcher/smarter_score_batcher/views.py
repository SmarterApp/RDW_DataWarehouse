'''
Created on Jul 15, 2014

@author: agrebneva
'''
from pyramid.view import view_config
from pyramid.response import Response
from smarter_score_batcher.processors import process_tdsreport


@view_config(route_name='xml_catcher', renderer='json', request_method='POST')
def xml_catcher(request):
    '''
    XML cacther service expects XML post and will delegate processing based on the root element
    '''
    process_tdsreport(request.body)
    Response('OK')
#     try:
#
#     except _:
#         return NotFound
#     return OK
