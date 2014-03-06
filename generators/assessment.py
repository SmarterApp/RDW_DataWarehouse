"""
An assessment generator for the SBAC assessment.

@author: nestep
@date: March 3, 2014
"""

import datetime

import general.util.gaussian_distribution as rand_gauss
import general.util.id_gen as id_gen
import project.sbac.config.cfg as sbac_config

from general.model.section import Section
from project.sbac.model.assessment import SBACAssessment
from project.sbac.model.assessmentoutcome import SBACAssessmentOutcome
from project.sbac.model.institutionhierarchy import InstitutionHierarchy
from project.sbac.model.student import SBACStudent


def generate_assessment(asmt_type, period_month, period_year, subject, from_date=None, to_date=None, most_recent=False):
    """
    Generate an assessment object.

    @param asmt_type: Assessment type
    @param period_month: Month of assessment period
    @param period_year: Year of assessment period
    @param subject: Assessment subject
    @param from_date: Assessment from date
    @param to_date: Assessment to date
    @param most_recent: If the assessment is the most recent
    @returns: The assessment object
    """
    # Get the claim definitions for this subject
    if subject not in sbac_config.CLAIM_DEFINITIONS:
        raise KeyError("Subject '" + subject + "' not found in claim definitions")
    claims = sbac_config.CLAIM_DEFINITIONS[subject]

    # Create the object
    sa = SBACAssessment()
    sa.rec_id = id_gen.get_rec_id()
    sa.guid = id_gen.get_uuid()
    sa.asmt_type = asmt_type
    sa.period = period_month + ' ' + str(period_year)
    sa.period_year = period_year
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
    sa.to_date = to_date
    sa.most_recent = most_recent

    # Save and return the object
    sa.save()

    return sa


def generate_assessment_outcome(student: SBACStudent, assessment: SBACAssessment, section: Section,
                                inst_hier: InstitutionHierarchy, month_taken=4, save_to_mongo=True):
    """
    Generate an assessment outcome for a given student.

    @param student: The student to create the outcome for
    @param assessment: The assessment to create the outcome for
    @param section: The section this assessment is related to
    @param inst_hier: The institution hierarchy this student belongs to
    @param month_taken: The month the assessment was taken (optional, defaults to 4 (April))
    @param save_to_mongo: If the outcome should be saved to Mongo (optional, defaults to True)
    @returns: The assessment outcome
    """
    # Create cut-point lists
    overall_cut_points = [assessment.overall_cut_point_1, assessment.overall_cut_point_2,
                          assessment.overall_cut_point_3]
    if assessment.overall_cut_point_4 is not None:
        overall_cut_points.append(assessment.overall_cut_point_4)
    claim_cut_points = [assessment.claim_cut_point_1, assessment.claim_cut_point_2]

    # Create the outcome object
    sao = SBACAssessmentOutcome()
    sao.rec_id = id_gen.get_rec_id()
    sao.guid = id_gen.get_uuid()
    sao.student = student
    sao.assessment = assessment
    sao.section = section
    sao.inst_hierarchy = inst_hier

    # Create the date taken
    sao.date_taken = datetime.date(assessment.period_year, month_taken, 15)

    # Create overall score and performance level
    sao.overall_score = int(rand_gauss.gauss_one(sbac_config.ASMT_SCORE_MIN, sbac_config.ASMT_SCORE_MAX,
                                                 sbac_config.ASMT_SCORE_AVG, sbac_config.ASMT_SCORE_STD))
    sao.overall_score_range_min = sao.overall_score - 20 if sao.overall_score > sbac_config.ASMT_SCORE_MIN + 20 else sbac_config.ASMT_SCORE_MIN
    sao.overall_score_range_max = sao.overall_score + 20 if sao.overall_score < sbac_config.ASMT_SCORE_MAX - 20 else sbac_config.ASMT_SCORE_MAX
    sao.overall_perf_lvl = _pick_performance_level(sao.overall_score, overall_cut_points)

    # Create claim scores and performance levels
    sao.claim_1_score = int(rand_gauss.gauss_one(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
    sao.claim_1_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
    sao.claim_1_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
    sao.claim_1_perf_lvl = _pick_performance_level(sao.claim_1_score, claim_cut_points)
    sao.claim_2_score = int(rand_gauss.gauss_one(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
    sao.claim_2_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
    sao.claim_2_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
    sao.claim_2_perf_lvl = _pick_performance_level(sao.claim_2_score, claim_cut_points)
    sao.claim_3_score = int(rand_gauss.gauss_one(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
    sao.claim_3_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
    sao.claim_3_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
    sao.claim_3_perf_lvl = _pick_performance_level(sao.claim_3_score, claim_cut_points)
    if assessment.claim_4_name is not None:
        sao.claim_4_score = int(rand_gauss.gauss_one(sbac_config.CLAIM_SCORE_MIN, sbac_config.CLAIM_SCORE_MAX))
        sao.claim_4_score_range_min = sao.claim_1_score - 20 if sao.claim_1_score > sbac_config.CLAIM_SCORE_MIN + 20 else sbac_config.CLAIM_SCORE_MIN
        sao.claim_4_score_range_max = sao.claim_1_score + 20 if sao.claim_1_score < sbac_config.CLAIM_SCORE_MAX - 20 else sbac_config.CLAIM_SCORE_MAX
        sao.claim_4_perf_lvl = _pick_performance_level(sao.claim_4_score, claim_cut_points)

    # Save and return the object
    if save_to_mongo:
        sao.save()

    return sao


def _pick_performance_level(score, cut_points):
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