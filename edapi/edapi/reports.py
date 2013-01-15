'''
Created on Jan 10, 2013

@author: aoren
'''
import sys
from edapi.repository.report_config_repository import report_config,\
    ReportConfigRepository

#from edapi.utils.database_connections import getDatabaseConnection

def get_report_delegate(reportName):
    try:
        # TODO: move to util
        instance =  getattr(sys.modules[__name__], reportName);
    except AttributeError:
        raise 'Report Class: {0} is not found'.format(reportName)
    return instance.get_json(instance);

class TestReport():
    _query = 'test'
        
    @report_config(alias = "test", params = {
                                                "freeTextField": {
                                                    "validation" : {
                                                        "regex":"[A-Za-z0-9\-]"
                                                    }
                                                },
                                                "staticListField": {
                                                    "value" : ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"] 
                                                },
                                                "aliasField": {"alias" : "test2" } 
                                             })
    def generate(self, params):
        return (params) #todo: return data
    
    @report_config(alias = "test2", params = { "staticListField": {
                                                    "value" : ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"] 
                                                }
                                              })
    def generate_test2(self, params):
        return (params) 
    
class ReportManager():
    
    @staticmethod
    def generate_report(reportName, params, repository):
        (obj,generate_report_method) = repository.get_report_delegate(reportName)
        return generate_report_method(obj, params)
    
    @staticmethod
    def generate_report_config(reportName, repository):
        return repository.get_report_config(reportName)
    
    
    
        