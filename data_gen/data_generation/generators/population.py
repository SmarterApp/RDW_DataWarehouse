"""Generate population elements.

:author: nestep
:date: Febraury 22, 2014
"""

import datetime
import random
import calendar

import data_generation.config.population as pop_config
import data_generation.generators.names as name_gen
import data_generation.util.id_gen as id_gen

from data_generation.model.district import District
from data_generation.model.school import School
from data_generation.model.staff import DistrictStaff, TeachingStaff
from data_generation.model.student import Student
from data_generation.util.weighted_choice import weighted_choice


def generate_district_staff_member(district: District, sub_class=None):
    """Generate a district-level staff member.

    :param district: The district the staff member belongs to
    :param sub_class: The sub-class of district staff to create (if requested, must be subclass of DistrictStaff)
    :return: The staff member
    """
    s = DistrictStaff() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.gender = random.choice(['male', 'female'])
    s.first_name, s.middle_name, s.last_name = name_gen.generate_person_name(s.gender)
    s.district = district
    return s


def generate_teaching_staff_member(school: School, sub_class=None):
    """Generate a teacher in a given school.

    :param school: The school the teacher teaches in
    :param sub_class: The sub-class of teaching staff to create (if requested, must be subclass of TeachingStaff)
    :returns: The staff member
    """
    s = TeachingStaff() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.gender = random.choice(['male', 'female'])
    s.first_name, s.middle_name, s.last_name = name_gen.generate_person_name(s.gender)
    s.school = school
    return s


def generate_student(school: School, grade, acad_year=datetime.datetime.now().year, sub_class=None,
                     has_email_address_rate=pop_config.HAS_EMAIL_ADDRESS_RATE,
                     has_physical_address_rate=pop_config.HAS_PHYSICAL_ADDRESS_RATE,
                     has_address_line_2_rate=pop_config.HAS_ADDRESS_LINE_2_RATE):
    """
    Generate a student.

    :param school: The school the student belongs to
    :param grade: The grade the student belongs to
    :param acad_year: The current academic year this student is being created for (optional, defaults to your machine
                      clock's current year)
    :param sub_class: The sub-class of student to create (if requested, must be subclass of Student)
    :param has_email_address_rate: The rate at which to generate an email address for the student
    :param has_physical_address_rate: The rate at which to generate a physical address for the student
    :param has_address_line_2_rate: The rate at which to generate a line two address for the student
    :return: The student
    """
    # Build student basics
    s = Student() if sub_class is None else sub_class()
    s.guid = id_gen.get_uuid()
    s.grade = grade
    s.school = school
    s.dob = _determine_student_dob(s.grade, acad_year)

    # Determine demographics
    (gender, ethnicities, iep, sec504, lep, ed) = _determine_demographics(school.demo_config[str(grade)])
    s.gender = gender
    s.prg_iep = iep
    s.prg_sec504 = sec504
    s.prg_lep = lep
    s.prg_econ_disad = ed

    if 'amer_ind' in ethnicities:
        s.eth_amer_ind = True
    if 'black' in ethnicities:
        s.eth_black = True
    if 'hispanic' in ethnicities:
        s.eth_hispanic = True
    if 'asian' in ethnicities:
        s.eth_asian = True
    if 'pac_isl' in ethnicities:
        s.eth_pacific = True
    if 'white' in ethnicities:
        s.eth_white = True
    if 'multi' in ethnicities:
        s.eth_multi = True
    if 'none' in ethnicities:
        s.eth_none = True

    # Create the name
    s.first_name, s.middle_name, s.last_name = name_gen.generate_person_name(s.gender)

    # Create physical and email addresses
    if random.random() < has_email_address_rate:
        # Email address (first.last.#@example.com)
        s.email = s.first_name + '.' + s.last_name + '.' + str(random.randint(1, 5000)) + '@example.com'

    if random.random() < has_physical_address_rate:
        s.address_line_1 = name_gen.generate_street_address_line_1()
        if random.random() < has_address_line_2_rate:
            s.address_line_2 = name_gen.generate_street_address_line_2()
        s.address_city = name_gen.generate_street_address_city()
        s.address_zip = random.randint(10000, 99999)

    return s


