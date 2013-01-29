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


def generate_assessments():
    '''
    Entry point for generating assessments.
    total       : Total number of assessments to generate
    Returns     : a list of assessment objects
    '''

    assessments = []

    for grade in GRADES:
        for type in TYPES:
            for per in PERIODS:
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
        ela_subjects = ['Comprehension', 'Composition', 'Grammar']
        rand = randint(0,2)
        return ela_subjects[rand]
    else:
        math_subjects =
        rand = randint(0,2)
        return math_subjects[rand]

def generate_type():
    rand = randint(0,1)
    if rand:
        return('ELA')
    else:
        return('MATH')

def generate_period():
    periods = ['BOY', 'MOY', 'EOY']
    rand_period_ind = randint(0,2)
    period = periods[rand_period_ind]

    years = ['2010', '2011', '2012']
    rand_year_ind = randint(0,2)
    year = years[rand_year_ind]

    return period + ' ' + year

def generate_version():
    return 'V1'

def generate_grade():
    return randint(0,13)

if __name__ == '__main__':
    assessments = generate_assessments(20)

    for asmt in assessments:
        print(str(asmt))