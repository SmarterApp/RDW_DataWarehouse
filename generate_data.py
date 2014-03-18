"""
The data generator for the SBAC project.

Command line arguments:
  --team TEAM_NAME: Name of team to generate data for (expects sonics or arkanoids)
  --state STATE_TYPE_NAME: Name of state type to generate data for (expects devel, typical_1, california)

@author: nestep
@date: March 17, 2014
"""

import argparse
import datetime
import os
import random

from mongoengine import connect
from pymongo import Connection

import data_generation.config.hierarchy as hier_config
import data_generation.config.population as pop_config
import data_generation.util.hiearchy as hier_util
import data_generation.writers.csv as csv_writer
import data_generation.writers.json as json_writer
import sbac_data_generation.config.cfg as sbac_in_config
import sbac_data_generation.config.hierarchy as sbac_hier_config
import sbac_data_generation.config.out as sbac_out_config
import sbac_data_generation.config.population as sbac_pop_config
import sbac_data_generation.generators.assessment as sbac_asmt_gen
import sbac_data_generation.generators.enrollment as enroll_gen
import sbac_data_generation.generators.hierarchy as sbac_hier_gen
import sbac_data_generation.generators.population as sbac_pop_gen

from sbac_data_generation.model.district import SBACDistrict
from sbac_data_generation.model.state import SBACState
from sbac_data_generation.writers.filters import SBAC_FILTERS

OUT_PATH_ROOT = 'out'

# See assign_team_configuration_options for these values
STATES = []
YEARS = []
ASMT_YEARS = []
INTERIM_ASMT_PERIODS = []
NUMBER_REGISTRATION_SYSTEMS = 1

# These are global regardless of team
GRADES_OF_CONCERN = {3, 4, 5, 6, 7, 8, 11}  # Made as a set for intersection later
REGISTRATION_SYSTEM_GUIDS = []

# Extend general configuration dictionaries with SBAC-specific configs
hier_config.STATE_TYPES.update(sbac_hier_config.STATE_TYPES)
pop_config.DEMOGRAPHICS['california'] = sbac_pop_config.DEMOGRAPHICS['california']
for grade, demo in sbac_pop_config.DEMOGRAPHICS['typical1'].items():
    if grade in pop_config.DEMOGRAPHICS['typical1']:
        pop_config.DEMOGRAPHICS['typical1'][grade].update(demo)

# Register output filters
csv_writer.register_filters(SBAC_FILTERS)


def assign_team_configuration_options(team, state_type):
    """
    Assign configuration options that are specific to one team.

    @param team: Name of team to assign options for
    @param state_type: Type of state to generate
    """
    global STATES, YEARS, ASMT_YEARS, INTERIM_ASMT_PERIODS, NUMBER_REGISTRATION_SYSTEMS

    # Validate parameter
    if team not in ['sonics', 'arkanoids']:
        raise ValueError("Team name '%s' is not known" % team)

    # Assign options
    if team == 'arkanoids':
        STATES = [{'name': 'North Carolina', 'code': 'NC', 'type': state_type}]
        YEARS = [2015, 2016]  # Expected sorted lowest to highest
        ASMT_YEARS = [2016]  # The years to generate summative assessments for
        INTERIM_ASMT_PERIODS = []  # The periods for interim assessments
        NUMBER_REGISTRATION_SYSTEMS = 1  # Should be less than the number of expected districts
    elif team == 'sonics':
        STATES = [{'name': 'North Carolina', 'code': 'NC', 'type': state_type}]
        YEARS = [2015, 2016, 2017]  # Expected sorted lowest to highest
        ASMT_YEARS = [2015, 2016, 2017]  # The years to generate summative assessments for
        INTERIM_ASMT_PERIODS = [('Fall', -1), ('Winter', -1), ('Spring', 0)]  # The periods for interim assessments
        NUMBER_REGISTRATION_SYSTEMS = 1  # Should be less than the number of expected districts


