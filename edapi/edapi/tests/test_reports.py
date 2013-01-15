'''
Created on Jan 15, 2013

@author: aoren
'''
from edapi.repository.report_config_repository import report_config

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