"""
Generate enrollment elements that can be related to SBAC assessments.

@author: nestep
@date: February 25, 2014
"""

import datetime

import general.generators.enrollment as general_enroll_gen
import general.util.id_gen as id_gen

from general.model.clss import Class
from project.sbac.model.section import SBACSection


def generate_section(clss: Class, name, grade, year=datetime.datetime.now().year, most_recent=None):
    """
    Generate a section for a given class. This will also generate the necessary number of teaching staff for the
    section.

    @param clss: The class to create a section for
    @param name: The name of the section
    @param grade: The grade of students for the section
    @param year: The academic year this section is in
    @param most_recent: If the section is the most recent section for this grade and class
    @returns: A section object
    """
    # Generate the general section
    s = general_enroll_gen.generate_section(clss, name, grade, year, most_recent, SBACSection)

    # Add additional attributes
    s.rec_id = id_gen.get_rec_id('section')

    # Save and return the section
    s.save()

    return s