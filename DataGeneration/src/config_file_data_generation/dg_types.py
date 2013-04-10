'''
Created on Apr 4, 2013

@author: kallen
'''

GRADES = 'grades'
STUDENTS = 'students'
STATE_TYPE = 'stateType'
DISTRICT_TYPES_AND_COUNTS = 'districtTypesAndCounts'
SCHOOL_COUNTS = 'school_counts'
MIN = 'min'
AVG = 'avg'
MAX = 'max'
SCHOOL_TYPES_AND_RATIOS = 'schoolTypesAndRatios'
NAME = 'name'
STATE_CODE = 'state_code'


def get_school_types():
    school_types = { 'High'      : {'grades' : [11],     'students' : {'min' : 100,  'max' : 500, 'avg' : 300}},
                    'Middle'    : {'grades' : [6,7,8],  'students' : {'min' :  50,  'max' : 200, 'avg' : 150}},
                    'Elementary': {'grades' : [3,4,5],  'students' : {'min' :  20,  'max' :  70, 'avg' :  60}}
                   }
    return school_types

def get_district_types():
    district_types = {'Big'      : { 'school_counts' : {'min' : 50, 'max' : 80, 'avg' : 65}, 'schoolTypesAndRatios' : {'High' : 1, 'Middle' : 2, 'Elementary' : 5} },
                     'Medium'   : { 'school_counts' : {'min' : 20, 'max' : 24, 'avg' : 22}, 'schoolTypesAndRatios' : {'High' : 1, 'Middle' : 2, 'Elementary' : 5} },
                     'Small'    : { 'school_counts' : {'min' :  2, 'max' :  8, 'avg' :  5}, 'schoolTypesAndRatios' : {'High' : 1, 'Middle' : 2, 'Elementary' : 5} }
                     }
    return district_types

def get_state_types():
    state_types = {'Typical1' : {'districtTypesAndCounts' : {'Big' : 2, 'Medium' : 6, 'Small' : 40}, 'subjectsAndPercentages' : {'Math' : .9, 'ELA' : .9}}
                  }
    return state_types

def get_states():
    states = [ {'name' : 'New York', 'state_code' : 'NY', 'state_type' : 'Typical1'}]
    return states