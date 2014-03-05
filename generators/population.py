"""
Augment the generation of population elements with SBAC-specific items.

@author: nestep
@date: March 3, 2014
"""

import datetime
import random

import general.generators.population as general_pop_gen
import project.sbac.util.id_gen as sbac_id_gen

from general.model.school import School
from project.sbac.model.student import SBACStudent


def generate_student(school: School, grade):
    """
    Generate a student.

    @param school: The school the student belongs to
    @param grade: The grade the student belongs to
    @return: The student
    """
    # Run the General generator
    s = general_pop_gen.generate_student(school, grade, SBACStudent)

    # Get the demographic config
    demo_config = school.demo_config[str(grade)]

    # Set other specifics
    s.guid_sr = sbac_id_gen.get_sr_uuid()
    s.external_ssid = sbac_id_gen.get_sr_uuid()
    s.school_entry_date = _generate_date_enter_us_school(s.grade)
    s.derived_demographic = _generate_derived_demographic(s)
    s.prg_migrant = general_pop_gen.determine_demo_option_selected(demo_config['migrant'])
    s.prg_idea = general_pop_gen.determine_demo_option_selected(demo_config['idea'])
    s.prg_primary_disability = random.choice(['', '',  # Allow blanks and give them higher weight
                                              'AUT', 'DB', 'DD', 'EMN', 'HI', 'ID', 'MD', 'OI', 'OHI', 'SLD', 'SLI',
                                              'TBI', 'VI'])

    # None-out primary disability if it doesn't make sense
    if not s.prg_iep and not s.prg_idea and not s.prg_sec504:
        s.prg_primary_disability = None

    # Set language items
    _set_lang_items(s)

    # Save and return object
    s.save()

    return s


def _generate_date_enter_us_school(grade):
    """
    Generates an appropriate date of when a student would have entered a US school, assuming all students entered
    school in grade K.

    @param grade: the current grade of the student
    @return: a date object that represents the student's entry date
    """
    current_year = int(datetime.datetime.now().year)
    entry_year = current_year - grade - 1
    entry_month = random.randint(8, 9)
    entry_day = random.randint(15, 31) if entry_month == 8 else random.randint(1,15)
    doe = datetime.date(entry_year, entry_month, entry_day).strftime("%Y-%m-%d")
    return doe


def _generate_date_lep_entry(grade):
    """
    Generates an appropriate date of when a student would have been designated as LEP

    @param grade: the current grade of the student
    @return: a date object that represents the student's entry date
    """
    current_year = int(datetime.datetime.now().year)
    entry_year = current_year - (grade if grade < 5 else random.randint(4, grade))
    entry_month = random.randint(8, 9)
    entry_day = random.randint(15, 31) if entry_month == 8 else random.randint(1,15)
    doe = datetime.date(entry_year, entry_month, entry_day).strftime("%Y-%m-%d")
    return doe


def _generate_date_lep_exit(grade):
    """
    Generates an appropriate date of when a student would have been promoted from LEP status

    @param grade: the current grade of the student
    @return: a date object that represents the student's exit date
    """
    current_year = int(datetime.datetime.now().year)
    entry_year = current_year - (3 if grade > 3 else 1)
    entry_month = random.randint(3, 6)
    entry_day = random.randint(1, 30)
    doe = datetime.date(entry_year, entry_month, entry_day).strftime("%Y-%m-%d")
    return doe


def _generate_derived_demographic(student):
    """
    Generate the derived demographic value for a student.

    @param student: Student to calculate value for
    @returns: Derived demographic value
    """
    try:
        # TODO: need to decide the value. is it true/false, or f/t, or others
        if student.eth_hispanic is True:
            student.derived_demographic = 2

        else:
            demos = {0: student.eth_none,
                     1: student.eth_black,
                     2: student.eth_asian,
                     4: student.eth_amer_ind,
                     5: student.eth_pacific,
                     6: student.eth_white}

            races = [demo for demo, value in demos.items() if value]

            if len(races) > 1:
                return 7  # multi-racial
            elif len(races) == 1:
                return races[0]
            else:
                raise Exception("No race?")
    except Exception as ex:
        print("Generate derived demographic column error " + str(ex))
        return -1


def _set_lang_items(student):
    """
    Set the language values for a student.

    @param student: The student to configure
    """
    if student.prg_lep:
        # Pick a random non-English language
        student.lang_code = random.choice(['fre', 'ben', 'ger', 'chi', 'kor', 'jpn', 'rus'])
        student.lang_prof_level = random.choice(['very poor', 'poor', 'adequate', 'good', 'very good'])
        student.lang_title_3_prg = random.choice(['', '',  # Allow blanks and give them higher weight
                                                  'DualLanguage', 'TwoWayImmersion', 'TransitionalBilingual',
                                                  'DevelopmentalBilingual', 'HeritageLanguage',
                                                  'ShelteredEnglishInstruction', 'StructuredEnglishImmersion', 'SDAIE',
                                                  'ContentBasedESL', 'PullOutESL', 'Other'])

        # Decide if to set entry date for LEP (will for 60%)
        if random.randint(1, 10) < 7:
            student.prg_lep_entry_date = _generate_date_lep_entry(student.grade)

        # Set an exit date if the proficiency level is good enough
        if student.lang_prof_level in ['good', 'very good']:
            student.prg_lep_exit_date = _generate_date_lep_exit(student.grade)
            student.lang_title_3_prg = None