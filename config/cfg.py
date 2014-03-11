"""
The input configuration for the SBAC project.

@author: nestep
@date: February 25, 2014
"""

import datetime

HIERARCHY_FROM_DATE = datetime.date(2012, 9, 1)
HIERARCHY_TO_DATE = None
HIERARCHY_MOST_RECENT = True

LEP_HAS_ENTRY_DATE_RATE = .9

HAS_ASMT_RESULT_BUT_NOT_IN_SR_RATE = .015

SUBJECTS = ['ELA', 'Math']

INTERIM_ASMT_RATE = .85

ASMT_SCORE_MIN = 1200
ASMT_SCORE_MAX = 2400
ASMT_SCORE_AVG = (ASMT_SCORE_MIN + ASMT_SCORE_MAX) / 2
ASMT_SCORE_STD = (ASMT_SCORE_AVG - ASMT_SCORE_MIN) / 4

ASMT_VERSION = 'V1'

ASMT_SCORE_CUT_POINT_1 = 1400
ASMT_SCORE_CUT_POINT_2 = 1800
ASMT_SCORE_CUT_POINT_3 = 2100
ASMT_SCORE_CUT_POINT_4 = None

ASMT_PERF_LEVEL_NAME_1 = 'Minimal Understanding'
ASMT_PERF_LEVEL_NAME_2 = 'Partial Understanding'
ASMT_PERF_LEVEL_NAME_3 = 'Adequate Understanding'
ASMT_PERF_LEVEL_NAME_4 = 'Thorough Understanding'
ASMT_PERF_LEVEL_NAME_5 = None

CLAIM_SCORE_MIN = 1200
CLAIM_SCORE_MAX = 2400

CLAIM_SCORE_CUT_POINT_1 = 1600
CLAIM_SCORE_CUT_POINT_2 = 2000

CLAIM_PERF_LEVEL_NAME_1 = 'Below Standard'
CLAIM_PERF_LEVEL_NAME_2 = 'At/Near Standard'
CLAIM_PERF_LEVEL_NAME_3 = 'Above Standard'

CLAIM_DEFINITIONS = {'Math': [{'name': 'Concepts & Procedures', 'weight': .4},
                              {'name': 'Problem Solving and Modeling & Data Analysis', 'weight': .45},
                              {'name': 'Communicating Reasoning', 'weight': .15}],
                     'ELA': [{'name': 'Reading', 'weight': .20},
                             {'name': 'Writing', 'weight': .25},
                             {'name': 'Listening', 'weight': .25},
                             {'name': 'Research & Inquiry', 'weight': .30}]
                     }