def create_assessment_object(asmt_type, period, year, subject, year_adj=0):
    """
    Create a new assessment object and write it out to JSON.

    @param asmt_type: Type of assessment to create
    @param period: Period (month) of assessment to create
    @param year: Year of assessment to create
    @param subject: Subject of assessment to create
    @param year_adj: An option adjustment to the assessment period year
    @returns: New assessment object
    """
    asmt = sbac_asmt_gen.generate_assessment(asmt_type, period, year, subject, asmt_year_adj=year_adj)
    file_name = sbac_out_config.ASMT_JSON_FORMAT['name'].replace('<YEAR>', str(year)).replace('<GUID>', asmt.guid)
    json_writer.write_object_to_file(file_name, sbac_out_config.ASMT_JSON_FORMAT['layout'], asmt,
                                     root_path=OUT_PATH_ROOT)
    file_name = sbac_out_config.DIM_ASMT_FORMAT['name']
    csv_writer.write_records_to_file(file_name, sbac_out_config.DIM_ASMT_FORMAT['columns'], [asmt],
                                     tbl_name='dim_asmt', root_path=OUT_PATH_ROOT)
    return asmt


def generate_district_data(state: SBACState, district: SBACDistrict, reg_sys_guid, assessments, asmt_rates_by_subject):
    """
    Generate an entire data set for a single district.

    @param state: State the district belongs to
    @param district: District to generate data for
    @param reg_sys_guid: GUID for the registration system this district is assigned to
    @param assessments: Dictionary of all assessment objects
    @param asmt_rates_by_subject: The rate that students take an assessment for a given subject
    """
    # Set up output file names and columns
    sr_out_cols = sbac_out_config.SR_FORMAT['columns']
    lz_asmt_out_cols = sbac_out_config.LZ_REALDATA_FORMAT['columns']
    fao_out_name = sbac_out_config.FAO_FORMAT['name']
    fao_out_cols = sbac_out_config.FAO_FORMAT['columns']
    dstu_out_name = sbac_out_config.DIM_STUDENT_FORMAT['name']
    dstu_out_cols = sbac_out_config.DIM_STUDENT_FORMAT['columns']
    dsec_out_name = sbac_out_config.DIM_SECTION_FORMAT['name']
    dsec_out_cols = sbac_out_config.DIM_SECTION_FORMAT['columns']

    # Decide how many schools to make
    school_count = random.triangular(district.config['school_counts']['min'],
                                     district.config['school_counts']['max'],
                                     district.config['school_counts']['avg'])

    # Convert school type counts into decimal ratios
    hier_util.convert_config_school_count_to_ratios(district.config)

    # Make the schools
    hierarchies = []
    inst_hiers = {}
    schools = []
    for school_type, school_type_ratio in district.config['school_types_and_ratios'].items():
        # Decide how many of this school type we need
        school_type_count = max(int(school_count * school_type_ratio), 1)  # Make sure at least 1

        for j in range(school_type_count):
            # Create the school and institution hierarchy object
            school = sbac_hier_gen.generate_school(school_type, district)
            ih = sbac_hier_gen.generate_institution_hierarchy(state, district, school)
            hierarchies.append(ih)
            inst_hiers[school.guid] = ih
            schools.append(school)
            print('    Created School: %s (%s)' % (school.name, school.type_str))

    # Write out hierarchies for this district
    csv_writer.write_records_to_file(sbac_out_config.DIM_INST_HIER_FORMAT['name'],
                                     sbac_out_config.DIM_INST_HIER_FORMAT['columns'], hierarchies,
                                     tbl_name='dim_hier', root_path=OUT_PATH_ROOT)

    # Sort the schools
    schools_by_grade = sbac_hier_gen.sort_schools_by_grade(schools)

    # Begin processing the years for data
    students = {}
    for asmt_year in YEARS:
        print('  YEAR %i' % asmt_year)

        # Prepare output file names
        sr_out_name = sbac_out_config.SR_FORMAT['name'].replace('<YEAR>', str(asmt_year)).replace('<GUID>', reg_sys_guid)
        lz_asmt_out_name = sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<YEAR>', str(asmt_year))

        # Set up a dictionary of schools and their grades
        schools_with_grades = sbac_hier_gen.set_up_schools_with_grades(schools, GRADES_OF_CONCERN)

        # Advance the students forward in the grades
        for guid, student in students.items():
            # Move the student forward (false from the advance method means the student disappears)
            if sbac_pop_gen.advance_student(student, schools_by_grade,
                                            drop_out_rate=sbac_in_config.NOT_ADVANCED_DROP_OUT_RATE,
                                            save_to_mongo=False):
                schools_with_grades[student.school][student.grade].append(student)

        # With the students moved around, we will re-populate empty grades and create sections and assessments with
        # outcomes for the students
        assessment_results = []
        sr_students = []
        dim_students = []
        for school, grades in schools_with_grades.items():
            # Get the institution hierarchy object
            inst_hier = inst_hiers[school.guid]

            for grade, grade_students in grades.items():
                # Potentially re-populate the student population
                sbac_pop_gen.repopulate_school_grade(school, grade, grade_students, asmt_year)

                # Create assessment results for this year if requested
                if asmt_year in ASMT_YEARS:
                    first_subject = True
                    for subject in sbac_in_config.SUBJECTS:
                        # Create a class and a section for this grade and subject
                        clss = enroll_gen.generate_class('Grade ' + str(grade) + ' ' + subject, subject, school)
                        section = enroll_gen.generate_section(clss, clss.name + ' - 01', grade, asmt_year, False)
                        csv_writer.write_records_to_file(dsec_out_name, dsec_out_cols, [section],
                                                         tbl_name='dim_section', root_path=OUT_PATH_ROOT)

                        # Grab the summative assessment object
                        asmt_summ = assessments[str(asmt_year) + 'summative' + str(grade) + subject]

                        # Grab the interim assessment objects
                        interim_asmts = []
                        if school.takes_interim_asmts:
                            for period, year_adj in INTERIM_ASMT_PERIODS:
                                key = str(asmt_year) + 'interim' + period + str(grade) + subject
                                interim_asmts.append(assessments[key])

                        for student in grade_students:
                            # Potentially create the summative assessment outcome for this student
                            if random.random() < asmt_rates_by_subject[subject]:
                                ao = sbac_asmt_gen.generate_assessment_outcome(student, asmt_summ, section,
                                                                               inst_hier, save_to_mongo=False)
                                assessment_results.append(ao)

                            # Generate interim assessment results (list will be empty if school does not perform
                            # interim assessments)
                            for asmt in interim_asmts:
                                # Students take interim assessment at the same rate as they take the summative one
                                if random.random() < asmt_rates_by_subject[subject]:
                                    ao = sbac_asmt_gen.generate_assessment_outcome(student, asmt, section,
                                                                                   inst_hier, save_to_mongo=False)
                                    assessment_results.append(ao)

                            # Determine if this student should be in the SR file
                            if random.random() < sbac_in_config.HAS_ASMT_RESULT_IN_SR_FILE_RATE and first_subject:
                                sr_students.append(student)

                            # Make sure we have the student for the next run
                            if first_subject:
                                if student.guid not in students:
                                    students[student.guid] = student
                                    dim_students.append(student)

                        first_subject = False
                else:
                    # We're not doing assessment results, so put all of the students into the list
                    sr_students.extend(grade_students)
                    for student in grade_students:
                        if student.guid not in students:
                            students[student.guid] = student
                            dim_students.append(student)

        # Write data out to CSV
        csv_writer.write_records_to_file(sr_out_name, sr_out_cols, sr_students, root_path=OUT_PATH_ROOT)
        csv_writer.write_records_to_file(dstu_out_name, dstu_out_cols, dim_students, entity_filter=('held_back', False),
                                         tbl_name='dim_student', root_path=OUT_PATH_ROOT)
        if asmt_year in ASMT_YEARS:
            csv_writer.write_records_to_file(lz_asmt_out_name, lz_asmt_out_cols, assessment_results,
                                             root_path=OUT_PATH_ROOT)
            csv_writer.write_records_to_file(fao_out_name, fao_out_cols, assessment_results,
                                             tbl_name='fact_asmt_outcome', root_path=OUT_PATH_ROOT)


