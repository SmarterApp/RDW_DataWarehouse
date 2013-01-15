'''
Created on Jan 10, 2013

@author: aoren
'''
import sys

#from edapi.utils.database_connections import getDatabaseConnection

def get_report_delegate(reportName):
    try:
        # TODO: move to util
        instance =  getattr(sys.modules[__name__], reportName);
    except AttributeError:
        raise 'Report Class: {0} is not found'.format(reportName)
    return instance.get_json(instance);
    
class ReportManager():
    
    @staticmethod
    def generate_report(reportName, params, repository):
        (obj,generate_report_method) = repository.get_report_delegate(reportName)
        return generate_report_method(obj, params)
    
    @staticmethod
    def generate_report_config(reportName, repository):
        return repository.get_report_config(reportName)
    
    
    
        