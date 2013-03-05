'''
Created on Jan 29, 2013

@author: abrien, swimberly
'''

from uuid import uuid4
from helper_entities import Claim

from idgen import IdGen
from entities import Assessment
from constants import ASSMT_TYPES, MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, ASSMT_SCORE_YEARS

GRADES = [i for i in range(13)]
TYPES = ['SUMMATIVE', 'INTERIM']
PERIODS = ['BOY', 'MOY', 'EOY']
SUBJECTS = ['ELA', 'Math']
PERFORMANCE_LEVELS = ['Minimal Command', 'Partial Command', 'Sufficient Command', 'Deep Command']

NUM_ASSMT = len(GRADES) * len(TYPES) * len(PERIODS) * len(SUBJECTS)


def generate_dim_assessment():
    '''
    Entry point for generating assessments.
    Returns     : a list of assessment objects
    '''

    assessments = []

    for grade in GRADES:
        for atype in TYPES:
            if atype == 'INTERIM':
                for period in PERIODS:
                    for subject in SUBJECTS:
                        for year in ASSMT_SCORE_YEARS:
                            assessment = generate_single_asmt(grade, atype, period, subject, year)
                            assessments.append(assessment)
            else:  # not ITERMIN therefore SUMMATIVE
                for subject in SUBJECTS:
                    for year in ASSMT_SCORE_YEARS:
                        assessment = generate_single_asmt(grade, atype, 'EOY', subject, year)
                        assessments.append(assessment)

    return assessments


def generate_single_asmt(student_grade, asmt_type, period, subject, year):
    '''
    returns an Assessment object
    student_grade -- the student_grade for the current assessment
    asmt_type -- the type of assessment to generate either 'INTERIM' or 'SUMMATIVE'
    period -- the period of the assessment. 'BOY', 'MOY' or 'EOY'
    subject -- the subject of the assessment. 'Math' or 'ELA'
    '''

    asmt_id = generate_id()
    version = generate_version()
    asmt_grade = '4' if student_grade < 8 else '8'
    asmt_info = ASSMT_TYPES[subject][asmt_grade]

    claim1_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][0])
    claim2_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][1])
    claim3_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][2])

    claim1 = Claim(asmt_info['claim_names'][0], claim1_min_max[0], claim1_min_max[1])
    claim2 = Claim(asmt_info['claim_names'][1], claim2_min_max[0], claim2_min_max[1])
    claim3 = Claim(asmt_info['claim_names'][2], claim3_min_max[0], claim3_min_max[1])

    params = {
        'asmt_id': asmt_id,
        'asmt_external_id': uuid4(),
        'asmt_type': asmt_type,
        'asmt_period': period,
        'asmt_period_year': year,
        'asmt_version': version,
        'asmt_grade': student_grade,
        'asmt_subject': subject,
        'claim_1': claim1,
        'claim_2': claim2,
        'claim_3': claim3,
        'asmt_score_min': MIN_ASSMT_SCORE,
        'asmt_score_max': MAX_ASSMT_SCORE,
        'asmt_perf_lvl_name_1': PERFORMANCE_LEVELS[0],
        'asmt_perf_lvl_name_2': PERFORMANCE_LEVELS[1],
        'asmt_perf_lvl_name_3': PERFORMANCE_LEVELS[2],
        'asmt_perf_lvl_name_4': PERFORMANCE_LEVELS[3],
        'asmt_cut_point_1': int((MAX_ASSMT_SCORE + MIN_ASSMT_SCORE) * .25),
        'asmt_cut_point_2': int((MAX_ASSMT_SCORE + MIN_ASSMT_SCORE) * .5),
        'asmt_cut_point_3': int((MAX_ASSMT_SCORE + MIN_ASSMT_SCORE) * .75),

        'from_date': '20120901',
        'most_recent': True
    }

    if len(asmt_info['claim_names']) >= 4 and len(asmt_info['claim_percs']) >= 4:
        claim4_min_max = calc_claim_min_max(MIN_ASSMT_SCORE, MAX_ASSMT_SCORE, asmt_info['claim_percs'][3])
        claim4 = Claim(asmt_info['claim_names'][3], claim4_min_max[0], claim4_min_max[1])
        params['claim_4'] = claim4

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

'''
if __name__ == '__main__':
    assessments = generate_dim_assessment()

    for asmt in assessments:
        print(str(asmt))
'''
