"""
Generate SBAC-specific hierarchy components.

@author: nestep
@date: Febraury 24, 2014
"""

import random

import general.generators.hierarchy as general_hier_gen
import general.util.id_gen as general_id_gen
import project.sbac.config.cfg as sbac_config
import project.sbac.util.id_gen as sbac_id_gen

from general.model.district import District
from general.model.school import School
from general.model.state import State
from project.sbac.model.district import SBACDistrict
from project.sbac.model.institutionhierarchy import InstitutionHierarchy
from project.sbac.model.registrationsystem import SBACRegistrationSystem
from project.sbac.model.school import SBACSchool
from project.sbac.model.state import SBACState


def generate_state(state_type, name, code):
    """
    Generate a state of the given state type.

    @param state_type: The type of state to generate
    @param name: The name of the state
    @param code: The two-character code of the state
    @returns: The state
    """
    # Run the general generator
    s = general_hier_gen.generate_state(state_type, name, code, SBACState)

    # Set the SR guid
    s.guid_sr = sbac_id_gen.get_sr_uuid()

    # Save the state
    s.save()

    return s


def generate_district(district_type, state: State):
    """
    Generate a district specified by the parameters.

    @param district_type: The type of district to generate
    @param state: The state the district belongs to
    @returns: The district
    """
    # Run the general generator
    d = general_hier_gen.generate_district(district_type, state, SBACDistrict)

    # Set the SR guid
    d.guid_sr = sbac_id_gen.get_sr_uuid()

    # Save the district
    d.save()

    return d


def generate_school(school_type, district: District):
    """
    Generate a school specified by the parameters.

    @param school_type: The type of school to generate
    @param district: The district the school belongs to
    @returns: The school
    """
    # Run the general generator
    s = general_hier_gen.generate_school(school_type, district, SBACSchool)

    # Set the SR guid
    s.guid_sr = sbac_id_gen.get_sr_uuid()

    # Decide if the school takes interim assessments
    if random.random() < sbac_config.INTERIM_ASMT_RATE:
        s.takes_interim_asmts = True

    # Save the school
    s.save()

    return s


def generate_registration_system(year, extract_date):
    """
    Generate a registration system.

    @param year: The academic year
    @param extract_date: The date of the data extract
    @returns: The registration system
    """
    # Create the object
    ars = SBACRegistrationSystem()
    ars.guid = general_id_gen.get_uuid()
    ars.sys_guid = general_id_gen.get_uuid()
    ars.academic_year = year
    ars.extract_date = extract_date
    ars.callback_url = 'SateTestReg.gov/StuReg/CallBack'

    # Save the registration system
    ars.save()

    return ars


def generate_institution_hierarchy(state: State, district: District, school: School):
    """
    Generate a hierarchy institution object for a set of hierarchy institutions.

    @param state: The state in the hierarchy
    @param district: The district in the hierarchy
    @param school: The school in the hierarchy
    @returns: An institution hierarchy object
    """
    # Create the object
    ih = InstitutionHierarchy()
    ih.rec_id = general_id_gen.get_rec_id()
    ih.guid = general_id_gen.get_uuid()
    ih.state = state
    ih.district = district
    ih.school = school
    ih.from_date = sbac_config.HIERARCHY_FROM_DATE
    ih.to_date = sbac_config.HIERARCHY_TO_DATE
    ih.most_recent = sbac_config.HIERARCHY_MOST_RECENT

    # Save and return the object
    ih.save()

    return ih


def sort_schools_by_grade(schools):
    """
    Sort a list of schools by grades available in the school.

    @param schools: Schools to sort
    @returns: Dictionary of sorted schools
    """
    schools_by_grade = {}
    for school in schools:
        for grade in school.grades:
            if grade not in schools_by_grade:
                schools_by_grade[grade] = []
            schools_by_grade[grade].append(school)
    return schools_by_grade


def set_up_schools_with_grades(schools, grades_of_concern):
    """
    Build a dictionary that associates each school with the grades of concern that a given school has.

    @param schools: Schools to set up
    @param grades_of_concern: The overall set of grades that we are concerned with
    @returns: Dictionary of schools to dictionary of grades
    """
    schools_with_grades = {}
    for school in schools:
        grades_for_school = grades_of_concern.intersection(school.config['grades'])
        schools_with_grades[school] = dict(zip(grades_for_school, [[] for _ in range(len(grades_for_school))]))
    return schools_with_grades