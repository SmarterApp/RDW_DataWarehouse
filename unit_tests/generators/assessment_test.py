"""
Unit tests for the project.sbac.generators.assessement module.

@author: nestep
@date: March 18, 2014
"""

import datetime

import data_generation.config.hierarchy as hier_config
import data_generation.config.population as pop_config
import sbac_data_generation.config.hierarchy as sbac_hier_config
import sbac_data_generation.config.population as sbac_pop_config
import sbac_data_generation.generators.assessment as asmt_gen
import sbac_data_generation.generators.enrollment as enroll_gen
import sbac_data_generation.generators.hierarchy as hier_gen
import sbac_data_generation.generators.population as pop_gen


def setup_module():
    hier_config.STATE_TYPES.update(sbac_hier_config.STATE_TYPES)
    pop_config.DEMOGRAPHICS['california'] = sbac_pop_config.DEMOGRAPHICS['california']
    for grade, demo in sbac_pop_config.DEMOGRAPHICS['typical1'].items():
        if grade in pop_config.DEMOGRAPHICS['typical1']:
            pop_config.DEMOGRAPHICS['typical1'][grade].update(demo)


def test_pick_default_accommodation_code_0():
    code = asmt_gen._pick_default_accommodation_code(0)
    assert code == 0


def test_pick_default_accommodation_code_non_zero():
    allowed_codes = [4, 5, 6, 7, 8, 9, 10]
    code = asmt_gen._pick_default_accommodation_code(4)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(5)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(6)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(7)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(8)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(9)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(10)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(100)
    assert code in allowed_codes
    code = asmt_gen._pick_default_accommodation_code(-2)
    assert code in allowed_codes


def test_pick_performance_level():
    cut_points = [10, 20, 30, 40]
    perf_level = asmt_gen.pick_performance_level(5, cut_points)
    assert 1 == perf_level
    perf_level = asmt_gen.pick_performance_level(10, cut_points)
    assert 2 == perf_level
    perf_level = asmt_gen.pick_performance_level(-2, cut_points)
    assert 1 == perf_level
    perf_level = asmt_gen.pick_performance_level(300, cut_points)
    assert 4 == perf_level


def test_generate_assessment_sbac():
    # Create the object
    assmt_type = 'SUMMATIVE'
    period_month = 'Spring'
    assmt_full_period = 'Spring 2015'
    period_year = 2015
    assmt_subject = 'ELA'
    sbac_assmt = asmt_gen.generate_assessment(assmt_type, period_month, period_year, assmt_subject)

    # Tests
    assert assmt_type == sbac_assmt.asmt_type
    assert assmt_full_period == sbac_assmt.period
    assert period_year == sbac_assmt.period_year
    assert 'V1' == sbac_assmt.version
    assert assmt_subject == sbac_assmt.subject
    assert 'Reading' == sbac_assmt.claim_1_name
    assert 'Writing' == sbac_assmt.claim_2_name
    assert 'Listening' == sbac_assmt.claim_3_name
    assert 'Research & Inquiry' == sbac_assmt.claim_4_name
    assert 'Minimal Understanding' == sbac_assmt.perf_lvl_name_1
    assert 'Partial Understanding' == sbac_assmt.perf_lvl_name_2
    assert 'Adequate Understanding' == sbac_assmt.perf_lvl_name_3
    assert 'Thorough Understanding' == sbac_assmt.perf_lvl_name_4
    assert None == sbac_assmt.perf_lvl_name_5
    assert 1200 == sbac_assmt.overall_score_min
    assert 2400 == sbac_assmt.overall_score_max
    assert 1200 == sbac_assmt.claim_1_score_min
    assert 2400 == sbac_assmt.claim_1_score_max
    assert 0.2 == sbac_assmt.claim_1_score_weight
    assert 1200 == sbac_assmt.claim_2_score_min
    assert 2400 == sbac_assmt.claim_2_score_max
    assert 0.25 == sbac_assmt.claim_2_score_weight
    assert 1200 == sbac_assmt.claim_3_score_min
    assert 2400 == sbac_assmt.claim_3_score_max
    assert 0.25 == sbac_assmt.claim_3_score_weight
    assert 1200 == sbac_assmt.claim_4_score_min
    assert 2400 == sbac_assmt.claim_4_score_max
    assert 0.30 == sbac_assmt.claim_4_score_weight
    assert 'Below Standard' == sbac_assmt.claim_perf_lvl_name_1
    assert 'At/Near Standard' == sbac_assmt.claim_perf_lvl_name_2
    assert 'Above Standard' == sbac_assmt.claim_perf_lvl_name_3
    assert 1400 == sbac_assmt.overall_cut_point_1
    assert 1800 == sbac_assmt.overall_cut_point_2
    assert 2100 == sbac_assmt.overall_cut_point_3
    assert None == sbac_assmt.overall_cut_point_4
    assert 1600 == sbac_assmt.claim_cut_point_1
    assert 2000 == sbac_assmt.claim_cut_point_2
    assert datetime.date(2012, 9, 1) == sbac_assmt.from_date
    assert datetime.date(9999, 12, 31) == sbac_assmt.to_date
    assert False == sbac_assmt.most_recent


def test_generate_assessment_outcome():
    # Create the objects
    sbac_assmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA')
    sbac_state = hier_gen.generate_state('devel', 'Example State', 'ES')
    sbac_district = hier_gen.generate_district('Small Average', sbac_state)
    sbac_school = hier_gen.generate_school('Elementary School', sbac_district)
    sbac_class = enroll_gen.generate_class('Class', 'ELA', sbac_school)
    section = enroll_gen.generate_section(sbac_class, 'Section', 3, 2015)
    student = pop_gen.generate_student(sbac_school, 3, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(sbac_state, sbac_district, sbac_school)
    assmt_outcome = asmt_gen.generate_assessment_outcome(student, sbac_assmt, section, institution_hierarchy)

    # Tests
    valid_accomodation_codes = [0, 4, 5, 6, 7, 8, 9, 10]
    assert 1199 < assmt_outcome.overall_score < 2401
    assert 1199 < assmt_outcome.overall_score_range_min < 2401
    assert 1199 < assmt_outcome.overall_score_range_max < 2401
    assert 1199 < assmt_outcome.claim_1_score < 2401
    assert 1199 < assmt_outcome.claim_1_score_range_min < 2401
    assert 1199 < assmt_outcome.claim_1_score_range_max < 2401
    assert 1199 < assmt_outcome.claim_2_score < 2401
    assert 1199 < assmt_outcome.claim_2_score_range_min < 2401
    assert 1199 < assmt_outcome.claim_2_score_range_max < 2401
    assert 1199 < assmt_outcome.claim_3_score < 2401
    assert 1199 < assmt_outcome.claim_3_score_range_min < 2401
    assert 1199 < assmt_outcome.claim_3_score_range_max < 2401
    assert assmt_outcome.acc_asl_video_embed in valid_accomodation_codes
    assert assmt_outcome.acc_asl_human_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_braile_embed in valid_accomodation_codes
    assert assmt_outcome.acc_closed_captioning_embed in valid_accomodation_codes
    assert assmt_outcome.acc_text_to_speech_embed in valid_accomodation_codes
    assert assmt_outcome.acc_abacus_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_alternate_response_options_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_calculator_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_multiplication_table_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_alternate_response_options_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_read_aloud_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_scribe_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_speech_to_text_nonembed in valid_accomodation_codes
    assert assmt_outcome.acc_streamline_mode in valid_accomodation_codes