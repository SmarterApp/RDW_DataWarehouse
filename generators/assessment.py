"""
An assessment generator for the SBAC assessment.

@author: nestep
@date: March 3, 2014
"""

import datetime
import random

import general.generators.assessment as gen_asmt_generator
import general.util.id_gen as gen_id_gen
import project.sbac.config.cfg as sbac_config

from general.model.section import Section
from project.sbac.model.assessment import SBACAssessment
from project.sbac.model.assessmentoutcome import SBACAssessmentOutcome
from project.sbac.model.institutionhierarchy import InstitutionHierarchy
from project.sbac.model.student import SBACStudent


def generate_assessment(asmt_type, period, asmt_year, subject, from_date=None, to_date=None, most_recent=False,
                        asmt_year_adj=0):
    """
    Generate an assessment object.

    @param asmt_type: Assessment type
    @param period: Period within assessment year
    @param asmt_year: Assessment year
    @param subject: Assessment subject
    @param from_date: Assessment from date
    @param to_date: Assessment to date
    @param most_recent: If the assessment is the most recent
    @param asmt_yaer_adj: An amount to adjust the assessment period year by
    @returns: The assessment object
    """
    # Get the claim definitions for this subject
    if subject not in sbac_config.CLAIM_DEFINITIONS:
        raise KeyError("Subject '" + subject + "' not found in claim definitions")
    claims = sbac_config.CLAIM_DEFINITIONS[subject]

    # Run the General generator
    sa = gen_asmt_generator.generate_assessment(SBACAssessment)

    # Set other specifics
    sa.rec_id = gen_id_gen.get_rec_id('assessment')
    sa.asmt_type = asmt_type
    sa.period = period + ' ' + str((asmt_year + asmt_year_adj))
    sa.period_year = asmt_year + asmt_year_adj
    sa.version = sbac_config.ASMT_VERSION
    sa.subject = subject
    sa.claim_1_name = claims[0]['name']
    sa.claim_2_name = claims[1]['name']
    sa.claim_3_name = claims[2]['name']
    sa.claim_4_name = claims[3]['name'] if len(claims) == 4 else None
    sa.perf_lvl_name_1 = sbac_config.ASMT_PERF_LEVEL_NAME_1
    sa.perf_lvl_name_2 = sbac_config.ASMT_PERF_LEVEL_NAME_2
    sa.perf_lvl_name_3 = sbac_config.ASMT_PERF_LEVEL_NAME_3
    sa.perf_lvl_name_4 = sbac_config.ASMT_PERF_LEVEL_NAME_4
    sa.perf_lvl_name_5 = sbac_config.ASMT_PERF_LEVEL_NAME_5
    sa.overall_score_min = sbac_config.ASMT_SCORE_MIN
    sa.overall_score_max = sbac_config.ASMT_SCORE_MAX
    sa.claim_1_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_1_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_1_score_weight = claims[0]['weight']
    sa.claim_2_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_2_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_2_score_weight = claims[1]['weight']
    sa.claim_3_score_min = sbac_config.CLAIM_SCORE_MIN
    sa.claim_3_score_max = sbac_config.CLAIM_SCORE_MAX
    sa.claim_3_score_weight = claims[2]['weight']
    sa.claim_4_score_min = sbac_config.CLAIM_SCORE_MIN if len(claims) == 4 else None
    sa.claim_4_score_max = sbac_config.CLAIM_SCORE_MAX if len(claims) == 4 else None
    sa.claim_4_score_weight = claims[3]['weight'] if len(claims) == 4 else None
    sa.claim_perf_lvl_name_1 = sbac_config.CLAIM_PERF_LEVEL_NAME_1
    sa.claim_perf_lvl_name_2 = sbac_config.CLAIM_PERF_LEVEL_NAME_2
    sa.claim_perf_lvl_name_3 = sbac_config.CLAIM_PERF_LEVEL_NAME_3
    sa.overall_cut_point_1 = sbac_config.ASMT_SCORE_CUT_POINT_1
    sa.overall_cut_point_2 = sbac_config.ASMT_SCORE_CUT_POINT_2
    sa.overall_cut_point_3 = sbac_config.ASMT_SCORE_CUT_POINT_3
    sa.overall_cut_point_4 = sbac_config.ASMT_SCORE_CUT_POINT_4
    sa.claim_cut_point_1 = sbac_config.CLAIM_SCORE_CUT_POINT_1
    sa.claim_cut_point_2 = sbac_config.CLAIM_SCORE_CUT_POINT_2
    sa.from_date = from_date if from_date is not None else sbac_config.HIERARCHY_FROM_DATE
    sa.to_date = to_date if to_date is not None else sbac_config.HIERARCHY_TO_DATE
    sa.effective_date = sbac_config.ASMT_EFFECTIVE_DATE
    sa.most_recent = most_recent

    # Save and return the object
    sa.save()

    return sa


