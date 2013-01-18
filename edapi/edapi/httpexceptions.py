'''
Created on Jan 18, 2013

@author: dip
'''
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed
import json

class EdApiHTTPNotFound(HTTPNotFound):
    '''
    a custom http exception return when resource not found
    '''
    #code = 404
    #title = 'Requested report not found'
    #explanation = ('The resource could not be found.')
    
    def __init__(self, msg):
        super().__init__(text = json.dumps({'error': msg}), content_type = "application/json")
        
class EdApiHTTPPreconditionFailed(HTTPPreconditionFailed):
    '''
    a custom http exception when precondition is not met
    '''
    #code = 412
    #title = 'Parameter validation failed'
    #xplanation = ('Request precondition failed.')
    
    def __init__(self, msg):
        super().__init__(text = json.dumps({'error': msg}), content_type = "application/json")