'''
Created on Jan 15, 2013

@author: aoren
'''
from edapi.utils import report_config

class TestReport():
    _query = 'test'
        
    @report_config(name="test_report", params=
                                             {
                                                "freeTextField" : {
                                                                   "type" : "string"
                                                                   },
                                                "staticListField": {
                                                                    "value" : ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"] 
                                                                    },
                                                "school_size": {"alias" : "school_size" } 
                                              }
                                            )
    def generate(self, params):
        return params  # todo: return data
    
    # this report requires configuration, and therefore should NOT get expanded automatically.
    @report_config(name="district_report_report", params={ "staticListField": {
                                                    "value" : ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"] 
                                                }
                                              })
    def generate_test2(self, params):
        return params 
    
    # this report can get retrieved with no configuration, and therefore gets expanded automatically.
    @report_config(name="school_size_report")
    def generate_test_no_config(self, params):
        return ["100", "200", "1000"]
