'''
Created on Jan 18, 2013

@author: dip
'''

class DummyRequest:
    '''
    Mimics an incoming request
    '''
    registry = {}
    matchdict = {}
    content_type = ''
    GET = {}
    json_body = {}
    
    def reset(self):
        self.registry = {}
        self.matchdict = {}
        self.content_type = ''
        self.GET = {}
        self.json_body = {}

class DummyValidator:
    '''
    Mimics Validator class
    '''
    def __init__(self, validated = True):
        self._validated = validated
        
    def validate_params_schema(self, registry, report_name, params):
        return (self._validated, None)
    
    def fix_types(self, registry, report_name, params):
        return params

class Dummy:
    def some_func(self, params):
        return { "report" : params}
    def some_func_that_returns(self, params):
        return {"report" : "123" }