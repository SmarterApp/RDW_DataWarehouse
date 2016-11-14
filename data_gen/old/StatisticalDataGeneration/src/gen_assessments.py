'''
Created on Jan 29, 2013

@author: abrien, swimberly
'''

from idgen import IdGen
from entities import Assessment
from helper_entities import Claim
from constants import CLAIM_DEFINITIONS, MINIMUM_ASSESSMENT_SCORE, MAXIMUM_ASSESSMENT_SCORE, ASSMT_SCORE_YEARS, CLAIM_SCORE_MASTER_MAX, CLAIM_SCORE_MASTER_MIN
from random import randint


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
    assmt_years = sorted(ASSMT_SCORE_YEARS)
    for grade in GRADES:
        for atype in TYPES:
            # INTERIM assessment has 3 periods, SUMMATIVE assessment has 1 'EOY' period
            periods = PERIODS if atype == 'INTERIM' else ['EOY']
            for period in periods:
                for subject in SUBJECTS:
                    for index_of_year in range(len(assmt_years)):
                        most_recent = (index_of_year == len(assmt_years) - 1)
                        assessment = generate_single_asmt(grade, atype, period, subject, assmt_years[index_of_year], most_recent)
                        assessments.append(assessment)
    return assessments


def generate_single_asmt(student_grade, asmt_type, period, subject, year, most_recent):
    '''
    returns an Assessment object
    student_grade -- the student_grade for the current assessment
    asmt_type -- the type of assessment to generate either 'INTERIM' or 'SUMMATIVE'
    period -- the period of the assessment. 'BOY', 'MOY' or 'EOY'
    subject -- the subject of the assessment. 'Math' or 'ELA'
    '''

    asmt_guid = generate_id()
    asmt_rec_id = generate_id()
    version = generate_version()

    # Generating claim objects for assessment constructor. Claims are defined by CLAIM_DEFINITIONS in constants.py
    # CLAIM_DEFINITIONS contains claim names, weights
    assessment_claim_info = CLAIM_DEFINITIONS[subject]
    claims = []
    for claim_info in assessment_claim_info:
        claim_name = claim_info['claim_name']
        min_max = generate_claim_score_min_max(CLAIM_SCORE_MASTER_MIN, CLAIM_SCORE_MASTER_MAX)
        claim_score_min = min_max[0]
        claim_score_max = min_max[1]
        claim_score_weight = claim_info['claim_weight']
        claim = Claim(claim_name, claim_score_min, claim_score_max, claim_score_weight)
        claims.append(claim)

    params = {
        'asmt_guid': asmt_guid,
        'asmt_rec_id': asmt_rec_id,
        'asmt_type': asmt_type,
        'asmt_period': period,
        'asmt_period_year': year,
        'asmt_version': version,
        'asmt_grade': student_grade,
        'asmt_subject': subject,
        'claim_list': claims,
        'asmt_score_min': MINIMUM_ASSESSMENT_SCORE,
        'asmt_score_max': MAXIMUM_ASSESSMENT_SCORE,
        'asmt_perf_lvl_name_1': PERFORMANCE_LEVELS[0],
        'asmt_perf_lvl_name_2': PERFORMANCE_LEVELS[1],
        'asmt_perf_lvl_name_3': PERFORMANCE_LEVELS[2],
        'asmt_perf_lvl_name_4': PERFORMANCE_LEVELS[3],
        # TODO: not hard code cut points
        'asmt_cut_point_1': 1400,
        'asmt_cut_point_2': 1800,
        'asmt_cut_point_3': 2100,

        'from_date': str(year) + '0901',
        'most_recent': most_recent
    }

    return Assessment(**params)


def generate_claim_score_min_max(lower_bound, upper_bound):
    if upper_bound - lower_bound < 10:
        raise Exception('lower bound and upper bound are too close')
    # We want at least 10 points between our min and our max

    # Don't want to pick a lower bound greater than (upper bound - 10)
    # If we do, we won't be able to have 10 points separating min and max
    minimum = randint(lower_bound, upper_bound - 10)
    maximum = randint(minimum + 10, upper_bound)

    return (minimum, maximum)


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
