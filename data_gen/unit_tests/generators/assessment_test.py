"""
Unit tests for the sbac_data_generation.generators.assessement module.

@author: nestep
@date: March 18, 2014
"""

import datetime

from nose.tools import assert_raises

import data_generation.config.hierarchy as hier_config
import data_generation.config.population as pop_config
import sbac_data_generation.config.hierarchy as sbac_hier_config
import sbac_data_generation.config.population as sbac_pop_config
import sbac_data_generation.generators.assessment as asmt_gen
import sbac_data_generation.generators.hierarchy as hier_gen
import sbac_data_generation.generators.population as pop_gen
import sbac_data_generation.model.itemdata as item_lvl_data

from sbac_data_generation.util.id_gen import IDGen

ID_GEN = IDGen()


def setup_module():
    hier_config.STATE_TYPES.update(sbac_hier_config.STATE_TYPES)
    pop_config.DEMOGRAPHICS['california'] = sbac_pop_config.DEMOGRAPHICS['california']
    for grade, demo in sbac_pop_config.DEMOGRAPHICS['typical1'].items():
        if grade in pop_config.DEMOGRAPHICS['typical1']:
            pop_config.DEMOGRAPHICS['typical1'][grade].update(demo)


def test_generate_assessment():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.asmt_type == 'SUMMATIVE'
    assert asmt.period == 'Spring 2015'
    assert asmt.period_year == 2015
    assert asmt.version == 'V1'
    assert asmt.subject == 'Math'
    assert asmt.from_date == datetime.date(2015, 5, 15)
    assert asmt.to_date == datetime.date(9999, 12, 31)


def test_generate_item_data():
    item_data = item_lvl_data.SBACAssessmentOutcomeItemData(student_guid='0b43854416674ec8961b9db797bca2',
                                                            key='1938',
                                                            segment_id='(SBAC)SBAC-MG110PT-S2-ELA-7-Spring-2014-2015',
                                                            position='19', format='MC')

    assert item_data.student_guid == '0b43854416674ec8961b9db797bca2'
    assert item_data.key == 1938
    assert item_data.segment_id == '(SBAC)SBAC-MG110PT-S2-ELA-7-Spring-2014-2015'
    assert item_data.position == 19
    assert item_data.format == 'MC'


def test_generate_assessment_invalid_subject():
    assert_raises(KeyError, asmt_gen.generate_assessment, 'SUMMATIVE', 'Spring', 2015, 'Subject', ID_GEN,
                  claim_definitions={})


def test_generate_assessment_claims_ela():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    assert asmt.claim_1_name == 'Reading'
    assert asmt.claim_1_score_min == 1200
    assert asmt.claim_1_score_max == 2400
    assert asmt.claim_1_score_weight == .2
    assert asmt.claim_2_name == 'Writing'
    assert asmt.claim_2_score_min == 1200
    assert asmt.claim_2_score_max == 2400
    assert asmt.claim_2_score_weight == .25
    assert asmt.claim_3_name == 'Listening'
    assert asmt.claim_3_score_min == 1200
    assert asmt.claim_3_score_max == 2400
    assert asmt.claim_3_score_weight == .25
    assert asmt.claim_4_name == 'Research & Inquiry'
    assert asmt.claim_4_score_min == 1200
    assert asmt.claim_4_score_max == 2400
    assert asmt.claim_4_score_weight == .3


def test_generate_assessment_claims_math():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.claim_1_name == 'Concepts & Procedures'
    assert asmt.claim_1_score_min == 1200
    assert asmt.claim_1_score_max == 2400
    assert asmt.claim_1_score_weight == .4
    assert asmt.claim_2_name == 'Problem Solving and Modeling & Data Analysis'
    assert asmt.claim_2_score_min == 1200
    assert asmt.claim_2_score_max == 2400
    assert asmt.claim_2_score_weight == .45
    assert asmt.claim_3_name == 'Communicating Reasoning'
    assert asmt.claim_3_score_min == 1200
    assert asmt.claim_3_score_max == 2400
    assert asmt.claim_3_score_weight == .15
    assert asmt.claim_4_name is None
    assert asmt.claim_4_score_min is None
    assert asmt.claim_4_score_max is None
    assert asmt.claim_4_score_weight is None


def test_generate_assessment_perf_lvl_names():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.perf_lvl_name_1 == 'Minimal Understanding'
    assert asmt.perf_lvl_name_2 == 'Partial Understanding'
    assert asmt.perf_lvl_name_3 == 'Adequate Understanding'
    assert asmt.perf_lvl_name_4 == 'Thorough Understanding'
    assert asmt.perf_lvl_name_5 is None


def test_generate_assessment_claim_perf_lvl_names():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.claim_perf_lvl_name_1 == 'Below Standard'
    assert asmt.claim_perf_lvl_name_2 == 'At/Near Standard'
    assert asmt.claim_perf_lvl_name_3 == 'Above Standard'


def test_generate_assessment_cut_points():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.overall_cut_point_1 == 1400
    assert asmt.overall_cut_point_2 == 1800
    assert asmt.overall_cut_point_3 == 2100
    assert asmt.overall_cut_point_4 is None


def test_generate_assessment_overall_scores():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.overall_score_min == 1200
    assert asmt.overall_score_max == 2400
    assert asmt.overall_cut_point_2 == 1800
    assert asmt.overall_cut_point_3 == 2100
    assert asmt.overall_cut_point_4 is None


def test_generate_assessment_summative_effective_date():
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.period_year == 2015
    assert asmt.effective_date == datetime.date(2015, 5, 15)


