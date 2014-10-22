"""
The input configuration for the SBAC project.

@author: nestep
@date: February 25, 2014
"""

import datetime
from sbac_data_generation.util.assessment_stats import Properties, Stats, GradeLevels, DemographicLevels

HIERARCHY_FROM_DATE = datetime.date(2012, 9, 1)
HIERARCHY_TO_DATE = datetime.date(9999, 12, 31)

LEP_LANGUAGE_CODES = ['fre', 'ben', 'ger', 'chi', 'kor', 'jpn', 'rus']
LEP_PROFICIENCY_LEVELS = ['very poor', 'poor', 'adequate', 'good', 'very good']
LEP_PROFICIENCY_LEVELS_EXIT = ['good', 'very good']
LEP_TITLE_3_PROGRAMS = [None, None,  # Allow blanks and give them higher weight
                        'DualLanguage', 'TwoWayImmersion', 'TransitionalBilingual', 'DevelopmentalBilingual',
                        'HeritageLanguage', 'ShelteredEnglishInstruction', 'StructuredEnglishImmersion', 'SDAIE',
                        'ContentBasedESL', 'PullOutESL', 'Other']
LEP_HAS_ENTRY_DATE_RATE = .9

PRG_DISABILITY_TYPES = [None, None,  # Allow blanks and give them higher weight
                        'AUT', 'DB', 'DD', 'EMN', 'HI', 'ID', 'MD', 'OI', 'OHI', 'SLD', 'SLI', 'TBI', 'VI']

HAS_ASMT_RESULT_IN_SR_FILE_RATE = .985  # The rate at which students with assessment results are in the SR CSV file

STUDENT_GROUPING_RATE = .7
ALL_GROUP_RATE = .9
ONE_GROUP_RATE = .5
STUDENTS_PER_GROUP = 50
GROUP_TYPE = ['section_based', 'staff_based']

HOLD_BACK_RATE = .01
NOT_ADVANCED_DROP_OUT_RATE = .4
TRANSFER_RATE = .03
REPOPULATE_ADDITIONAL_STUDENTS = [0, 0, 1, 2, 3, 4]

SUBJECTS = ['ELA', 'Math']

ASMT_TO_DATE = datetime.date(9999, 12, 31)

ASMT_ITEM_BANK_SIZE = 130
ASMT_ITEM_BANK_FORMAT = ['MC', 'EQ', 'GI']
ITEMS_PER_ASMT = 100

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

ACCOMMODATIONS = {
                  'acc_abacus_nonembed': {'ELA': 0, 'Math': 4},
                  'acc_alternate_response_options_nonembed': {'ELA': 4, 'Math': 4},
                  'acc_asl_video_embed': {'ELA': 4, 'Math': 4},
                  'acc_braile_embed': {'ELA': 4, 'Math': 4},
                  'acc_calculator_nonembed': {'ELA': 0, 'Math': 4},
                  'acc_closed_captioning_embed': {'ELA': 4, 'Math': 0},
                  'acc_multiplication_table_nonembed': {'ELA': 0, 'Math': 4},
                  'acc_noise_buffer_nonembed': {'ELA': 4, 'Math': 4},
                  'acc_print_on_demand_items_nonembed': {'ELA': 4, 'Math': 4},
                  'acc_print_on_demand_nonembed': {'ELA': 4, 'Math': 4},
                  'acc_read_aloud_nonembed': {'ELA': 4, 'Math': 0},
                  'acc_scribe_nonembed': {'ELA': 4, 'Math': 0},
                  'acc_speech_to_text_nonembed': {'ELA': 4, 'Math': 0},
                  'acc_streamline_mode': {'ELA': 4, 'Math': 4},
                  'acc_text_to_speech_embed': {'ELA': 4, 'Math': 0},
                  }