def generate_state_data(state: SBACState):
    """
    Generate an entire data set for a single state.

    @param state: State to generate data for
    """
    # Grab the assessment rates by subjects
    asmt_rates_by_subject = state.config['subjects_and_percentages']

    # Create the assessment objects
    assessments = {}
    for year in ASMT_YEARS:
        for subject in sbac_in_config.SUBJECTS:
            for grade in GRADES_OF_CONCERN:
                # Create the summative assessment
                asmt_key_summ = str(year) + 'summative' + str(grade) + subject
                assessments[asmt_key_summ] = create_assessment_object('SUMMATIVE', 'Spring', year, subject)

                # Create the interim assessments
                for period, year_adj in INTERIM_ASMT_PERIODS:
                    asmt_key_intrm = str(year) + 'interim' + period + str(grade) + subject
                    asmt_intrm = create_assessment_object('INTERIM COMPREHENSIVE', period, year, subject, year_adj)
                    assessments[asmt_key_intrm] = asmt_intrm

    # Build the districts
    for district_type, dist_type_count in state.config['district_types_and_counts'].items():
        for _ in range(dist_type_count):
            # Create the district
            district = sbac_hier_gen.generate_district(district_type, state)
            print('  Created District: %s (%s District)' % (district.name, district.type_str))

            # Generate the district data set
            generate_district_data(state, district, random.choice(REGISTRATION_SYSTEM_GUIDS), assessments,
                                   asmt_rates_by_subject)