def test_generate_assessment_interim_fall_effective_date():
    asmt = asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'Math', ID_GEN)
    assert asmt.period_year == 2015
    assert asmt.effective_date == datetime.date(2014, 9, 15)


def test_generate_assessment_interim_winter_effective_date():
    asmt = asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'Math', ID_GEN)
    assert asmt.period_year == 2015
    assert asmt.effective_date == datetime.date(2014, 12, 15)


def test_generate_assessment_interim_spring_effective_date():
    asmt = asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'Math', ID_GEN)
    assert asmt.period_year == 2015
    assert asmt.effective_date == datetime.date(2015, 3, 15)


def test_generate_assessment_outcome_default_status():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Test
    assert asmt_out.result_status == 'C'


def test_generate_assessment_outcome_scores():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Tests
    assert 1200 <= asmt_out.overall_score <= 2400
    assert 1200 <= asmt_out.overall_score_range_min <= 2400
    assert 1200 <= asmt_out.overall_score_range_max <= 2400
    assert 1200 <= asmt_out.claim_1_score <= 2400
    assert 1200 <= asmt_out.claim_1_score_range_min <= 2400
    assert 1200 <= asmt_out.claim_1_score_range_max <= 2400
    assert 1200 <= asmt_out.claim_2_score <= 2400
    assert 1200 <= asmt_out.claim_2_score_range_min <= 2400
    assert 1200 <= asmt_out.claim_2_score_range_max <= 2400
    assert 1200 <= asmt_out.claim_3_score <= 2400
    assert 1200 <= asmt_out.claim_3_score_range_min <= 2400
    assert 1200 <= asmt_out.claim_3_score_range_max <= 2400


def test_generate_assessment_outcome_summative_taken_date():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Test
    assert asmt_out.date_taken == datetime.date(2015, 5, 15)


def test_generate_assessment_outcome_interim_fall_taken_date():
    # Create objects
    asmt = asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'Math', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Test
    assert asmt_out.date_taken == datetime.date(2014, 9, 15)


def test_generate_assessment_outcome_interim_winter_taken_date():
    # Create objects
    asmt = asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'Math', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Test
    assert asmt_out.date_taken == datetime.date(2014, 12, 15)


def test_generate_assessment_outcome_interim_spring_taken_date():
    # Create objects
    asmt = asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'Math', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Test
    assert asmt_out.date_taken == datetime.date(2015, 3, 15)


def test_generate_assessment_outcome_accommodations_ela():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Tests
    assert 4 <= asmt_out.acc_asl_video_embed <= 10
    assert 4 <= asmt_out.acc_asl_human_nonembed <= 10
    assert 4 <= asmt_out.acc_braile_embed <= 10
    assert 4 <= asmt_out.acc_closed_captioning_embed <= 10
    assert 4 <= asmt_out.acc_text_to_speech_embed <= 10
    assert asmt_out.acc_abacus_nonembed == 0
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 10
    assert asmt_out.acc_calculator_nonembed == 0
    assert asmt_out.acc_multiplication_table_nonembed == 0
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 10
    assert 4 <= asmt_out.acc_read_aloud_nonembed <= 10
    assert 4 <= asmt_out.acc_scribe_nonembed <= 10
    assert 4 <= asmt_out.acc_speech_to_text_nonembed <= 10
    assert 4 <= asmt_out.acc_streamline_mode <= 10


def test_generate_assessment_outcome_accommodations_math():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'Math', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, state, 2015)
    institution_hierarchy = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, institution_hierarchy, ID_GEN)

    # Tests
    assert 4 <= asmt_out.acc_asl_video_embed <= 10
    assert 4 <= asmt_out.acc_asl_human_nonembed <= 10
    assert 4 <= asmt_out.acc_braile_embed <= 10
    assert asmt_out.acc_closed_captioning_embed == 0
    assert asmt_out.acc_text_to_speech_embed == 0
    assert 4 <= asmt_out.acc_abacus_nonembed <= 10
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 10
    assert 4 <= asmt_out.acc_calculator_nonembed <= 10
    assert 4 <= asmt_out.acc_multiplication_table_nonembed <= 10
    assert 4 <= asmt_out.acc_alternate_response_options_nonembed <= 10
    assert asmt_out.acc_read_aloud_nonembed == 0
    assert asmt_out.acc_scribe_nonembed == 0
    assert asmt_out.acc_speech_to_text_nonembed == 0
    assert 4 <= asmt_out.acc_streamline_mode <= 10


def test_pick_performance_levels():
    cut_points = [1600, 1800, 2100]
    assert asmt_gen._pick_performance_level(1390, cut_points) == 1
    assert asmt_gen._pick_performance_level(1790, cut_points) == 2
    assert asmt_gen._pick_performance_level(1810, cut_points) == 3
    assert asmt_gen._pick_performance_level(2110, cut_points) == 4


def test_pick_performance_level_on_cut_points():
    cut_points = [1600, 1800, 2100]
    assert asmt_gen._pick_performance_level(1600, cut_points) == 2
    assert asmt_gen._pick_performance_level(1800, cut_points) == 3
    assert asmt_gen._pick_performance_level(2100, cut_points) == 4


def test_pick_default_accommodation_code_negative():
    assert_raises(ValueError, asmt_gen._pick_default_accommodation_code, -1)


def test_pick_default_accommodation_code_too_big():
    assert_raises(ValueError, asmt_gen._pick_default_accommodation_code, 5)


def test_pick_default_accommodation_code_0():
    code = asmt_gen._pick_default_accommodation_code(0)
    assert code == 0


def test_pick_default_accommodation_code_four():
    assert 4 <= asmt_gen._pick_default_accommodation_code(4) <= 10
