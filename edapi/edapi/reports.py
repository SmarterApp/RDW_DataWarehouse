'''
Created on Jan 10, 2013

@author: aoren
'''
import sys
from edapi.repository.report_config_repository import report_config

#from edapi.utils.database_connections import getDatabaseConnection

def get_report(reportName):
    try:
        # TODO: move to util
        instance =  getattr(sys.modules[__name__], reportName);
    except AttributeError:
        raise 'Report Class: {0} is not found'.format(reportName)
    return instance.get_json(instance);
    
#class BaseReport:
#    _query = ''
#    _reportConfig = None
#    
#    def validate(self, params):
#        return True
#    
#    def generate(self, params):
#        raise NotImplementedError( "Should have implemented this")

class TestReport():
    _query = 'test'
        
    @report_config(alias = "test", params = {"adam" : 1})
    def generate(self, params):
        return  (params) #todo: return data
