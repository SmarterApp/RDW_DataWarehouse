"""
Unit tests for the project.sbac.generators.assessement module.

@author: sshrestha
@date: March 10, 2014
"""

import datetime

from nose.tools import assert_equal, assert_in, assert_not_in

import sbac_data_generation.generators.assessment as assessment
import sbac_data_generation.generators.population as pop_gen
import sbac_data_generation.generators.hierarchy as hier_gen
import data_generation.generators.enrollment as general_enroll_gen
import sbac_data_generation.generators.enrollment as enroll_gen


def test_pick_default_accommodation_code_0():
    code = assessment._pick_default_accommodation_code(0)
    assert_equal(code, 0)


def test_pick_default_accommodation_code_non_zero():
    allowed_codes = [4, 5, 6, 7, 8, 9, 10]
    code = assessment._pick_default_accommodation_code(4)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(5)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(6)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(7)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(8)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(9)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(10)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(100)
    assert_in(code, allowed_codes)
    code = assessment._pick_default_accommodation_code(-2)
    assert_in(code, allowed_codes)


def test_pick_performance_level():
    cut_points = [10, 20, 30, 40]
    perf_level = assessment.pick_performance_level(5, cut_points)
    assert_equal(1, perf_level)
    perf_level = assessment.pick_performance_level(10, cut_points)
    assert_equal(2, perf_level)
    perf_level = assessment.pick_performance_level(-2, cut_points)
    assert_equal(1, perf_level)
    perf_level = assessment.pick_performance_level(300, cut_points)
    assert_equal(4, perf_level)


def test_generate_assessment_sbac():
    # Create the object
    assmt_type = 'SUMMATIVE'
    period_month = 'Spring'
    assmt_full_period = 'Spring 2015'
    period_year = 2015
    assmt_subject = 'ELA'
    sbac_assmt = assessment.generate_assessment(assmt_type, period_month, period_year, assmt_subject)

    # Tests
    assert_equal(assmt_type, sbac_assmt.asmt_type)
    assert_equal(assmt_full_period, sbac_assmt.period)
    assert_equal(period_year, sbac_assmt.period_year)
    assert_equal('V1', sbac_assmt.version)
    assert_equal(assmt_subject, sbac_assmt.subject)
    assert_equal('Reading', sbac_assmt.claim_1_name)
    assert_equal('Writing', sbac_assmt.claim_2_name)
    assert_equal('Listening', sbac_assmt.claim_3_name)
    assert_equal('Research & Inquiry', sbac_assmt.claim_4_name)
    assert_equal('Minimal Understanding', sbac_assmt.perf_lvl_name_1)
    assert_equal('Partial Understanding', sbac_assmt.perf_lvl_name_2)
    assert_equal('Adequate Understanding', sbac_assmt.perf_lvl_name_3)
    assert_equal('Thorough Understanding', sbac_assmt.perf_lvl_name_4)
    assert_equal(None, sbac_assmt.perf_lvl_name_5)
    assert_equal(1200, sbac_assmt.overall_score_min)
    assert_equal(2400, sbac_assmt.overall_score_max)
    assert_equal(1200, sbac_assmt.claim_1_score_min)
    assert_equal(2400, sbac_assmt.claim_1_score_max)
    assert_equal(0.2, sbac_assmt.claim_1_score_weight)
    assert_equal(1200, sbac_assmt.claim_2_score_min)
    assert_equal(2400, sbac_assmt.claim_2_score_max)
    assert_equal(0.25, sbac_assmt.claim_2_score_weight)
    assert_equal(1200, sbac_assmt.claim_3_score_min)
    assert_equal(2400, sbac_assmt.claim_3_score_max)
    assert_equal(0.25, sbac_assmt.claim_3_score_weight)
    assert_equal(1200, sbac_assmt.claim_4_score_min)
    assert_equal(2400, sbac_assmt.claim_4_score_max)
    assert_equal(0.30, sbac_assmt.claim_4_score_weight)
    assert_equal('Below Standard', sbac_assmt.claim_perf_lvl_name_1)
    assert_equal('At/Near Standard', sbac_assmt.claim_perf_lvl_name_2)
    assert_equal('Above Standard', sbac_assmt.claim_perf_lvl_name_3)
    assert_equal(1400, sbac_assmt.overall_cut_point_1)
    assert_equal(1800, sbac_assmt.overall_cut_point_2)
    assert_equal(2100, sbac_assmt.overall_cut_point_3)
    assert_equal(None, sbac_assmt.overall_cut_point_4)
    assert_equal(1600, sbac_assmt.claim_cut_point_1)
    assert_equal(2000, sbac_assmt.claim_cut_point_2)
    assert_equal(datetime.date(2012, 9, 1), sbac_assmt.from_date)
    assert_equal(datetime.date(9999, 12, 31), sbac_assmt.to_date)
    assert_equal(False, sbac_assmt.most_recent)


def test_generate_assessment_outcome():
    # Create the objects
    sbac_assmt = assessment.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA')
    sbac_state = hier_gen.generate_state('devel', 'Example State', 'ES')
    sbac_district = hier_gen.generate_district('Small Average', sbac_state)
    sbac_school = hier_gen.generate_school('Elementary School', sbac_district)
    sbac_class = general_enroll_gen.generate_class('Class', 'ELA', sbac_school)
    section = enroll_gen.generate_section(sbac_class, 'Section', 3, 2015)
    student = pop_gen.generate_student(sbac_school, 3, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(sbac_state, sbac_district, sbac_school)
    assmt_outcome = assessment.generate_assessment_outcome(student, sbac_assmt, section, institution_hierarchy)

    # Tests
    valid_accomodation_codes = [0, 4, 5, 6, 7, 8, 9, 10]
    assert assmt_outcome.overall_score > 1199
    assert assmt_outcome.overall_score < 2401
    assert assmt_outcome.overall_score_range_min > 1199
    assert assmt_outcome.overall_score_range_max < 2401
    assert assmt_outcome.claim_1_score > 1199
    assert assmt_outcome.claim_1_score < 2401
    assert assmt_outcome.claim_1_score_range_min < 1199
    assert assmt_outcome.claim_1_score_range_max < 2401
    assert assmt_outcome.claim_2_score > 1199
    assert assmt_outcome.claim_2_score < 2401
    assert assmt_outcome.claim_2_score_range_min < 1199
    assert assmt_outcome.claim_2_score_range_max < 2401
    assert assmt_outcome.claim_3_score > 1199
    assert assmt_outcome.claim_3_score < 2401
    assert assmt_outcome.claim_3_score_range_min < 1199
    assert assmt_outcome.claim_3_score_range_max < 2401
    assert_in(assmt_outcome.acc_asl_video_embed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_asl_human_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_braile_embed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_closed_captioning_embed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_text_to_speech_embed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_abacus_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_alternate_response_options_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_calculator_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_multiplication_table_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_alternate_response_options_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_read_aloud_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_scribe_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_speech_to_text_nonembed, valid_accomodation_codes)
    assert_in(assmt_outcome.acc_streamline_mode, valid_accomodation_codes)