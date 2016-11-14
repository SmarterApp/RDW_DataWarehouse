"""
Unit tests for the generate_data module.

@author: nestep
@date: March 20, 2014
"""

import datetime
import os

from nose.tools import assert_raises

import generate_data as generate_data
import sbac_data_generation.generators.assessment as asmt_gen
import sbac_data_generation.generators.hierarchy as hier_gen
import sbac_data_generation.generators.population as pop_gen

from sbac_data_generation.util.id_gen import IDGen
import sbac_data_generation.config.cfg as sbac_config

ID_GEN = IDGen()


def setup_module():
    # Verify output directory exists (some tested methods will write to disk)
    if not os.path.exists(generate_data.OUT_PATH_ROOT):
        os.makedirs(generate_data.OUT_PATH_ROOT)


def test_set_configuration_exception():
    assert_raises(ValueError, generate_data.assign_configuration_options, 'Unknown', 'North Carolina', 'NC',
                  'typical_1')


def test_set_configuration_state():
    # Set the configuration
    generate_data.assign_configuration_options('regular', 'North Carolina', 'NC', 'typical_1')

    # Tests
    assert generate_data.STATES[0]['name'] == 'North Carolina'
    assert generate_data.STATES[0]['code'] == 'NC'
    assert generate_data.STATES[0]['type'] == 'typical_1'


def test_set_configuration_regular():
    # Set the configuration
    generate_data.assign_configuration_options('regular', 'North Carolina', 'NC', 'typical_1')

    # Tests
    assert len(generate_data.YEARS) == 3
    assert 2015 in generate_data.YEARS
    assert 2016 in generate_data.YEARS
    assert 2017 in generate_data.YEARS
    assert len(generate_data.ASMT_YEARS) == 3
    assert 2015 in generate_data.ASMT_YEARS
    assert 2016 in generate_data.ASMT_YEARS
    assert 2017 in generate_data.ASMT_YEARS
    assert len(generate_data.INTERIM_ASMT_PERIODS) == 3
    assert 'Fall' in generate_data.INTERIM_ASMT_PERIODS
    assert 'Winter' in generate_data.INTERIM_ASMT_PERIODS
    assert 'Spring' in generate_data.INTERIM_ASMT_PERIODS
    assert generate_data.NUMBER_REGISTRATION_SYSTEMS == 1


def test_create_assessment_object():
    asmt = generate_data.create_assessment_object('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN, generate_item_level=False)
    assert asmt.asmt_type == 'SUMMATIVE'
    assert asmt.subject == 'ELA'


def test_create_assessment_object_summative():
    asmt = generate_data.create_assessment_object('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN, generate_item_level=False)
    assert asmt.period_year == 2015
    assert asmt.period == 'Spring 2015'
    assert asmt.effective_date == datetime.date(2015, 5, 15)
    assert asmt.from_date == datetime.date(2015, 5, 15)
    assert asmt.to_date == datetime.date(9999, 12, 31)


def test_create_assessment_object_interim_fall():
    asmt = generate_data.create_assessment_object('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN,
                                                  generate_item_level=False)
    assert asmt.period_year == 2015
    assert asmt.period == 'Fall 2014'
    assert asmt.effective_date == datetime.date(2014, 9, 15)
    assert asmt.from_date == datetime.date(2014, 9, 15)
    assert asmt.to_date == datetime.date(9999, 12, 31)


def test_create_assessment_object_interim_winter():
    asmt = generate_data.create_assessment_object('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN,
                                                  generate_item_level=False)
    assert asmt.period_year == 2015
    assert asmt.period == 'Winter 2014'
    assert asmt.effective_date == datetime.date(2014, 12, 15)
    assert asmt.from_date == datetime.date(2014, 12, 15)
    assert asmt.to_date == datetime.date(9999, 12, 31)


def test_create_assessment_object_interim_spring():
    asmt = generate_data.create_assessment_object('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN,
                                                  generate_item_level=False)
    assert asmt.period_year == 2015
    assert asmt.period == 'Spring 2015'
    assert asmt.effective_date == datetime.date(2015, 3, 15)
    assert asmt.from_date == datetime.date(2015, 3, 15)
    assert asmt.to_date == datetime.date(9999, 12, 31)


def test_create_assessment_object_item_data():
    asmt = generate_data.create_assessment_object('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN,
                                                  generate_item_level=True)
    assert len(asmt.item_bank) == sbac_config.ASMT_ITEM_BANK_SIZE


def test_create_assessment_object_no_item_data():
    asmt = generate_data.create_assessment_object('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN,
                                                  generate_item_level=False)
    assert len(asmt.item_bank) == 0


def test_create_assessment_outcome_object_item_data():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=0,
                                                   retake_rate=0, delete_rate=0, update_rate=0,
                                                   generate_item_level=True)

    # Tests
    assert len(outcomes) == 1
    assert len(outcomes[asmt.guid_sr][0].item_level_data) == sbac_config.ITEMS_PER_ASMT


def test_create_assessment_outcome_object_skipped():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=1,
                                                   retake_rate=0, delete_rate=0, update_rate=0,
                                                   generate_item_level=False)

    # Tests
    assert len(outcomes) == 0


