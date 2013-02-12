'''
Created on Jan 29, 2013

@author: abrien, swimberly
'''

from uuid import uuid4

from idgen import IdGen
from entities import Assessment, Claim
from constants import ASSMT_TYPES, MIN_ASSMT_SCORE, MAX_ASSMT_SCORE

GRADES = [i for i in range(13)]
TYPES = ['SUMMATIVE', 'INTERIM']
PERIODS = ['BOY', 'MOY', 'EOY']
SUBJECTS = ['ELA', 'Math']
PERFORMANCE_LEVELS = ['Minimal Command', 'Partial Command', 'Sufficient Command', 'Deep Command']

NUM_ASSMT = len(GRADES) * len(TYPES) * len(PERIODS) * len(SUBJECTS)


def generate_assessment_types():
    '''
    Entry point for generating assessments.
    total       : Total number of assessments to generate
    Returns     : a list of assessment objects
    '''

    assessments = []

    for grade in GRADES:
        for atype in TYPES:
            if atype == 'INTERIM':
                for period in PERIODS:
                    for subject in SUBJECTS:
                        assessment = generate_single_asmt(grade, atype, period, subject)
                        assessments.append(assessment)
            else:
                for subject in SUBJECTS:
                    assessment = generate_single_asmt(grade, atype, 'EOY', subject)
                    assessments.append(assessment)

    return assessments


def generate_single_asmt(grade, asmt_type, period, subject):
    '''
    returns an Assessment object
    grade -- the grade for the current assessment
    asmt_type -- the type of assessment to generate either 'INTERIM' or 'SUMMATIVE'
    period -- the period of the assessment. 'BOY', 'MOY' or 'EOY'
    subject -- the subject of the assessment. 'Math' or 'ELA'
    '''

    asmt_id = generate_id()
    version = generate_version()
    asmt_gr = '4' if grade < 8 else '8'
    asmt_info = ASSMT_TYPES[subject][asmt_gr]

    claim1_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][0])
    claim2_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][1])
    claim3_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][2])
    claim4_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][3])

    claim1 = Claim(asmt_info['claim_names'][0], claim1_min_max[0], claim1_min_max[1])
    claim2 = Claim(asmt_info['claim_names'][1], claim2_min_max[0], claim2_min_max[1])
    claim3 = Claim(asmt_info['claim_names'][2], claim3_min_max[0], claim3_min_max[1])
    claim4 = Claim(asmt_info['claim_names'][3], claim4_min_max[0], claim4_min_max[1])
    #TODO: set assessment year
    params = {
        'asmt_id': asmt_id,
        'asmt_external_id': uuid4(),
        'asmt_type': asmt_type,
        'asmt_period': period,
        'asmt_period_year': 2012,
        'asmt_version': version,
        'asmt_grade': grade,
        'asmt_subject': subject,
        'claim_1': claim1,
        'claim_2': claim2,
        'claim_3': claim3,
        'claim_4': claim4,
        'asmt_score_min': MIN_ASSMT_SCORE,
        'asmt_score_max': MAX_ASSMT_SCORE,
        'asmt_perf_lvl_name_1': PERFORMANCE_LEVELS[0],
        'asmt_perf_lvl_name_2': PERFORMANCE_LEVELS[1],
        'asmt_perf_lvl_name_3': PERFORMANCE_LEVELS[2],
        'asmt_perf_lvl_name_4': PERFORMANCE_LEVELS[3],
        'asmt_cut_point_1': int((MAX_ASSMT_SCORE + MIN_ASSMT_SCORE) * .25),
        'asmt_cut_point_2': int((MAX_ASSMT_SCORE + MIN_ASSMT_SCORE) * .5),
        'asmt_cut_point_3': int((MAX_ASSMT_SCORE + MIN_ASSMT_SCORE) * .75)
    }

    return Assessment(**params)


def calc_claim_min_max(asmt_min, asmt_max, claim_perc):
    '''
    returns a minimum and maximum score for a claim given the minimum for the asmt and percentage
    that the claim makes up in the total score
    '''
    claim_min = asmt_min * (claim_perc * .01)
    claim_max = asmt_max * (claim_perc * .01)

    return int(claim_min), int(claim_max)


def generate_id():
    '''
    Generates a unique id by using the IdGen module
    '''

    id_generator = IdGen()
    return id_generator.get_id()


def generate_version():
    '''
    Method to return a version
    currently returns V1
    '''

    return 'V1'


ASSESSMENT_TYPES_LIST = generate_assessment_types()


if __name__ == '__main__':
    assessments = generate_assessment_types()

    for asmt in assessments:
        print(str(asmt))

    print('version2: ')
    for asmt in ASSESSMENT_TYPES_LIST:
        print(str(asmt))
