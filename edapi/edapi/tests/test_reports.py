'''
Created on Jan 15, 2013

@author: aoren
'''
from edapi.utils import report_config

class TestReport():
    _query = 'test'
        
    @report_config(name="test_report", params=
                                             {
                                                "free_text_field" : {
                                                                   "type" : "string",
                                                                   "pattern" : "^[a-z]$"
                                                                   },
                                                "numeric_field" : {
                                                                   "type" : "integer"
                                                                   },
                                                "optional_field" : {
                                                                   "type" : "integer",
                                                                   "required" : False
                                                                   },
                                                "school_sizes": {"type" : "integer", "name" : "school_size_report" },
                                                "student_lists": {"name" : "student_list_report" }
                                              }
                                            )
    def generate(self, params):
        return [ { "student_id": 1111, "first_name": 'William', "middle_name": 'Henry', "last_name": 'Gates', "asmt_subject": 'ELA', "asmt_period": '2012 MOY', "asmt_score": 198, 
                  "asmt_claim_1_score": 30, "asmt_claim_2_score": 40, "asmt_claim_3_score": 55, "asmt_claim_4_score": 73 } ] 
    
    # this report can get retrieved with no configuration, and therefore gets expanded automatically.
    @report_config(name="school_size_report")
    def generate_test_no_config(self, params):
        return ["100", "200", "1000"]
    
    # this report requires configuration, and therefore should NOT get expanded automatically.
    @report_config(name="student_list_report", params={ "scope": {
                                                    "value" : ["State", "Account", "School Group", "School", "Teacher", "Class", "Student", "Grade", "Race", "Custom Attribute"] 
                                                }
                                              })
    def generate_test2(self, params):
        if params['scope'].lower() == "school":
            return { "number_of_students" : "200" }
        else:
            return{ "number_of_students" : "1000" }
    

