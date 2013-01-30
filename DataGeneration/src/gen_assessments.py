'''
Created on Jan 29, 2013

@author: abrien
'''

from idgen import IdGen
from random import randint
from entities import Assessment

GRADES = [i for i in range(13)]
TYPES = ['ELA', 'MATH']
PERIODS = ['BOY', 'MOY', 'EOY']
ELA_SUBJECTS = ['Comprehension', 'Composition', 'Grammar']
MATH_SUBJECTS = ['Geometry', 'Algebra', 'Statistics']


def generate_assessment_types():
    '''
    Entry point for generating assessments.
    total       : Total number of assessments to generate
    Returns     : a list of assessment objects
    '''

    assessments = []

    for grade in GRADES:
        for type in TYPES:
            for period in PERIODS:
                id = generate_id()
                subject = generate_subject(type)
                version = generate_version()
                asmt = Assessment(id, subject, type, period, version, grade)
                assessments.append(asmt)

    return assessments

def generate_id():
    id_generator = IdGen()
    id = id_generator.get_id()
    return id

def generate_subject(type):
    if type == 'ELA':
        rand = randint(0,len(ELA_SUBJECTS)-1)
        return ELA_SUBJECTS[rand]
    else:
        rand = randint(0,len(MATH_SUBJECTS)-1)
        return MATH_SUBJECTS[rand]

def generate_version():
    return 'V1'

if __name__ == '__main__':
    assessments = generate_assessment_types()

    for asmt in assessments:
        print(str(asmt))