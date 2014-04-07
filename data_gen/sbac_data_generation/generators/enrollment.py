"""
Generate enrollment elements that can be related to SBAC assessments.

@author: nestep
@date: February 25, 2014
"""

import datetime

import data_generation.generators.enrollment as general_enroll_gen

from sbac_data_generation.model.clss import SBACClass
from sbac_data_generation.model.enrollment import SBACEnrollment
from sbac_data_generation.model.school import SBACSchool
from sbac_data_generation.model.section import SBACSection
from sbac_data_generation.model.student import SBACStudent


def generate_class(name, subject, school: SBACSchool):
    """
    Generate a class for a subject in a school.

    @param name: The name of the class
    @param subject: The subject this class covers
    @param school: The school containing the class
    @returns: A class object
    """
    # Generate the general class
    s = general_enroll_gen.generate_class(name, subject, school, SBACClass)

    return s


def generate_section(clss: SBACClass, name, grade, id_gen, state, year=datetime.datetime.now().year):
    """
    Generate a section for a given class. This will also generate the necessary number of teaching staff for the
    section.

    @param clss: The class to create a section for
    @param name: The name of the section
    @param grade: The grade of students for the section
    @param id_gen: ID generator
    @param state: The state this section falls within
    @param year: The academic year this section is in
    @returns: A section object
    """
    # Generate the general section
    s = general_enroll_gen.generate_section(clss, name, grade, year, teachers_for_section=0, sub_class=SBACSection)

    # Add additional attributes
    s.rec_id = id_gen.get_rec_id('section')
    s.school = clss.school
    s.district = clss.school.district
    s.state = state

    return s


def generate_enrollment(section: SBACSection, student: SBACStudent, grade=None):
    """
    Generate an enrollment record linking a student with a section.

    @param section: The section the student is enrolled in
    @param student: The student enrolled in the section
    @param grade: The grade of the student at the time of enrollment (defaults to student current grade)
    @returns: An enrollment object
    """
    # Create the general enrollment
    e = general_enroll_gen.generate_enrollment(section, student, grade, sub_class=SBACEnrollment)

    return e