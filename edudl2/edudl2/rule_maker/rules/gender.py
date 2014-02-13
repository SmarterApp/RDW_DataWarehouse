'''
Created on May 29, 2013

@author: kallen
'''
from edudl2.rule_maker.makers.dataprep import __default_prep


__prepare = __default_prep
__canon = {'M': ['M', 'B'],
           'F': ['F', 'G'],
           'NS': ['NS', 'NOT_SPECIFIED', 'NOT SPECIFIED']
           }