def advance_student(student: Student, schools_by_grade, hold_back_rate=pop_config.STUDENT_HOLD_BACK_RATE,
                    drop_out_rate=pop_config.STUDENT_DROP_OUT_RATE, transfer_rate=pop_config.STUDENT_TRANSFER_RATE):
    """Take a student and advance them to the next grade. If the next grade takes the student out of the current school,
    pick a new school for them to go to. Should that new grade not be available in any school, the student will be
    marked to drop out of the system.

    :param student: The student to move
    :param schools_by_grade: Potential new schools for a student to be enrolled in
    :param hold_back_rate: The rate at which a student should be held back from a new grade
    :param drop_out_rate: The rate that a student will drop out at if they are not advanced
    :param transfer_rate: The rate at which a student will transfer to a new school without being forced to by grade
                          boundaries
    :returns: True if the student still exists in the system, False if they do not
    """
    # Now check if this student should be advanced
    if random.random() < hold_back_rate:
        # The student is not being advanced
        # Decide if the student should drop out and make sure the student's grade is valid
        #   If the student's grade is not valid, we could accidentally return True
        #   Return False to indicate the student is dropped out
        student.held_back = True
        if random.random() < drop_out_rate:
            # The student is being dropped out, so make them go away
            return False
        else:
            # If the student is not being advanced, but is still in a valid grade, return True
            return student.grade in schools_by_grade

    # Bump the grade
    student.held_back = False
    student.grade += 1

    # If the new grade is not available in any school, drop the student
    if student.grade not in schools_by_grade:
        return False

    # If the new grade of the student is not available in the school, pick a new school
    if student.grade not in student.school.grades or random.random() < transfer_rate:
        student.school = random.choice(schools_by_grade[student.grade])

    return True


def determine_demo_option_selected(sub_config):
    """Decide if a boolean characteristic is selected (is true).

    :param sub_config: A dictionary for a single boolean characteristic
    :returns: If the characteristic is selected
    """
    rand_val = random.random()
    if rand_val < sub_config['perc']:
        return True
    return False


def _determine_student_dob(grade, acad_year=datetime.datetime.now().year):
    """Generates an appropriate date of birth given the student's current grade

    :param grade: The current grade of the student
    :param acad_year: The current academic year this student is being created for (optional, defaults to your machine
                      clock's current year)
    :return: A string representation of the student's date of birth
    """
    approx_age = grade + 6
    birth_year = acad_year - approx_age

    if calendar.isleap(birth_year):
        bday_offset = random.randint(0, 365)

    else:
        bday_offset = random.randint(0, 364)

    # construct a birth date as an offset from January 1st
    return datetime.date(birth_year, 1, 1) + datetime.timedelta(days=bday_offset)


def _determine_demographics(config):
    """Determine the demographic characteristics for a student based on the configuration dictionary.

    :param config: Demographics configuration dictionary to use
    :returns: A tuple of characteristics
    """
    # Determine characteristics
    gender = _pick_demo_option(config['gender'])
    ethnicity = _pick_demo_option(config['ethnicity'])
    iep = determine_demo_option_selected(config['iep'])
    sec504 = determine_demo_option_selected(config['504'])
    lep = determine_demo_option_selected(config['lep'])
    ed = determine_demo_option_selected(config['econ_dis'])

    # Pick more ethnicities if needed
    if ethnicity == 'multi':
        eth1 = 'multi'
        eth2 = 'mutli'
        while eth1 == 'multi' or eth2 == 'multi':
            eth1 = _pick_demo_option(config['ethnicity']) if eth1 == 'multi' else eth1
            eth2 = _pick_demo_option(config['ethnicity']) if eth2 == 'multi' else eth2
        ethnicities = ['multi', eth1, eth2]
    else:
        ethnicities = [ethnicity]

    # Return the characteristics
    return gender, ethnicities, iep, sec504, lep, ed


def _pick_demo_option(sub_config):
    """Pick a single demographic characteristic from a dict of options.

    :param sub_config: A dictionary for a single multi-select characteristic
    :returns: Selected value for characteristic
    """
    return weighted_choice({name: obj['perc']
                            for name, obj in sub_config.items()})
