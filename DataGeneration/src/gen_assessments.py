'''
Created on Jan 29, 2013

@author: abrien
'''

from idgen import IdGen
from random import randint
from entities import AssessmentType

GRADES = [i for i in range(13)]
TYPES = ['SUMMATIVE', 'INTERIM']
PERIODS = ['BOY', 'MOY', 'EOY']
SUBJECTS = ['ELA', 'MATH']

NUM_ASSMT = len(GRADES) * len(TYPES) * len(PERIODS) * len(SUBJECTS)


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
                for subject in SUBJECTS:
                    id = generate_id()
                    version = generate_version()
                    asmt_type = AssessmentType(id, subject, type, period, version, grade)
                    assessments.append(asmt_type)

    return assessments


def generate_id():
    id_generator = IdGen()
    id = id_generator.get_id()
    return id


def generate_version():
    return 'V1'


ASSESSMENT_TYPES_LIST = [AssessmentType(generate_id(), sub, ty, per, generate_version(), gr) for gr in GRADES for ty in TYPES for per in PERIODS for sub in SUBJECTS]

if __name__ == '__main__':
    assessments = generate_assessment_types()

    for asmt in assessments:
        print(str(asmt))

    print('version2: ')
    for asmt in ASSESSMENT_TYPES_LIST:
        print(str(asmt))