def generate_assessment_outcome(student: SBACStudent, assessment: SBACAssessment, section: Section,
                                inst_hier: InstitutionHierarchy, save_to_mongo=True):
    """
    Generate an assessment outcome for a given student.

    @param student: The student to create the outcome for
    @param assessment: The assessment to create the outcome for
    @param section: The section this assessment is related to
    @param inst_hier: The institution hierarchy this student belongs to
    @param save_to_mongo: If the outcome should be saved to Mongo (optional, defaults to True)
    @returns: The assessment outcome
    """
    # Create cut-point lists
    overall_cut_points = [assessment.overall_cut_point_1, assessment.overall_cut_point_2,
                          assessment.overall_cut_point_3]
    if assessment.overall_cut_point_4 is not None:
        overall_cut_points.append(assessment.overall_cut_point_4)
    claim_cut_points = [assessment.claim_cut_point_1, assessment.claim_cut_point_2]

    # Run the General generator
    sao = gen_asmt_generator.generate_assessment_outcome(student, assessment, section, SBACAssessmentOutcome)

    # Set other specifics
    sao.inst_hierarchy = inst_hier

    # Create the date taken
    period_month = 9
    if assessment.asmt_type == 'SUMMATIVE':
        period_month = 4
    elif 'Winter' in assessment.period:
        period_month = 12
    elif 'Spring' in assessment.period:
        period_month = 2
    sao.date_taken = datetime.date(assessment.period_year, period_month, 15)

    # Create overall score and performance level
    sao.overall_score = int(random.uniform(sbac_config.ASMT_SCORE_MIN, sbac_config.ASMT_SCORE_MAX))
    sao.overall_score_range_min = sao.overall_score - 20 if sao.overall_score > sbac_config.ASMT_SCORE_MIN + 20 else sbac_config.ASMT_SCORE_MIN
    sao.overall_score_range_max = sao.overall_score + 20 if sao.overall_score < sbac_config.ASMT_SCORE_MAX - 20 else sbac_config.ASMT_SCORE_MAX
    sao.overall_perf_lvl = pick_performance_level(sao.overall_score, overall_cut_points)

    # Create claim scores and performance levels
    sao.claim_1_score = int(random.uniform(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
    sao.claim_1_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
    sao.claim_1_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
    sao.claim_1_perf_lvl = pick_performance_level(sao.claim_1_score, claim_cut_points)
    sao.claim_2_score = int(random.uniform(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
    sao.claim_2_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
    sao.claim_2_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
    sao.claim_2_perf_lvl = pick_performance_level(sao.claim_2_score, claim_cut_points)
    sao.claim_3_score = int(random.uniform(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
    sao.claim_3_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
    sao.claim_3_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
    sao.claim_3_perf_lvl = pick_performance_level(sao.claim_3_score, claim_cut_points)
    if assessment.claim_4_name is not None:
        sao.claim_4_score = int(random.uniform(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
        sao.claim_4_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
        sao.claim_4_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
        sao.claim_4_perf_lvl = pick_performance_level(sao.claim_4_score, claim_cut_points)

    # Create accommodations details
    sao.acc_asl_video_embed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_asl_video_embed'][assessment.subject])
    sao.acc_asl_human_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_asl_human_nonembed'][assessment.subject])
    sao.acc_braile_embed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_braile_embed'][assessment.subject])
    sao.acc_closed_captioning_embed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_closed_captioning_embed'][assessment.subject])
    sao.acc_text_to_speech_embed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_text_to_speech_embed'][assessment.subject])
    sao.acc_abacus_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_abacus_nonembed'][assessment.subject])
    sao.acc_alternate_response_options_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_alternate_response_options_nonembed'][assessment.subject])
    sao.acc_calculator_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_calculator_nonembed'][assessment.subject])
    sao.acc_multiplication_table_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_multiplication_table_nonembed'][assessment.subject])
    sao.acc_print_on_demand_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_asl_video_embed'][assessment.subject])
    sao.acc_read_aloud_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_read_aloud_nonembed'][assessment.subject])
    sao.acc_scribe_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_scribe_nonembed'][assessment.subject])
    sao.acc_speech_to_text_nonembed = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_speech_to_text_nonembed'][assessment.subject])
    sao.acc_streamline_mode = _pick_default_accommodation_code(sbac_config.ACCOMODATIONS['acc_streamline_mode'][assessment.subject])
    
    # Save and return the object
    if save_to_mongo:
        sao.save()

    return sao


def pick_performance_level(score, cut_points):
    """
    Pick the performance level for a given score and cut points.

    @param score: The score to assign a performance level for
    @param cut_points: List of scores that separate the performance levels
    @returns: Performance level
    """
    for i, cut_point in enumerate(cut_points):
        if score < cut_point:
            return i + 1

    return len(cut_points)


def _pick_default_accommodation_code(code):
    """
    Pick accomdation code of 4 to 10 randomly if code is 4.
    If code is 0 return 0.

    @param code: The code to generate
    @return: Generated random code
    """
    if code == 0:
        return code
    else:
        return random.randint(4, 10)