def test_create_assessment_outcome_object_one_active_result():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=0,
                                                   retake_rate=0, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid_sr][0].result_status == 'C'
    assert outcomes[asmt.guid_sr][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_object_retake_results():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=0,
                                                   retake_rate=1, delete_rate=0, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid_sr][0].result_status == 'I'
    assert outcomes[asmt.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt.guid_sr][1].result_status == 'C'
    assert outcomes[asmt.guid_sr][1].date_taken == datetime.date(2015, 5, 20)


def test_create_assessment_outcome_object_one_deleted_result():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=0,
                                                   retake_rate=0, delete_rate=1, update_rate=0)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid_sr][0].result_status == 'D'
    assert outcomes[asmt.guid_sr][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_object_update_no_second_delete_results():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=0,
                                                   retake_rate=0, delete_rate=0, update_rate=1)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid_sr][0].result_status == 'D'
    assert outcomes[asmt.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt.guid_sr][1].result_status == 'C'
    assert outcomes[asmt.guid_sr][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_object_update_second_delete_results():
    # Create objects
    asmt = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_object(student, asmt, inst_hier, ID_GEN, outcomes, skip_rate=0,
                                                   retake_rate=0, delete_rate=1, update_rate=1)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt.guid_sr][0].result_status == 'D'
    assert outcomes[asmt.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt.guid_sr][1].result_status == 'D'
    assert outcomes[asmt.guid_sr][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interims_skipped():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, [], inst_hier, ID_GEN, outcomes,
                                                    skip_rate=1, retake_rate=0, delete_rate=0, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 0


def test_create_assessment_outcome_objects_no_interims_one_active_result():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, [], inst_hier, ID_GEN, outcomes,
                                                    skip_rate=0, retake_rate=0, delete_rate=0, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'C'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interims_retake_results():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, [], inst_hier, ID_GEN, outcomes,
                                                    skip_rate=0, retake_rate=1, delete_rate=0, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'I'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid_sr][1].result_status == 'C'
    assert outcomes[asmt_summ.guid_sr][1].date_taken == datetime.date(2015, 5, 20)


def test_create_assessment_outcome_objects_no_interim_one_deleted_result():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, [], inst_hier, ID_GEN, outcomes,
                                                    skip_rate=0, retake_rate=0, delete_rate=1, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interim_update_no_second_delete_results():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, [], inst_hier, ID_GEN, outcomes,
                                                    skip_rate=0, retake_rate=0, delete_rate=0, update_rate=1,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid_sr][1].result_status == 'C'
    assert outcomes[asmt_summ.guid_sr][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_no_interim_update_second_delete_results():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, [], inst_hier, ID_GEN, outcomes,
                                                    skip_rate=0, retake_rate=0, delete_rate=1, update_rate=1,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 1
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid_sr][1].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][1].date_taken == datetime.date(2015, 5, 15)


def test_create_assessment_outcome_objects_interims_skipped():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    interim_asmts = [asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, ID_GEN,
                                                    outcomes, skip_rate=1, retake_rate=0, delete_rate=0, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 0


def test_create_assessment_outcome_objects_interims_one_active_result():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    interim_asmts = [asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, ID_GEN,
                                                    outcomes, skip_rate=0, retake_rate=0, delete_rate=0, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 4
    assert outcomes[asmt_summ.guid_sr][0].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'C'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][0].result_status == 'C'
    assert outcomes[interim_asmts[0].guid_sr][0].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[1].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][0].result_status == 'C'
    assert outcomes[interim_asmts[1].guid_sr][0].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[2].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][0].result_status == 'C'
    assert outcomes[interim_asmts[2].guid_sr][0].date_taken == datetime.date(2015, 3, 15)


def test_create_assessment_outcome_objects_interims_retake_results():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    interim_asmts = [asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, ID_GEN,
                                                    outcomes, skip_rate=0, retake_rate=1, delete_rate=0, update_rate=0,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 4
    assert outcomes[asmt_summ.guid_sr][0].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'I'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid_sr][1].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][1].result_status == 'C'
    assert outcomes[asmt_summ.guid_sr][1].date_taken == datetime.date(2015, 5, 20)
    assert outcomes[interim_asmts[0].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][0].result_status == 'I'
    assert outcomes[interim_asmts[0].guid_sr][0].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[0].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][1].result_status == 'C'
    assert outcomes[interim_asmts[0].guid_sr][1].date_taken == datetime.date(2014, 9, 20)
    assert outcomes[interim_asmts[1].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][0].result_status == 'I'
    assert outcomes[interim_asmts[1].guid_sr][0].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[1].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][1].result_status == 'C'
    assert outcomes[interim_asmts[1].guid_sr][1].date_taken == datetime.date(2014, 12, 20)
    assert outcomes[interim_asmts[2].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][0].result_status == 'I'
    assert outcomes[interim_asmts[2].guid_sr][0].date_taken == datetime.date(2015, 3, 15)
    assert outcomes[interim_asmts[2].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][1].result_status == 'C'
    assert outcomes[interim_asmts[2].guid_sr][1].date_taken == datetime.date(2015, 3, 20)


