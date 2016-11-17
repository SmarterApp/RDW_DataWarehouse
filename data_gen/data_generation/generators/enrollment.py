"""Generate enrollment elements.

:author: nestep
:date: February 25, 2014
"""

import datetime

import data_generation.config.enrollment as general_enroll_config
import data_generation.generators.population as general_pop_gen
import data_generation.util.id_gen as id_gen

from data_generation.model.clss import Class
from data_generation.model.enrollment import Enrollment
from data_generation.model.school import School
from data_generation.model.section import Section
from data_generation.model.student import Student


def generate_class(name, subject, school: School, sub_class=None):
    """Generate a class for a subject in a school.

    :param name: The name of the class
    :param subject: The subject this class covers
    :param school: The school containing the class
    :param sub_class: The sub-class of class to create (if requested, must be subclass of Class)
    :returns: A class object
    """
    # Create the class
    c = Class() if sub_class is None else sub_class()
    c.guid = id_gen.get_uuid()
    c.school = school
    c.name = name
    c.subject = subject

    return c


def generate_section(clss: Class, name, grade, year=datetime.datetime.now().year, most_recent=False,
                     teachers_for_section=general_enroll_config.TEACHERS_PER_SECTION, sub_class=None):
    """Generate a section for a given class. This will also generate the necessary number of teaching staff for the
    section.

    :param clss: The class to create a section for
    :param name: The name of the section
    :param grade: The grade of students for the section
    :param year: The academic year this section is in
    :param most_recent: If the section is the most recent section for this grade and class
    :param teachers_for_section: The number of teachers to generate for this section
    :param sub_class: The sub-class of section to create (if requested, must be subclass of Section)
    :returns: A section object
    """
    # Create the section
    s = Section() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.clss = clss
    s.name = name
    s.grade = grade

    s.from_date = datetime.date(year, 9, 1)
    s.most_recent = most_recent
    if not most_recent:
        s.to_date = datetime.date(year + 1, 6, 1)

    # Generate teaching staff
    for i in range(teachers_for_section):
        s.teachers.append(general_pop_gen.generate_teaching_staff_member(clss.school))

    return s


def generate_enrollment(section: Section, student: Student, grade=None, sub_class=None):
    """Generate an enrollment record linking a student with a section.

    :param section: The section the student is enrolled in
    :param student: The student enrolled in the section
    :param grade: The grade of the student at the time of enrollment (defaults to student current grade)
    :param sub_class: The sub-class of enrollment to create (if requested, must be subclass of Enrollment)
    :returns: An enrollment object
    """
    # Create the enrollment
    e = Enrollment() if sub_class is None else sub_class()
    e.guid = id_gen.get_uuid()
    e.section = section
    e.student = student
    e.grade = grade if grade is not None else student.grade

    return e
