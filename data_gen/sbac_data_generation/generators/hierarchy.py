"""
Generate SBAC-specific hierarchy components.

@author: nestep
@date: Febraury 24, 2014
"""

import random

import data_generation.generators.hierarchy as general_hier_gen
import sbac_data_generation.config.cfg as sbac_config
import sbac_data_generation.generators.population as sbac_pop_gen

from sbac_data_generation.model.district import SBACDistrict
from sbac_data_generation.model.institutionhierarchy import InstitutionHierarchy
from sbac_data_generation.model.registrationsystem import SBACRegistrationSystem
from sbac_data_generation.model.school import SBACSchool
from sbac_data_generation.model.state import SBACState
from sbac_data_generation.model.group import SBACgroup


def generate_state(state_type, name, code, id_gen):
    """
    Generate a state of the given state type.

    @param state_type: The type of state to generate
    @param name: The name of the state
    @param code: The two-character code of the state
    @param id_gen: ID generator
    @returns: The state
    """
    # Run the general generator
    s = general_hier_gen.generate_state(state_type, name, code, sub_class=SBACState)

    # Set the SR guid
    s.guid_sr = id_gen.get_sr_uuid()

    return s


def generate_district(district_type, state: SBACState, id_gen):
    """
    Generate a district specified by the parameters.

    @param district_type: The type of district to generate
    @param state: The state the district belongs to
    @param id_gen: ID generator
    @returns: The district
    """
    # Run the general generator
    d = general_hier_gen.generate_district(district_type, state, sub_class=SBACDistrict)

    if random.random() < sbac_config.STUDENT_GROUPING_RATE:
        d.student_grouping = True
    # Set the SR guid
    d.guid_sr = id_gen.get_sr_uuid()

    return d


def generate_school(school_type, district: SBACDistrict, id_gen, interim_asmt_rate=sbac_config.INTERIM_ASMT_RATE):
    """
    Generate a school specified by the parameters.

    @param school_type: The type of school to generate
    @param district: The district the school belongs to
    @param id_gen: ID generator
    @param interim_asmt_rate: The rate (chance) that students in this school will take interim assessments
    @returns: The school
    """
    # Run the general generator
    s = general_hier_gen.generate_school(school_type, district, sub_class=SBACSchool)

    # Set the SR guid
    s.guid_sr = id_gen.get_sr_uuid()

    # Decide if the school takes interim assessments
    if random.random() < interim_asmt_rate:
        s.takes_interim_asmts = True

    return s


def generate_registration_system(year, extract_date, id_gen):
    """
    Generate a registration system.

    @param year: The academic year
    @param extract_date: The date of the data extract
    @param id_gen: ID generator
    @returns: The registration system
    """
    # Create the object
    ars = SBACRegistrationSystem()
    ars.guid = id_gen.get_uuid()
    ars.guid_sr = id_gen.get_sr_uuid()
    ars.sys_guid = id_gen.get_uuid()
    ars.academic_year = year
    ars.extract_date = extract_date
    ars.callback_url = 'SateTestReg.gov/StuReg/CallBack'

    return ars


def generate_institution_hierarchy(state: SBACState, district: SBACDistrict, school: SBACSchool, id_gen):
    """
    Generate a hierarchy institution object for a set of hierarchy institutions.

    @param state: The state in the hierarchy
    @param district: The district in the hierarchy
    @param school: The school in the hierarchy
    @param id_gen: ID generator
    @returns: An institution hierarchy object
    """
    # Create the object
    ih = InstitutionHierarchy()
    ih.rec_id = id_gen.get_rec_id('inst_hier')
    ih.guid = id_gen.get_uuid()
    ih.state = state
    ih.district = district
    ih.school = school
    ih.from_date = sbac_config.HIERARCHY_FROM_DATE
    ih.to_date = sbac_config.HIERARCHY_TO_DATE

    return ih


def generate_group(group_type, school: SBACSchool, id_gen):
    """
    Generate a group of given group_type and school
    @param group_type: Type of group
    @param id_gen: ID generator
    @returns: A group object
    """
    if group_type not in sbac_config.GROUP_TYPE:
        raise LookupError("Group type '" + str(group_type) + "' was not found")

    g = SBACgroup()
    g.type = group_type
    g.guid_sr = id_gen.get_sr_uuid()
    g.school = school
    g.id = id_gen.get_group_id('group')

    if group_type == 'section_based':
        g.name = "Homeroom " + str(g.id)
    elif group_type == 'staff_based':
        # Create a teacher object
        staff = sbac_pop_gen.generate_teaching_staff_member(school, id_gen)
        g.name = staff.name

    return g


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


def populate_schools_with_groupings(schools_with_groupings, id_gen):
    """
    Populate a dictionary of groups that associates each school with the concerned grades,
    subject and groups that a given school has.

    @param schools_with_groupings: Dictionary of schools to dictionary of grades, subject and grouping
    @param id_gen: ID generator
    """

    for school, grades in schools_with_groupings.items():
        num_groups = school.student_count_avg / sbac_config.STUDENTS_PER_GROUP
        for grade, subjects in grades.items():
            for subject, groups in subjects.items():
                for group_type, group_list in groups.items():
                    for i in range(int(num_groups)):
                        g = generate_group(group_type, school, id_gen)
                        group_list.append(g)
    return schools_with_groupings


def set_up_schools_with_groupings(schools, grades_of_concern):
    """
    Build a dictionary that associates each school with the concerned grades,
    subject and empty dict of groups that a given school has.

    @param schools: Schools to set up
    @param grades_of_concern: The overall set of grades that we are concerned with
    @returns: Dictionary of schools to dictionary of grades, subject and empty groupings
    """
    schools_with_groupings = {}
    for school in schools:
        grade_sub_groups = {}
        grades_for_school = grades_of_concern.intersection(school.config['grades'])

        for grade in grades_for_school:
            group_types = dict(zip(sbac_config.GROUP_TYPE,
                                   [[] for _ in range(len(sbac_config.GROUP_TYPE))]))
            grade_sub_groups[grade] = dict(zip(sbac_config.SUBJECTS,
                                               [dict(zip(sbac_config.GROUP_TYPE,
                                                         [[] for _ in range(len(sbac_config.GROUP_TYPE))]))
                                                for _ in range(len(sbac_config.SUBJECTS))]))
        schools_with_groupings[school] = grade_sub_groups

    return schools_with_groupings