DEMOGRAPHICS_BY_GRADE = {
    1: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    ),
    2: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    ),
    3: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    ),
    4: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 92.0, True: 8.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 21.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 18.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    5: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 45.0, True: 55.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 93.0, True: 7.0},
        gender={'female': 49.0, 'male': 51.0, 'not_stated': 0.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 20.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 19.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    6: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 46.0, True: 54.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 94.0, True: 6.0},
        gender={'female': 49.0, 'male': 50.0, 'not_stated': 1.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 22.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 18.0, 'dmg_eth_ami': 0.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    7: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 47.0, True: 53.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 95.0, True: 5.0},
        gender={'female': 48.0, 'male': 51.0, 'not_stated': 1.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 22.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 2.0},
    ),
    8: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 48.0, True: 52.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 95.0, True: 5.0},
        gender={'female': 49.0, 'male': 51.0, 'not_stated': 0.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 21.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 19.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 46.0, 'dmg_eth_pcf': 2.0},
    ),
    9: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    ),
    10: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    ),
    11: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 48.0, True: 52.0},
        dmg_prg_iep={False: 84.0, True: 16.0},
        dmg_prg_lep={False: 95.0, True: 5.0},
        gender={'female': 49.0, 'male': 50.0, 'not_stated': 1.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 21.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 18.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 47.0, 'dmg_eth_pcf': 2.0},
    ),
    12: Properties(
        dmg_prg_504={False: 92.0, True: 8.0},
        dmg_prg_tt1={False: 44.0, True: 56.0},
        dmg_prg_iep={False: 85.0, True: 15.0},
        dmg_prg_lep={False: 91.0, True: 9.0},
        gender={'female': 48.0, 'male': 50.0, 'not_stated': 2.0},
        race={'dmg_eth_2mr': 1.0, 'dmg_eth_hsp': 24.0, 'dmg_eth_asn': 8.0, 'dmg_eth_nst': 2.0, 'dmg_eth_blk': 16.0, 'dmg_eth_ami': 1.0, 'dmg_eth_wht': 48.0, 'dmg_eth_pcf': 0.0},
    ),
}
LEVELS_BY_GRADE_BY_SUBJ = {
    "Math": {
        1: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),),),
        2: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),),),
        3: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),),),
        4: GradeLevels((9.0, 32.0, 54.0, 5.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(35.0, 45.0, 20.0, 0.0),
                            False: Stats(6.739130434782608, 30.869565217391305, 56.95652173913044, 5.434782608695652)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 41.0, 44.0, 2.0),
                            False: Stats(3.909090909090909, 20.545454545454547, 66.72727272727273, 8.818181818181818)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(35.0, 45.0, 20.0, 0.0),
                            False: Stats(4.0476190476190474, 29.523809523809526, 60.476190476190474, 5.9523809523809526)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(30.0, 52.0, 18.0, 0.0),
                            False: Stats(7.173913043478261, 30.26086956521739, 57.130434782608695, 5.434782608695652)}),
                       gender=DemographicLevels(
                           female=Stats(7.0, 29.0, 58.0, 6.0),
                           male=Stats(12.0, 33.0, 52.0, 3.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(5.0, 28.0, 37.0, 30.0),
                           dmg_eth_ami=Stats(13.0, 39.0, 46.0, 2.0),
                           dmg_eth_asn=Stats(6.0, 20.0, 64.0, 10.0),
                           dmg_eth_blk=Stats(14.0, 43.0, 41.0, 2.0),
                           dmg_eth_hsp=Stats(13.0, 42.0, 43.0, 2.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(6.0, 24.0, 64.0, 6.0),),),
        5: GradeLevels((11.0, 31.0, 53.0, 5.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(39.0, 44.0, 17.0, 0.0),
                            False: Stats(8.565217391304348, 29.869565217391305, 56.130434782608695, 5.434782608695652)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(15.0, 40.0, 43.0, 2.0),
                            False: Stats(6.111111111111111, 20.0, 65.22222222222223, 8.666666666666666)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(39.0, 44.0, 17.0, 0.0),
                            False: Stats(5.666666666666667, 28.523809523809526, 59.857142857142854, 5.9523809523809526)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(39.0, 48.0, 13.0, 0.0),
                            False: Stats(8.89247311827957, 29.72043010752688, 56.01075268817204, 5.376344086021505)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 30.0, 56.0, 6.0),
                           male=Stats(13.0, 33.0, 51.0, 3.0),
                           not_stated=Stats(0.0, 0.0, 0.0, 0.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 29.0, 35.0, 27.0),
                           dmg_eth_ami=Stats(15.0, 42.0, 40.0, 3.0),
                           dmg_eth_asn=Stats(7.0, 20.0, 63.0, 10.0),
                           dmg_eth_blk=Stats(17.0, 43.0, 38.0, 2.0),
                           dmg_eth_hsp=Stats(15.0, 40.0, 43.0, 2.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(7.0, 25.0, 62.0, 6.0),),),
        6: GradeLevels((11.0, 33.0, 54.0, 2.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(38.0, 47.0, 15.0, 0.0),
                            False: Stats(8.652173913043478, 31.782608695652176, 57.391304347826086, 2.1739130434782608)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(16.0, 43.0, 40.0, 1.0),
                            False: Stats(5.130434782608695, 21.26086956521739, 70.43478260869566, 3.1739130434782608)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(38.0, 47.0, 15.0, 0.0),
                            False: Stats(5.857142857142857, 30.333333333333332, 61.42857142857143, 2.380952380952381)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(51.0, 44.0, 5.0, 0.0),
                            False: Stats(8.446808510638299, 32.297872340425535, 57.12765957446808, 2.127659574468085)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 58.0, 3.0),
                           male=Stats(13.0, 36.0, 49.0, 2.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 30.0, 32.0, 31.0),
                           dmg_eth_ami=Stats(0.0, 0.0, 0.0, 0.0),
                           dmg_eth_asn=Stats(8.0, 23.0, 64.0, 5.0),
                           dmg_eth_blk=Stats(16.0, 47.0, 36.0, 1.0),
                           dmg_eth_hsp=Stats(17.0, 44.0, 38.0, 1.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(6.0, 26.0, 64.0, 4.0),),),
        7: GradeLevels((8.0, 40.0, 48.0, 4.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(33.0, 55.0, 12.0, 0.0),
                            False: Stats(5.826086956521739, 38.69565217391305, 51.130434782608695, 4.3478260869565215)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 50.0, 36.0, 1.0),
                            False: Stats(2.3617021276595747, 28.72340425531915, 61.53191489361702, 7.382978723404255)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(33.0, 55.0, 12.0, 0.0),
                            False: Stats(3.238095238095238, 37.142857142857146, 54.857142857142854, 4.761904761904762)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(42.0, 54.0, 4.0, 0.0),
                            False: Stats(6.2105263157894735, 39.26315789473684, 50.31578947368421, 4.2105263157894735)}),
                       gender=DemographicLevels(
                           female=Stats(6.0, 36.0, 53.0, 5.0),
                           male=Stats(11.0, 42.0, 44.0, 3.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 28.0, 34.0, 31.0),
                           dmg_eth_ami=Stats(11.0, 50.0, 38.0, 1.0),
                           dmg_eth_asn=Stats(6.0, 26.0, 60.0, 8.0),
                           dmg_eth_blk=Stats(13.0, 53.0, 33.0, 1.0),
                           dmg_eth_hsp=Stats(13.0, 51.0, 35.0, 1.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.0, 31.0, 59.0, 5.0),),),
        8: GradeLevels((7.0, 43.0, 48.0, 2.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 60.0, 11.0, 0.0),
                            False: Stats(5.086956521739131, 41.52173913043478, 51.21739130434783, 2.1739130434782608)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(11.0, 54.0, 34.0, 1.0),
                            False: Stats(2.6666666666666665, 31.083333333333332, 63.166666666666664, 3.0833333333333335)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 60.0, 11.0, 0.0),
                            False: Stats(2.8095238095238093, 39.76190476190476, 55.04761904761905, 2.380952380952381)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(43.0, 54.0, 3.0, 0.0),
                            False: Stats(5.105263157894737, 42.421052631578945, 50.36842105263158, 2.1052631578947367)}),
                       gender=DemographicLevels(
                           female=Stats(5.0, 39.0, 53.0, 3.0),
                           male=Stats(9.0, 46.0, 44.0, 1.0),
                           not_stated=Stats(0.0, 0.0, 0.0, 0.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(8.0, 30.0, 42.0, 20.0),
                           dmg_eth_ami=Stats(10.0, 52.0, 37.0, 1.0),
                           dmg_eth_asn=Stats(7.0, 28.0, 61.0, 4.0),
                           dmg_eth_blk=Stats(11.0, 59.0, 30.0, 0.0),
                           dmg_eth_hsp=Stats(12.0, 55.0, 33.0, 0.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(4.0, 33.0, 60.0, 3.0),),),
        9: GradeLevels((14.0, 30.0, 49.0, 7.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(20.0, 38.0, 39.0, 3.0),
                            False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(45.0, 37.0, 17.0, 1.0),
                            False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(38.0, 43.0, 19.0, 0.0),
                            False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}),
                       gender=DemographicLevels(
                           female=Stats(11.0, 29.0, 52.0, 8.0),
                           male=Stats(16.0, 33.0, 46.0, 5.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                           dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                           dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                           dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                           dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),),),
        10: GradeLevels((14.0, 30.0, 49.0, 7.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(20.0, 38.0, 39.0, 3.0),
                             False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(38.0, 43.0, 19.0, 0.0),
                             False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}),
                        gender=DemographicLevels(
                            female=Stats(11.0, 29.0, 52.0, 8.0),
                            male=Stats(16.0, 33.0, 46.0, 5.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                            dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                            dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                            dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                            dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),),),
        11: GradeLevels((7.0, 43.0, 48.0, 2.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(29.0, 60.0, 11.0, 0.0),
                             False: Stats(5.086956521739131, 41.52173913043478, 51.21739130434783, 2.1739130434782608)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(11.0, 54.0, 34.0, 1.0),
                             False: Stats(2.6666666666666665, 31.083333333333332, 63.166666666666664, 3.0833333333333335)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(29.0, 60.0, 11.0, 0.0),
                             False: Stats(2.8095238095238093, 39.76190476190476, 55.04761904761905, 2.380952380952381)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(43.0, 54.0, 3.0, 0.0),
                             False: Stats(5.105263157894737, 42.421052631578945, 50.36842105263158, 2.1052631578947367)}),
                        gender=DemographicLevels(
                            female=Stats(5.0, 39.0, 53.0, 3.0),
                            male=Stats(9.0, 46.0, 44.0, 1.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(10.0, 52.0, 37.0, 1.0),
                            dmg_eth_asn=Stats(7.0, 28.0, 61.0, 4.0),
                            dmg_eth_blk=Stats(11.0, 59.0, 30.0, 0.0),
                            dmg_eth_hsp=Stats(12.0, 55.0, 33.0, 0.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(4.0, 33.0, 60.0, 3.0),),),
        12: GradeLevels((14.0, 30.0, 49.0, 7.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(11.304347826086957, 29.391304347826086, 51.78260869565217, 7.521739130434782)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(20.0, 38.0, 39.0, 3.0),
                             False: Stats(6.363636363636363, 19.818181818181817, 61.72727272727273, 12.090909090909092)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(45.0, 37.0, 17.0, 1.0),
                             False: Stats(8.529411764705882, 28.764705882352942, 54.64705882352941, 8.058823529411764)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(38.0, 43.0, 19.0, 0.0),
                             False: Stats(11.626373626373626, 28.714285714285715, 51.967032967032964, 7.6923076923076925)}),
                        gender=DemographicLevels(
                            female=Stats(11.0, 29.0, 52.0, 8.0),
                            male=Stats(16.0, 33.0, 46.0, 5.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(18.0, 36.0, 42.0, 4.0),
                            dmg_eth_asn=Stats(8.0, 22.0, 57.0, 13.0),
                            dmg_eth_blk=Stats(21.0, 40.0, 37.0, 2.0),
                            dmg_eth_hsp=Stats(20.0, 39.0, 38.0, 3.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(0.0, 0.0, 0.0, 0.0),
                            dmg_eth_wht=Stats(9.0, 25.0, 57.0, 9.0),),),
    },
    "ELA": {
        1: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.494623655913978, 29.096774193548388, 49.655913978494624, 13.75268817204301)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.697674418604651, 20.72093023255814, 55.95348837209303, 19.627906976744185)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.470588235294118, 27.88235294117647, 51.88235294117647, 14.764705882352942)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.615384615384615, 28.813186813186814, 49.582417582417584, 13.989010989010989)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4),),),
        2: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.494623655913978, 29.096774193548388, 49.655913978494624, 13.75268817204301)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.697674418604651, 20.72093023255814, 55.95348837209303, 19.627906976744185)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.470588235294118, 27.88235294117647, 51.88235294117647, 14.764705882352942)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.615384615384615, 28.813186813186814, 49.582417582417584, 13.989010989010989)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4),),),
        3: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.494623655913978, 29.096774193548388, 49.655913978494624, 13.75268817204301)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.697674418604651, 20.72093023255814, 55.95348837209303, 19.627906976744185)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.470588235294118, 27.88235294117647, 51.88235294117647, 14.764705882352942)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.615384615384615, 28.813186813186814, 49.582417582417584, 13.989010989010989)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4),),),
        4: GradeLevels((5.0, 26.0, 39.0, 30.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(21.0, 44.0, 26.0, 9.0),
                            False: Stats(3.608695652173913, 24.434782608695652, 40.130434782608695, 31.82608695652174)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(8.0, 33.0, 38.0, 21.0),
                            False: Stats(1.1818181818181819, 17.09090909090909, 40.27272727272727, 41.45454545454545)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(21.0, 44.0, 26.0, 9.0),
                            False: Stats(1.9523809523809523, 22.571428571428573, 41.476190476190474, 34.0)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(15.0, 42.0, 33.0, 10.0),
                            False: Stats(4.010989010989011, 24.417582417582416, 39.59340659340659, 31.978021978021978)}),
                       gender=DemographicLevels(
                           female=Stats(5.0, 26.0, 39.0, 30.0),
                           male=Stats(5.0, 26.0, 39.0, 30.0),
                           not_stated=Stats(0.0, 0.0, 0.0, 0.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(5.0, 28.0, 37.0, 30.0),
                           dmg_eth_ami=Stats(8.0, 34.0, 36.0, 22.0),
                           dmg_eth_asn=Stats(2.0, 10.0, 31.0, 57.0),
                           dmg_eth_blk=Stats(8.0, 40.0, 37.0, 15.0),
                           dmg_eth_hsp=Stats(8.0, 33.0, 40.0, 19.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(3.0, 19.0, 40.4468, 37.5532),),),
        5: GradeLevels((7.0, 26.0, 39.0, 28.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(27.0, 42.0, 25.0, 6.0),
                            False: Stats(5.260869565217392, 24.608695652173914, 40.21739130434783, 29.91304347826087)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(10.0, 33.0, 37.0, 20.0),
                            False: Stats(3.1818181818181817, 17.09090909090909, 41.54545454545455, 38.18181818181818)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(27.0, 42.0, 25.0, 6.0),
                            False: Stats(3.1904761904761907, 22.952380952380953, 41.666666666666664, 32.19047619047619)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(21.0, 42.0, 28.0, 9.0),
                            False: Stats(5.782608695652174, 24.608695652173914, 39.95652173913044, 29.652173913043477)}),
                       gender=DemographicLevels(
                           female=Stats(7.0, 25.0, 40.0, 28.0),
                           male=Stats(7.1, 26.9, 37.64, 28.36),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 29.0, 35.0, 27.0),
                           dmg_eth_ami=Stats(13.0, 34.0, 35.0, 18.0),
                           dmg_eth_asn=Stats(3.0, 11.0, 30.0, 56.0),
                           dmg_eth_blk=Stats(13.0, 36.0, 36.0, 15.0),
                           dmg_eth_hsp=Stats(10.0, 33.0, 38.0, 19.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(4.8542, 21.145799999999998, 41.4167, 32.5833),),),
        6: GradeLevels((8.0, 27.0, 34.0, 31.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 44.0, 21.0, 6.0),
                            False: Stats(6.173913043478261, 25.52173913043478, 35.130434782608695, 33.17391304347826)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(12.0, 35.0, 33.0, 20.0),
                            False: Stats(3.3043478260869565, 17.608695652173914, 35.17391304347826, 43.91304347826087)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 44.0, 21.0, 6.0),
                            False: Stats(4.0, 23.761904761904763, 36.476190476190474, 35.76190476190476)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(27.0, 44.0, 21.0, 8.0),
                            False: Stats(6.787234042553192, 25.914893617021278, 34.829787234042556, 32.46808510638298)}),
                       gender=DemographicLevels(
                           female=Stats(7.0, 26.0, 34.6735, 32.3265),
                           male=Stats(9.0, 28.0, 33.0, 30.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 30.0, 32.0, 31.0),
                           dmg_eth_ami=Stats(12.0, 35.0, 34.0, 19.0),
                           dmg_eth_asn=Stats(3.0, 11.0, 26.0, 60.0),
                           dmg_eth_blk=Stats(14.6842, 38.3158, 32.0, 15.0),
                           dmg_eth_hsp=Stats(12.0, 36.0, 34.0, 18.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.0, 21.2553, 35.7021, 38.0426),),),
        7: GradeLevels((9.0, 26.0, 34.0, 31.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(31.0, 43.0, 21.0, 5.0),
                            False: Stats(7.086956521739131, 24.52173913043478, 35.130434782608695, 33.26086956521739)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 35.0, 33.0, 19.0),
                            False: Stats(4.48936170212766, 15.851063829787234, 35.12765957446808, 44.53191489361702)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(31.0, 43.0, 21.0, 5.0),
                            False: Stats(4.809523809523809, 22.761904761904763, 36.476190476190474, 35.95238095238095)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(30.0, 43.0, 20.0, 7.0),
                            False: Stats(7.659574468085107, 24.914893617021278, 34.8936170212766, 32.53191489361702)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 26.0, 35.0, 31.0),
                           male=Stats(10.0, 26.0, 32.7255, 31.2745),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(7.0, 28.0, 34.0, 31.0),
                           dmg_eth_ami=Stats(10.0, 35.0, 34.0, 21.0),
                           dmg_eth_asn=Stats(3.0, 12.0, 25.0, 60.0),
                           dmg_eth_blk=Stats(18.3684, 37.6316, 31.0, 13.0),
                           dmg_eth_hsp=Stats(13.0, 36.0, 34.0, 17.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.0, 19.0, 36.4167, 39.5833),),),
        8: GradeLevels((7.0, 32.0, 41.0, 20.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(27.0, 50.0, 21.0, 2.0),
                            False: Stats(5.260869565217392, 30.434782608695652, 42.73913043478261, 21.565217391304348)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(11.0, 40.0, 37.0, 12.0),
                            False: Stats(2.6666666666666665, 23.333333333333332, 45.333333333333336, 28.666666666666668)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(27.0, 50.0, 21.0, 2.0),
                            False: Stats(3.1904761904761907, 28.571428571428573, 44.80952380952381, 23.428571428571427)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(22.0, 45.0, 27.0, 6.0),
                            False: Stats(6.042553191489362, 31.170212765957448, 41.8936170212766, 20.893617021276597)}),
                       gender=DemographicLevels(
                           female=Stats(6.0, 31.0, 41.8163, 21.1837),
                           male=Stats(8.0, 33.0, 40.0, 19.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(8.0, 30.0, 42.0, 20.0),
                           dmg_eth_ami=Stats(9.0, 40.0, 39.0, 12.0),
                           dmg_eth_asn=Stats(2.0, 14.0, 37.0, 47.0),
                           dmg_eth_blk=Stats(13.5, 45.5, 34.0, 7.0),
                           dmg_eth_hsp=Stats(11.0, 40.0, 39.0, 10.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(4.0, 26.5625, 45.0625, 24.375),),),
        9: GradeLevels((9.0, 30.0, 48.0, 13.0),
                       dmg_prg_504=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(7.494623655913978, 29.096774193548388, 49.655913978494624, 13.75268817204301)}),
                       dmg_prg_tt1=DemographicLevels(
                           {True: Stats(13.0, 37.0, 42.0, 8.0),
                            False: Stats(3.697674418604651, 20.72093023255814, 55.95348837209303, 19.627906976744185)}),
                       dmg_prg_iep=DemographicLevels(
                           {True: Stats(29.0, 42.0, 26.0, 3.0),
                            False: Stats(5.470588235294118, 27.88235294117647, 51.88235294117647, 14.764705882352942)}),
                       dmg_prg_lep=DemographicLevels(
                           {True: Stats(23.0, 42.0, 32.0, 3.0),
                            False: Stats(7.615384615384615, 28.813186813186814, 49.582417582417584, 13.989010989010989)}),
                       gender=DemographicLevels(
                           female=Stats(8.0, 31.0, 49.0, 12.0),
                           male=Stats(10.0, 29.0, 47.0, 14.0),
                           not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                       race=DemographicLevels(
                           dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                           dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                           dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                           dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                           dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                           dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                           dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                           dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4),),),
        10: GradeLevels((9.0, 30.0, 48.0, 13.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(7.494623655913978, 29.096774193548388, 49.655913978494624, 13.75268817204301)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(13.0, 37.0, 42.0, 8.0),
                             False: Stats(3.697674418604651, 20.72093023255814, 55.95348837209303, 19.627906976744185)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(5.470588235294118, 27.88235294117647, 51.88235294117647, 14.764705882352942)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(23.0, 42.0, 32.0, 3.0),
                             False: Stats(7.615384615384615, 28.813186813186814, 49.582417582417584, 13.989010989010989)}),
                        gender=DemographicLevels(
                            female=Stats(8.0, 31.0, 49.0, 12.0),
                            male=Stats(10.0, 29.0, 47.0, 14.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                            dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                            dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                            dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4),),),
        11: GradeLevels((7.0, 32.0, 41.0, 20.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(27.0, 50.0, 21.0, 2.0),
                             False: Stats(5.260869565217392, 30.434782608695652, 42.73913043478261, 21.565217391304348)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(11.0, 40.0, 37.0, 12.0),
                             False: Stats(2.6666666666666665, 23.333333333333332, 45.333333333333336, 28.666666666666668)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(27.0, 50.0, 21.0, 2.0),
                             False: Stats(3.1904761904761907, 28.571428571428573, 44.80952380952381, 23.428571428571427)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(22.0, 45.0, 27.0, 6.0),
                             False: Stats(6.042553191489362, 31.170212765957448, 41.8936170212766, 20.893617021276597)}),
                        gender=DemographicLevels(
                            female=Stats(6.0, 31.0, 43.0, 20.0),
                            male=Stats(8.0, 33.0, 38.7647, 20.2353),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(9.0, 40.0, 39.0, 12.0),
                            dmg_eth_asn=Stats(2.0, 14.0, 37.0, 47.0),
                            dmg_eth_blk=Stats(12.9474, 46.052600000000005, 34.0, 7.0),
                            dmg_eth_hsp=Stats(11.0, 40.0, 39.0, 10.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(4.0, 25.9149, 45.1915, 24.893600000000003),),),
        12: GradeLevels((9.0, 30.0, 48.0, 13.0),
                        dmg_prg_504=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(7.494623655913978, 29.096774193548388, 49.655913978494624, 13.75268817204301)}),
                        dmg_prg_tt1=DemographicLevels(
                            {True: Stats(13.0, 37.0, 42.0, 8.0),
                             False: Stats(3.697674418604651, 20.72093023255814, 55.95348837209303, 19.627906976744185)}),
                        dmg_prg_iep=DemographicLevels(
                            {True: Stats(29.0, 42.0, 26.0, 3.0),
                             False: Stats(5.470588235294118, 27.88235294117647, 51.88235294117647, 14.764705882352942)}),
                        dmg_prg_lep=DemographicLevels(
                            {True: Stats(23.0, 42.0, 32.0, 3.0),
                             False: Stats(7.615384615384615, 28.813186813186814, 49.582417582417584, 13.989010989010989)}),
                        gender=DemographicLevels(
                            female=Stats(8.0, 31.0, 49.0, 12.0),
                            male=Stats(10.0, 29.0, 47.0, 14.0),
                            not_stated=Stats(9.0, 30.0, 51.0, 10.0),),
                        race=DemographicLevels(
                            dmg_eth_2mr=Stats(9.0, 31.0, 47.0, 13.0),
                            dmg_eth_ami=Stats(12.0, 36.0, 43.0, 9.0),
                            dmg_eth_asn=Stats(3.0, 16.0, 53.0, 28.0),
                            dmg_eth_blk=Stats(17.0, 40.0, 37.0, 6.0),
                            dmg_eth_hsp=Stats(13.0, 37.0, 43.0, 7.0),
                            dmg_eth_nst=Stats(4.0, 47.0, 31.0, 18.0),
                            dmg_eth_pcf=Stats(2.0, 15.0, 53.0, 30.0),
                            dmg_eth_wht=Stats(5.3, 24.7, 54.6, 15.4),),),
    },
}
