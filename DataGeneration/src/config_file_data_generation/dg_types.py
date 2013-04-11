'''
Created on Apr 4, 2013

@author: kallen
'''

GRADES = 'grades'
STUDENTS = 'students'
STATE_TYPE = 'state_type'
DISTRICT_TYPES_AND_COUNTS = 'district_types_and_counts'
SCHOOL_COUNTS = 'school_counts'
MIN = 'min'
AVG = 'avg'
MAX = 'max'
SCHOOL_TYPES_AND_RATIOS = 'school_types_and_ratios'
NAME = 'name'
STATE_CODE = 'state_code'


def get_school_types():
    school_types = { 'High School'      : {'grades' : [11],     'students' : {'min' : 100,  'max' : 500, 'avg' : 300}},
                    'Middle School'    : {'grades' : [6,7,8],  'students' : {'min' :  50,  'max' : 200, 'avg' : 150}},
                    'Elementary School': {'grades' : [3,4,5],  'students' : {'min' :  20,  'max' :  70, 'avg' :  60}}
                   }
    return school_types

def get_district_types():
    district_types = {'Big'      : { 'school_counts' : {'min' : 50, 'max' : 80, 'avg' : 65}, 'school_types_and_ratios' : {'High School' : 1, 'Middle School' : 2, 'Elementary School' : 5} },
                     'Medium'   : { 'school_counts' : {'min' : 20, 'max' : 24, 'avg' : 22}, 'school_types_and_ratios' : {'High School' : 1, 'Middle School' : 2, 'Elementary School' : 5} },
                     'Small'    : { 'school_counts' : {'min' :  2, 'max' :  8, 'avg' :  5}, 'school_types_and_ratios' : {'High School' : 1, 'Middle School' : 2, 'Elementary School' : 5} }
                     }
    return district_types

def get_state_types():
    state_types = {'Typical_1' : {'district_types_and_counts' : {'Big' : 2, 'Medium' : 6, 'Small' : 40}, 'subjects_and_percentages' : {'Math' : .9, 'ELA' : .9}}
                  }
    return state_types

def get_states():
    states = [ {'name' : 'New York', 'state_code' : 'NY', 'state_type' : 'Typical_1'}]
    return states