if __name__ == '__main__':
    # Argument parsing for task-specific arguments
    parser = argparse.ArgumentParser(description='SBAC data generation task.')
    parser.add_argument('-t', '--team', dest='team_name', action='store', default='sonics',
                        help='Specify the name of the team to generate data for (sonics, arkanoids)',
                        required=False)
    parser.add_argument('-s', '--state', dest='state_type', action='store', default='devel',
                        help='Specify the type of state to generate data for (devel, typical_1, california)',
                        required=False)
    args, unknown = parser.parse_known_args()

    # Set team-specific configuration options
    assign_team_configuration_options(args.team_name, args.state_type)

    # Record current (start) time
    tstart = datetime.datetime.now()

    # Verify output directory exists
    if not os.path.exists(OUT_PATH_ROOT):
        os.makedirs(OUT_PATH_ROOT)

    # Connect to MongoDB and drop an existing datagen database
    c = Connection()
    if 'datagen' in c.database_names():
        c.drop_database('datagen')

    # Clean output directory
    for file in os.listdir(OUT_PATH_ROOT):
        file_path = os.path.join(OUT_PATH_ROOT, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            pass

    # Connect to MongoDB, datagen database
    connect('datagen')

    # Prepare star-schema output files
    csv_writer.prepare_csv_file(sbac_out_config.FAO_FORMAT['name'], sbac_out_config.FAO_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_STUDENT_FORMAT['name'],
                                sbac_out_config.DIM_STUDENT_FORMAT['columns'], root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_INST_HIER_FORMAT['name'],
                                sbac_out_config.DIM_INST_HIER_FORMAT['columns'], root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_SECTION_FORMAT['name'],
                                sbac_out_config.DIM_SECTION_FORMAT['columns'], root_path=OUT_PATH_ROOT)
    csv_writer.prepare_csv_file(sbac_out_config.DIM_ASMT_FORMAT['name'], sbac_out_config.DIM_ASMT_FORMAT['columns'],
                                root_path=OUT_PATH_ROOT)

    # Prepare the landing zone files
    for year in YEARS:
        name = sbac_out_config.LZ_REALDATA_FORMAT['name'].replace('<YEAR>', str(year))
        csv_writer.prepare_csv_file(name, sbac_out_config.LZ_REALDATA_FORMAT['columns'], root_path=OUT_PATH_ROOT)

    sr_out_cols = sbac_out_config.SR_FORMAT['columns']
    rs_out_layout = sbac_out_config.REGISTRATION_SYSTEM_FORMAT['layout']

    # Build the registration systems for every year
    start_year = YEARS[0] - 1
    for i in range(NUMBER_REGISTRATION_SYSTEMS):
        # Build the original system
        rs = sbac_hier_gen.generate_registration_system(start_year, str(start_year - 1) + '-02-25', save_to_mongo=False)
        REGISTRATION_SYSTEM_GUIDS.append(rs.guid)

        # Update it over every year
        for year in YEARS:
            # Update the system
            rs.academic_year = year
            rs.extract_date = str(year - 1) + '-02-27'

            # Create the JSON file
            file_name = sbac_out_config.REGISTRATION_SYSTEM_FORMAT['name']
            file_name = file_name.replace('<YEAR>', str(year)).replace('<GUID>', rs.guid)
            json_writer.write_object_to_file(file_name, rs_out_layout, rs, root_path=OUT_PATH_ROOT)

            # Prepare the SR CSV file
            file_name = sbac_out_config.SR_FORMAT['name'].replace('<YEAR>', str(year)).replace('<GUID>', rs.guid)
            csv_writer.prepare_csv_file(file_name, sr_out_cols, root_path=OUT_PATH_ROOT)

    # Start the generation of data
    for state_cfg in STATES:
        # Create the state object
        state = sbac_hier_gen.generate_state(state_cfg['type'], state_cfg['name'], state_cfg['code'])
        print('Created State: %s' % state.name)

        # Process the state
        generate_state_data(state)

    # Record now current (end) time
    tend = datetime.datetime.now()

    # Print statistics
    print()
    print('Run began at:  %s' % tstart)
    print('Run ended at:  %s' % tend)
    print('Run run took:  %s' % (tend - tstart))
    print()