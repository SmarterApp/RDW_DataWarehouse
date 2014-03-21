"""
Generate SBAC-specific hierarchy components.

@author: nestep
@date: Febraury 24, 2014
"""

import random

import data_generation.generators.hierarchy as general_hier_gen
import data_generation.util.id_gen as general_id_gen
import sbac_data_generation.config.cfg as sbac_config
import sbac_data_generation.util.id_gen as sbac_id_gen

from sbac_data_generation.model.district import SBACDistrict
from sbac_data_generation.model.institutionhierarchy import InstitutionHierarchy
from sbac_data_generation.model.registrationsystem import SBACRegistrationSystem
from sbac_data_generation.model.school import SBACSchool
from sbac_data_generation.model.state import SBACState


def generate_state(state_type, name, code, save_to_mongo=True):
    """
    Generate a state of the given state type.

    @param state_type: The type of state to generate
    @param name: The name of the state
    @param code: The two-character code of the state
    @param save_to_mongo: If the new state object should be saved to Mongo
    @returns: The state
    """
    # Run the general generator
    s = general_hier_gen.generate_state(state_type, name, code, sub_class=SBACState)

    # Set the SR guid
    s.guid_sr = sbac_id_gen.get_sr_uuid()

    # Save the state
    if save_to_mongo:
        s.save()

    return s


def generate_district(district_type, state: SBACState, save_to_mongo=True):
    """
    Generate a district specified by the parameters.

    @param district_type: The type of district to generate
    @param state: The state the district belongs to
    @param save_to_mongo: If the new district object should be saved to Mongo
    @returns: The district
    """
    # Run the general generator
    d = general_hier_gen.generate_district(district_type, state, sub_class=SBACDistrict)

    # Set the SR guid
    d.guid_sr = sbac_id_gen.get_sr_uuid()

    # Save the district
    if save_to_mongo:
        d.save()

    return d


def generate_school(school_type, district: SBACDistrict, interim_asmt_rate=sbac_config.INTERIM_ASMT_RATE,
                    save_to_mongo=True):
    """
    Generate a school specified by the parameters.

    @param school_type: The type of school to generate
    @param district: The district the school belongs to
    @param interim_asmt_rate: The rate (chance) that students in this school will take interim assessments
    @param save_to_mongo: If the new school object should be saved to Mongo
    @returns: The school
    """
    # Run the general generator
    s = general_hier_gen.generate_school(school_type, district, sub_class=SBACSchool)

    # Set the SR guid
    s.guid_sr = sbac_id_gen.get_sr_uuid()

    # Decide if the school takes interim assessments
    if random.random() < interim_asmt_rate:
        s.takes_interim_asmts = True

    # Save the school
    if save_to_mongo:
        s.save()

    return s


def generate_registration_system(year, extract_date, save_to_mongo=True):
    """
    Generate a registration system.

    @param year: The academic year
    @param extract_date: The date of the data extract
    @param save_to_mongo: If the new registration system object should be saved to Mongo
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
    if save_to_mongo:
        ars.save()

    return ars


def generate_institution_hierarchy(state: SBACState, district: SBACDistrict, school: SBACSchool, save_to_mongo=True):
    """
    Generate a hierarchy institution object for a set of hierarchy institutions.

    @param state: The state in the hierarchy
    @param district: The district in the hierarchy
    @param school: The school in the hierarchy
    @param save_to_mongo: If the new hierarchy object should be saved to Mongo
    @returns: An institution hierarchy object
    """
    # Create the object
    ih = InstitutionHierarchy()
    ih.rec_id = general_id_gen.get_rec_id('inst_hier')
    ih.guid = general_id_gen.get_uuid()
    ih.state = state
    ih.district = district
    ih.school = school
    ih.from_date = sbac_config.HIERARCHY_FROM_DATE
    ih.to_date = sbac_config.HIERARCHY_TO_DATE

    # Save and return the object
    if save_to_mongo:
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