'''
Created on Jan 15, 2013

@author: aoren
'''
from edapi.utils import report_config

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
                                                "aliasField": {"alias" : "test2" }, 
                                                "noConfigField": {"alias" : "no_config" } 
                                             })
    def generate(self, params):
        return params #todo: return data
    
    #this report requires configuration, and therefore should NOT get expanded automatically.
    @report_config(alias = "test2", params = { "staticListField": {
                                                    "value" : ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"] 
                                                }
                                              })
    def generate_test2(self, params):
        return params 
    
    #this report can get retrieved with no configuration, and therefore gets expanded automatically.
    @report_config(alias = "no_config")
    def generate_test_no_config(self, params):
        return ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"]
