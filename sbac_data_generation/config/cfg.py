"""
The input configuration for the SBAC project.

@author: nestep
@date: February 25, 2014
"""

import datetime

HIERARCHY_FROM_DATE = datetime.date(2012, 9, 1)
HIERARCHY_TO_DATE = datetime.date(9999, 12, 31)

LEP_LANGUAGE_CODES = ['fre', 'ben', 'ger', 'chi', 'kor', 'jpn', 'rus']
LEP_PROFICIENCY_LEVELS = ['very poor', 'poor', 'adequate', 'good', 'very good']
LEP_PROFICIENCY_LEVELS_EXIT = ['good', 'very good']
LEP_TITLE_3_PROGRAMS = ['', '',  # Allow blanks and give them higher weight
                        'DualLanguage', 'TwoWayImmersion', 'TransitionalBilingual', 'DevelopmentalBilingual',
                        'HeritageLanguage', 'ShelteredEnglishInstruction', 'StructuredEnglishImmersion', 'SDAIE',
                        'ContentBasedESL', 'PullOutESL', 'Other']
LEP_HAS_ENTRY_DATE_RATE = .9

PRG_DISABILITY_TYPES = ['', '',  # Allow blanks and give them higher weight
                        'AUT', 'DB', 'DD', 'EMN', 'HI', 'ID', 'MD', 'OI', 'OHI', 'SLD', 'SLI', 'TBI', 'VI']

HAS_ASMT_RESULT_IN_SR_FILE_RATE = .985  # The rate at which students with assessment results are in the SR CSV file

HOLD_BACK_RATE = .01
NOT_ADVANCED_DROP_OUT_RATE = .4
TRANSFER_RATE = .03
REPOPULATE_ADDITIONAL_STUDENTS = [0, 0, 1, 2, 3, 4]

SUBJECTS = ['ELA', 'Math']

ASMT_TO_DATE = datetime.date(9999, 12, 31)

INTERIM_ASMT_RATE = .85
ASMT_SKIP_RATE = .05
ASMT_RETAKE_RATE = .01
ASMT_DELETE_RATE = .02
ASMT_UPDATE_RATE = .02

ASMT_STATUS_ACTIVE = 'C'
ASMT_STATUS_INACTIVE = 'I'
ASMT_STATUS_DELETED = 'D'

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

ACCOMODATIONS = {'acc_asl_video_embed': {'ELA': 4, 'Math': 4},
                 'acc_asl_human_nonembed': {'ELA': 4, 'Math': 4},
                 'acc_braile_embed': {'ELA': 4, 'Math': 4},
                 'acc_closed_captioning_embed': {'ELA': 4, 'Math': 0},
                 'acc_text_to_speech_embed': {'ELA': 4, 'Math': 0},
                 'acc_abacus_nonembed': {'ELA': 0, 'Math': 4},
                 'acc_alternate_response_options_nonembed': {'ELA': 4, 'Math': 4},
                 'acc_calculator_nonembed': {'ELA': 0, 'Math': 4},
                 'acc_multiplication_table_nonembed': {'ELA': 0, 'Math': 4},
                 'acc_print_on_demand_nonembed': {'ELA': 4, 'Math': 4},
                 'acc_read_aloud_nonembed': {'ELA': 4, 'Math': 0},
                 'acc_scribe_nonembed': {'ELA': 4, 'Math': 0},
                 'acc_speech_to_text_nonembed': {'ELA': 4, 'Math': 0},
                 'acc_streamline_mode': {'ELA': 4, 'Math': 4}
                }
