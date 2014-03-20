"""
Generate enrollment elements that can be related to SBAC assessments.

@author: nestep
@date: February 25, 2014
"""

import datetime

import data_generation.generators.enrollment as general_enroll_gen
import data_generation.util.id_gen as id_gen

from sbac_data_generation.model.clss import SBACClass
from sbac_data_generation.model.enrollment import SBACEnrollment
from sbac_data_generation.model.school import SBACSchool
from sbac_data_generation.model.section import SBACSection
from sbac_data_generation.model.student import SBACStudent


def generate_class(name, subject, school: SBACSchool, save_to_mongo=True):
    """
    Generate a class for a subject in a school.

    @param name: The name of the class
    @param subject: The subject this class covers
    @param school: The school containing the class
    @param save_to_mongo: If the newly created class should be saved to Mongo
    @returns: A class object
    """
    # Generate the general class
    s = general_enroll_gen.generate_class(name, subject, school, SBACClass)

    # Save and return the section
    if save_to_mongo:
        s.save()

    return s


def generate_section(clss: SBACClass, name, grade, year=datetime.datetime.now().year, most_recent=False,
                     save_to_mongo=True):
    """
    Generate a section for a given class. This will also generate the necessary number of teaching staff for the
    section.

    @param clss: The class to create a section for
    @param name: The name of the section
    @param grade: The grade of students for the section
    @param year: The academic year this section is in
    @param most_recent: If the section is the most recent section for this grade and class
    @param save_to_mongo: If the newly created section should be saved to Mongo
    @returns: A section object
    """
    # Generate the general section
    s = general_enroll_gen.generate_section(clss, name, grade, year, most_recent, sub_class=SBACSection)

    # Add additional attributes
    s.rec_id = id_gen.get_rec_id('section')

    # Save and return the section
    if save_to_mongo:
        s.save()

    return s


def generate_enrollment(section: SBACSection, student: SBACStudent, grade=None, save_to_mongo=True):
    """
    Generate an enrollment record linking a student with a section.

    @param section: The section the student is enrolled in
    @param student: The student enrolled in the section
    @param grade: The grade of the student at the time of enrollment (defaults to student current grade)
    @param save_to_mongo: If the newly created section should be saved to Mongo
    @returns: An enrollment object
    """
    # Create the general enrollment
    e = general_enroll_gen.generate_enrollment(section, student, grade, sub_class=SBACEnrollment)

    # Save and return the enrollment
    if save_to_mongo:
        e.save()

    return e