def test_create_assessment_outcome_objects_interim_one_deleted_result():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    interim_asmts = [asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, ID_GEN,
                                                    outcomes, skip_rate=0, retake_rate=0, delete_rate=1, update_rate=0)

    # Tests
    assert len(outcomes) == 4
    assert outcomes[asmt_summ.guid_sr][0].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[0].guid_sr][0].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[1].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[1].guid_sr][0].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[2].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[2].guid_sr][0].date_taken == datetime.date(2015, 3, 15)


def test_create_assessment_outcome_objects_interim_update_no_second_delete_results():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    interim_asmts = [asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, ID_GEN,
                                                    outcomes, skip_rate=0, retake_rate=0, delete_rate=0, update_rate=1,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 4
    assert outcomes[asmt_summ.guid_sr][0].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid_sr][1].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][1].result_status == 'C'
    assert outcomes[asmt_summ.guid_sr][1].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[0].guid_sr][0].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[0].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][1].result_status == 'C'
    assert outcomes[interim_asmts[0].guid_sr][1].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[1].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[1].guid_sr][0].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[1].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][1].result_status == 'C'
    assert outcomes[interim_asmts[1].guid_sr][1].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[2].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[2].guid_sr][0].date_taken == datetime.date(2015, 3, 15)
    assert outcomes[interim_asmts[2].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][1].result_status == 'C'
    assert outcomes[interim_asmts[2].guid_sr][1].date_taken == datetime.date(2015, 3, 15)


def test_create_assessment_outcome_objects_interim_update_second_delete_results():
    # Create objects
    asmt_summ = asmt_gen.generate_assessment('SUMMATIVE', 'Spring', 2015, 'ELA', ID_GEN)
    interim_asmts = [asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Fall', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Winter', 2015, 'ELA', ID_GEN),
                     asmt_gen.generate_assessment('INTERIM COMPREHENSIVE', 'Spring', 2015, 'ELA', ID_GEN)]
    state = hier_gen.generate_state('devel', 'Example State', 'ES', ID_GEN)
    district = hier_gen.generate_district('Small Average', state, ID_GEN)
    school = hier_gen.generate_school('Elementary School', district, ID_GEN)
    student = pop_gen.generate_student(school, 3, ID_GEN, 2015)
    inst_hier = hier_gen.generate_institution_hierarchy(state, district, school, ID_GEN)
    outcomes = {}

    # Create outcomes
    generate_data.create_assessment_outcome_objects(student, asmt_summ, interim_asmts, inst_hier, ID_GEN,
                                                    outcomes, skip_rate=0, retake_rate=0, delete_rate=1, update_rate=1,
                                                    generate_item_level=False)

    # Tests
    assert len(outcomes) == 4
    assert outcomes[asmt_summ.guid_sr][0].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][0].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][0].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[asmt_summ.guid_sr][1].assessment.asmt_type == 'SUMMATIVE'
    assert outcomes[asmt_summ.guid_sr][1].result_status == 'D'
    assert outcomes[asmt_summ.guid_sr][1].date_taken == datetime.date(2015, 5, 15)
    assert outcomes[interim_asmts[0].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[0].guid_sr][0].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[0].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[0].guid_sr][1].result_status == 'D'
    assert outcomes[interim_asmts[0].guid_sr][1].date_taken == datetime.date(2014, 9, 15)
    assert outcomes[interim_asmts[1].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[1].guid_sr][0].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[1].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[1].guid_sr][1].result_status == 'D'
    assert outcomes[interim_asmts[1].guid_sr][1].date_taken == datetime.date(2014, 12, 15)
    assert outcomes[interim_asmts[2].guid_sr][0].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][0].result_status == 'D'
    assert outcomes[interim_asmts[2].guid_sr][0].date_taken == datetime.date(2015, 3, 15)
    assert outcomes[interim_asmts[2].guid_sr][1].assessment.asmt_type == 'INTERIM COMPREHENSIVE'
    assert outcomes[interim_asmts[2].guid_sr][1].result_status == 'D'
    assert outcomes[interim_asmts[2].guid_sr][1].date_taken == datetime.date(2015, 3, 15)
