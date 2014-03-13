"""
Augment the generation of population elements with SBAC-specific items.

@author: nestep
@date: March 3, 2014
"""

import datetime
import random

import general.generators.population as general_pop_gen
import project.sbac.config.cfg as sbac_in_config
import project.sbac.util.id_gen as sbac_id_gen

from general.model.school import School
from general.model.student import Student
from project.sbac.model.student import SBACStudent


def generate_student(school: School, grade, acad_year=datetime.datetime.now().year):
    """
    Generate a student.

    @param school: The school the student belongs to
    @param grade: The grade the student belongs to
    @param acad_year: The current academic year this student is being created for (optional, defaults to your machine
                      clock's current year)
    @return: The student
    """
    # Run the General generator
    s = general_pop_gen.generate_student(school, grade, acad_year, SBACStudent)
    s.district = school.district

    # Get the demographic config
    demo_config = school.demo_config[str(grade)]

    # Set other specifics
    s.guid_sr = sbac_id_gen.get_sr_uuid()
    s.external_ssid = s.guid + 'ext'
    s.external_ssid_sr = sbac_id_gen.get_sr_uuid()
    s.school_entry_date = generate_date_enter_us_school(s.grade, acad_year)
    s.derived_demographic = generate_derived_demographic(s)
    s.prg_migrant = general_pop_gen.determine_demo_option_selected(demo_config['migrant'])
    s.prg_idea = general_pop_gen.determine_demo_option_selected(demo_config['idea'])
    s.prg_primary_disability = random.choice(['', '',  # Allow blanks and give them higher weight
                                              'AUT', 'DB', 'DD', 'EMN', 'HI', 'ID', 'MD', 'OI', 'OHI', 'SLD', 'SLI',
                                              'TBI', 'VI'])

    # None-out primary disability if it doesn't make sense
    if not s.prg_iep and not s.prg_idea and not s.prg_sec504:
        s.prg_primary_disability = None

    # Set language items
    set_lang_items(s, acad_year)

    # Save and return object
    s.save()

    return s


def advance_student(student: Student, schools_by_grade, drop_out_rate=.5):
    """
    Take a student and advance them to the next grade. If the next grade takes the student out of the current school,
    pick a new school for them to go to.

    @param student: The student to move
    @param schools_by_grade: Potential new schools for a student to be enrolled in
    @param drop_out_rate: The rate that a student will drop out at if they are not advanced
    @returns: True if the student still exists in the system, False if they do not
    """
    # Use the general generator to advance the student
    rslt = general_pop_gen.advance_student(student, schools_by_grade, drop_out_rate=drop_out_rate)

    # If we are not keeping the student, don't worry about them
    if not rslt:
        return rslt

    # TODO: Change things like LEP status or IEP status, etc

    return True


def repopulate_school_grade(school: School, grade, grade_students, acad_year=datetime.datetime.now().year):
    """
    Take a school grade and make sure it has enough students. The list of students is updated in-place.

    @param school: The school to potentially re-populate
    @param grade: The grade in the school to potentially re-populate
    @param grade_students: The students currently in the grade for this school
    @param acad_year: The current academic year that the repopulation is occurring within (optional, defaults to your
                      machine clock's current year)
    """
    # Re-populate grades if necessary
    if len(grade_students) < (school.student_count_avg / 20):
        student_count = int(random.triangular(school.student_count_min, school.student_count_max,
                                              school.student_count_avg))
        print('  Creating %i students in grade %i for school %s (%s)' % (student_count, grade, school.name,
                                                                         school.district.name))
        for _ in range(student_count):
            s = generate_student(school, grade, acad_year)
            grade_students.append(s)
    else:
        # The grade is populated, but see if we should add a few new students
        # 33% of the time we do not add students and the other 67% of the time we add 1 to 4 students
        for _ in range(random.choice([0, 0, 1, 2, 3, 4])):
            s = generate_student(school, grade, acad_year)
            grade_students.append(s)
        print('  Grade %i sufficiently populated for school %s (%s)' % (grade, school.name, school.district.name))


def generate_date_enter_us_school(grade, acad_year=datetime.datetime.now().year):
    """
    Generates an appropriate date of when a student would have entered a US school, assuming all students entered
    school in grade K.

    @param grade: the current grade of the student
    @param acad_year: The current academic year to use to create the date (optional, defaults to your machine clock's
                      current year)
    @return: a date object that represents the student's entry date
    """
    entry_year = acad_year - grade - 1
    entry_month = random.randint(8, 9)
    entry_day = random.randint(15, 31) if entry_month == 8 else random.randint(1, 15)
    return datetime.date(entry_year, entry_month, entry_day)


def generate_date_lep_entry(grade, acad_year=datetime.datetime.now().year):
    """
    Generates an appropriate date of when a student would have been designated as LEP

    @param grade: the current grade of the student
    @return: a date object that represents the student's entry date
    """
    entry_year = acad_year - (grade if grade < 5 else random.randint(4, grade))
    entry_month = random.randint(8, 9)
    entry_day = random.randint(15, 31) if entry_month == 8 else random.randint(1, 15)
    return datetime.date(entry_year, entry_month, entry_day)


def generate_date_lep_exit(grade, acad_year=datetime.datetime.now().year):
    """
    Generates an appropriate date of when a student would have been promoted from LEP status

    @param grade: the current grade of the student
    @param acad_year: The current academic year to use to create the date (optional, defaults to your machine clock's
                      current year)
    @return: a date object that represents the student's exit date
    """
    entry_year = acad_year - (3 if grade > 3 else 1)
    entry_month = random.randint(3, 6)
    entry_day = random.randint(1, 30)
    return datetime.date(entry_year, entry_month, entry_day)


def generate_derived_demographic(student):
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
        print('Generate derived demographic column error: %s' % str(ex))
        return -1


def set_lang_items(student, acad_year=datetime.datetime.now().year):
    """
    Set the language values for a student.

    @param student: The student to configure
    @param acad_year: The current academic year to use to create the date (optional, defaults to your machine clock's
                      current year)
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

        # Decide if to set entry date for LEP
        if random.random() < sbac_in_config.LEP_HAS_ENTRY_DATE_RATE:
            student.prg_lep_entry_date = generate_date_lep_entry(student.grade, acad_year)

        # Set an exit date if the proficiency level is good enough
        if student.lang_prof_level in ['good', 'very good']:
            student.prg_lep_exit_date = generate_date_lep_exit(student.grade, acad_year)
            student.lang_title_3_prg = None