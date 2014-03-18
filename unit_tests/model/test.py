"""Unit tests for sbac_data_generation.model.* modules.

@author: nestep
@date: March 18, 2014
"""

import sbac_data_generation.generators.assessment as asmt_gen
import sbac_data_generation.generators.enrollment as enroll_gen
import sbac_data_generation.generators.hierarchy as hier_gen
import sbac_data_generation.generators.population as pop_gen


def test_assessment_outcome_get_object_set():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    ih = hier_gen.generate_institution_hierarchy(state, district, school)
    clss = enroll_gen.generate_class('Class', 'ELA', school)
    section = enroll_gen.generate_section(clss, 'Section', 3, 2014)
    asmt = asmt_gen.generate_assessment()
    student = pop_gen.generate_student(school, 3)
    asmt_out = asmt_gen.generate_assessment_outcome(student, asmt, section)

    # Tests
    objs = asmt_out.get_object_set()
    assert len(objs) == 8
    assert 'state' in objs
    assert objs['state'].guid == state.guid
    assert 'district' in objs
    assert objs['district'].guid == district.guid
    assert 'school' in objs
    assert objs['school'].guid == school.guid
    assert 'student' in objs
    assert objs['student'].guid == student.guid
    assert 'section' in objs
    assert objs['section'].guid == section.guid
    assert 'institution_hierarchy' in objs
    assert objs['institution_hierarchy'].guid == ih.guid
    assert 'assessment' in objs
    assert objs['assessment'].guid == asmt.guid
    assert 'assessment_outcome' in objs
    assert objs['assessment_outcome'].guid == asmt_out.guid


def test_institution_hierarchy_get_object_set():
    # Create necessary objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    ih = hier_gen.generate_institution_hierarchy(state, district, school)

    # Tests
    objs = ih.get_object_set()
    assert len(objs) == 4
    assert 'state' in objs
    assert objs['state'].guid == state.guid
    assert 'district' in objs
    assert objs['district'].guid == district.guid
    assert 'school' in objs
    assert objs['school'].guid == school.guid
    assert 'institution_hierarchy' in objs
    assert objs['institution_hierarchy'].guid == ih.guid


def test_registration_system_get_object_set():
    # Create necessary objects
    reg_sys = hier_gen.generate_registration_system(2015, '2014-02-25')

    # Tests
    objs = reg_sys.get_object_set()
    assert len(objs) == 1
    assert 'registration_system' in objs
    assert objs['registration_system'].guid == reg_sys.guid