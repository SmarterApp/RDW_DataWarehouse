"""
Unit tests for the project.sbac.generators.enrollment module.

@author: nestep
@date: March 20, 2014
"""

import datetime

from nose.tools import assert_is_instance

import sbac_data_generation.generators.enrollment as enroll_gen
import sbac_data_generation.generators.hierarchy as hier_gen
import sbac_data_generation.generators.population as pop_gen

from sbac_data_generation.model.clss import SBACClass
from sbac_data_generation.model.enrollment import SBACEnrollment
from sbac_data_generation.model.section import SBACSection


def test_generate_class():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    clss = enroll_gen.generate_class('Class 01', 'Math', school)

    # Tests
    assert_is_instance(clss, SBACClass)
    assert clss.name == 'Class 01'
    assert clss.subject == 'Math'
    assert clss.school == school


def test_generate_section_defaults():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    clss = enroll_gen.generate_class('Class 01', 'Math', school)
    section = enroll_gen.generate_section(clss, 'Section 01', 3)

    # Tests
    assert_is_instance(section, SBACSection)
    assert section.clss == clss
    assert section.name == 'Section 01'
    assert section.grade == 3
    assert section.from_date == datetime.date(datetime.datetime.now().year, 9, 1)
    assert section.to_date == datetime.date(datetime.datetime.now().year + 1, 6, 1)


def test_generate_section_specific_year():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    clss = enroll_gen.generate_class('Class 01', 'Math', school)
    section = enroll_gen.generate_section(clss, 'Section 01', 3, 2017)

    # Tests
    assert_is_instance(section, SBACSection)
    assert section.clss == clss
    assert section.name == 'Section 01'
    assert section.grade == 3
    assert section.from_date == datetime.date(2017, 9, 1)
    assert section.to_date == datetime.date(2018, 6, 1)


def test_generate_enrollment_defaults():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    student = pop_gen.generate_student(school, 3)
    clss = enroll_gen.generate_class('Class 01', 'Math', school)
    section = enroll_gen.generate_section(clss, 'Section 01', 3)
    enrollment = enroll_gen.generate_enrollment(section, student)

    # Tests
    assert_is_instance(enrollment, SBACEnrollment)
    assert enrollment.section == section
    assert enrollment.student == student
    assert enrollment.grade == 3


def test_generate_enrollment_grade():
    # Create objects
    state = hier_gen.generate_state('devel', 'Example State', 'ES')
    district = hier_gen.generate_district('Small Average', state)
    school = hier_gen.generate_school('Elementary School', district)
    student = pop_gen.generate_student(school, 3)
    clss = enroll_gen.generate_class('Class 01', 'Math', school)
    section = enroll_gen.generate_section(clss, 'Section 01', 3)
    enrollment = enroll_gen.generate_enrollment(section, student, 5)

    # Tests
    assert_is_instance(enrollment, SBACEnrollment)
    assert enrollment.section == section
    assert enrollment.student == student
    assert enrollment.grade == 5