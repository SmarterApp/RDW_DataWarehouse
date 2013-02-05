'''
create_star -- create a star schema

create_star will create a database, a schema within the database, and all the required tables, indexes,
and foreign keys required to implement the star schema

Command line options are available form --help, but as a quick start:
    to locally create a schema use something like:
        --database --name <your_star_db> --schema --sname <your_schema_name> --tables --verbose
    to make a schema on QA:
        --database --name <qa_star_date> --schema --sname <edware> --tables --server monetdb1.poc.dum.edwdc.net:5432 --user edware --password edware --verbose

@author:     smacgibbon

@copyright:  2013 Wireless Generation. All rights reserved.

@license:    boiler plate goes here - open source? is it in RFP?

@contact:    edwaredevs@wgen.net
@deffield    updated: Updated
'''
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Index
from sqlalchemy import BigInteger, SmallInteger, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.types import Enum

__all__ = []
__version__ = 0.1
__date__ = '2013-02-02'
__updated__ = '2013-02-02'

DBDRIVER = "postgresql+pypostgresql"
DEBUG = 0
VERBOSE = False


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def generate_ed_metadata(scheme_name=None):

    metadata = MetaData(schema=scheme_name)

    # For PR, Guam, US VI, Brazil... etc
    country = Table('dim_country', metadata,
                    Column('country_id', String(2), primary_key=True),
                    Column('country_name', String(100), nullable=False),
                    Column('country_code', String(3), nullable=False),
                    )

    Index('dim_country_idx', country.c.country_id, unique=True)

    # Two-letter state - some countries have 3 or more, but two will do for US
    state_prov = Table('dim_state', metadata,
                       Column('state_id', String(2), primary_key=True),
                       Column('state_name', String(32), nullable=False),
                       Column('state_code', String(2), nullable=True),
                       )

    Index('dim_state_idx', state_prov.c.state_id, unique=True)
    Index('dim_state_codex', state_prov.c.state_code, unique=True)

    district = Table('dim_district', metadata,
                     Column('district_id', BigInteger, primary_key=True),
                     Column('district_external_id', String(256)),
                     Column('district_name', String(256), nullable=False),
                     Column('address_1', String(256), nullable=True),
                     Column('address_2', String(256), nullable=True),
                     Column('zip_code', String(5), nullable=True),
                     Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                     )

    Index('dim_district_idx', district.c.dim_district, unique=True)

    school = Table('dim_school', metadata,
                   Column('school_id', BigInteger, primary_key=True),
                   Column('school_external_id', String(256)),
                   Column('school_name', String(256), nullable=False),
                   Column('district_name', String(256), nullable=False),
                   Column('school_categories_type', nullable=True,
                          Enum("Elementary/Secondary School",
                               "Elementary School",
                               "High School",
                               "Middle School",
                               "Junior High School",
                               "SecondarySchool",
                               "Ungraded",
                               "Adult School",
                               "Infant/toddler School",
                               "Preschool/early childhood",
                               "Primary School",
                               "Intermediate School",
                               "All Levels")
                          ),  # From Ed-Fi SchoolCategoriesType
                   Column('school_type', nullable=True,
                          Enum("Alternative",
                               "Regular",
                               "Special Education",
                               "Vocational",
                               "JJAEP",
                               "DAEP")
                          ),  # From Ed-Fi SchoolType
                   Column('address_1', String(256), nullable=True),
                   Column('address_2', String(256), nullable=True),
                   Column('city', String(100), nullable=True),
                   Column('zip_code', String(5), nullable=True),
                   Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                   )

    Index('dim_school_idx', school.c.school_id, unique=True)

    where_taken = Table('dim_where_taken', metadata,
                        Column('where_taken_id', BigInteger, primary_key=True),
                        Column('where_taken_name', String(256), primary_key=True),
                        Column('district_name', String(256), nullable=False),
                        Column('address_1', String(32), nullable=False),
                        Column('address_2', String(32), nullable=True),
                        Column('city', String(32), nullable=False),
                        Column('zip_code', String(5), nullable=False),
                        Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                        Column('country_id', None, ForeignKey('dim_country.country_id'))
                        )

    Index('dim_where_taken_idx', where_taken.c.where_taken_id, unique=True)

    grade = Table('dim_grade', metadata,
                  Column('grade_id', String(2), primary_key=True),
                  Column('grade_code', String(10), nullable=False),
                  Column('grade_desc', String(32)),
                  )

    Index('dim_grade_idx', grade.c.grade_id, unique=True)
    Index('dim_grade_codex', grade.c.grade_code, unique=True)

    sections = Table('dim_section', metadata,
                     Column('section_id', BigInteger, primary_key=True),
                     Column('section_external_id', String(256), nullable=False),
                     Column('section_name', String(256)),
                     Column('class_name', String(256)),
                     Column('school_id', None, ForeignKey('dim_school.school_id'), nullable=False),
                     )

    Index('dim_section_idx', sections.c.section_id, unique=True)

    students = Table('dim_student', metadata,
                     Column('student_id', BigInteger, primary_key=True),
                     Column('student_external_id', String(256), primary_key=True),
                     Column('first_name', String(256), nullable=False),
                     Column('middle_name', String(256), nullable=True),
                     Column('last_name', String(256), nullable=False),
                     Column('address_1', String(32), nullable=False),
                     Column('address_2', String(32), nullable=True),
                     Column('city', String(32), nullable=False),
                     Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                     Column('zip_code', String(5), nullable=False),
                     Column('gender', String(10), nullable=False),
                     Column('email', String(256), nullable=False),
                     Column('dob', Date, nullable=False),
                     Column('school_id', None, ForeignKey('dim_school.school_id'), nullable=False),
                     Column('district_id', None, ForeignKey('dim_district.district_id'), nullable=False),
                     )

    Index('dim_student_idx', students.c.student_id, unique=True)

    parents = Table('dim_parent', metadata,
                    Column('parent_id', BigInteger, primary_key=True),
                    Column('parent_external_id', String(256), nullable=False),
                    Column('first_name', String(128), nullable=False),
                    Column('middle_name', String(128), nullable=True),
                    Column('last_name', String(256), nullable=False),
                    Column('address_1', String(32), nullable=False),
                    Column('address_2', String(32), nullable=True),
                    Column('city', String(32), nullable=False),
                    Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                    Column('zip_code', String(5), nullable=False),
                    )

    Index('dim_parent_id_idx', parents.c.parent_id, unique=True)

    external_user_student = Table('dim_external_user_student', metadata,
                                  Column('external_user_student_id', BigInteger, primary_key=True),
                                  Column('external_user_id', String(256), nullable=False),
                                  Column('student_id', None, ForeignKey('dim_student.student_id'), nullable=False),
                                  Column('rel_start_date', Date, nullable=False),
                                  Column('rel_end_date', Date, nullable=True),
                                  )

    Index('dim_external_user_student_idx', external_user_student.c.external_user_student_id, unique=True)
    Index('dim_external_user_student_student_x', external_user_student.c.external_user_id, external_user_student.c.student_id, unique=True)

    teacher = Table('dim_teacher', metadata,
                    Column('teacher_id', BigInteger, primary_key=True),
                    Column('teacher_external_id', String(256), nullable=False),
                    Column('first_name', String(256), nullable=False),
                    Column('middle_name', String(256), nullable=False),
                    Column('last_name', String(256), nullable=False),
                    Column('district_id', None, ForeignKey('dim_district.district_id'), nullable=False),
                    Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                    )

    Index('dim_teacher_idx', teacher.c.teacher_id, unique=True)

    teacher_section = Table('dim_teacher_section', metadata,
                            Column('teacher_section_id', BigInteger, primary_key=True),
                            Column('teacher_id', None, ForeignKey('dim_teacher.teacher_id'), nullable=False),
                            Column('section_id', None, ForeignKey('dim_section.section_id'), nullable=False),
                            Column('rel_start_date', Date, nullable=False),
                            Column('rel_end_date', Date, nullable=True),
                            )

    Index('dim_teacher_section_idx', teacher_section.c.teacher_section_id, unique=True)
    Index('dim_teacher_section_x', teacher_section.c.teacher_id, teacher_section.c.section_id, unique=True)

    staff = Table('dim_staff', metadata,
                  Column('staff_id', BigInteger, primary_key=True),
                  Column('staff_external_id', String(256), nullable=False),
                  Column('first_name', String(256), nullable=False),
                  Column('middle_name', String(256), nullable=False),
                  Column('last_name', String(256), nullable=False),
                  Column('district_id', None, ForeignKey('dim_district.district_id')),
                  Column('state_code', None, ForeignKey('dim_state.state_code')),
                  Column('school_id', None, ForeignKey('dim_school.school_id')),
                  )

    Index('dim_staff_idx', staff.c.staff_id, unique=True)

    assessment = Table('dim_asmt', metadata,
                       Column('asmt_id', BigInteger, primary_key=True),
                       Column('asmt_external_id', String(256), nullable=False),
                       Column('asmt_type', String(16), nullable=False),
                       Column('asmt_period', String(32), nullable=False),
                       Column('asmt_period_year', SmallInteger, nullable=False),
                       Column('asmt_version', String(16), nullable=False),
                       Column('asmt_grade', None, ForeignKey('dim_grade.grade_id')),
                       Column('asmt_subject', String(100)),
                       Column('asmt_claim_1_name', String(256), nullable=True),
                       Column('asmt_claim_2_name', String(256), nullable=True),
                       Column('asmt_claim_3_name', String(256), nullable=True),
                       Column('asmt_claim_4_name', String(256), nullable=True),
                       Column('asmt_cut_point_name_1', String(100), nullable=True),
                       Column('asmt_cut_point_name_2', String(100), nullable=True),
                       Column('asmt_cut_point_name_3', String(100), nullable=True),
                       Column('asmt_cut_point_name_4', String(100), nullable=True),
                       Column('asmt_cut_point_1', SmallInteger, nullable=True),
                       Column('asmt_cut_point_2', SmallInteger, nullable=True),
                       Column('asmt_cut_point_3', SmallInteger, nullable=True),
                       Column('asmt_cut_point_4', SmallInteger, nullable=True),
                       )

    Index('dim_asmt_idx', assessment.c.asmt_id, unique=True)

    assessment_outcome = Table('fact_asmt_outcome', metadata,
                               Column('asmnt_outcome_id', BigInteger, primary_key=True),
                               Column('asmnt_outcome_external_id', String(256), nullable=False),
                               Column('asmt_id', None, ForeignKey('dim_asmt.asmt_id'), nullable=False),
                               Column('student_id', None, ForeignKey('dim_student.student_id'), nullable=False),
                               Column('stdnt_tmprl_id', None, ForeignKey('dim_stdnt_tmprl_data.stdnt_tmprl_id'), nullable=False),
                               Column('teacher_id', None, ForeignKey('dim_teacher.teacher_id'), nullable=False),
                               Column('state_code', None, ForeignKey('dim_state.state_code'), nullable=False),
                               Column('district_id', None, ForeignKey('dim_district.district_id'), nullable=False),
                               Column('school_id', None, ForeignKey('dim_school.school_id'), nullable=False),
                               Column('asmt_grade_id', None, ForeignKey('dim_grade.grade_id'), nullable=False),
                               Column('asmt_grade_code', None, ForeignKey('dim_grade.grade_code'), nullable=False),
                               Column('enrl_grade_id', None, ForeignKey('dim_grade.grade_id'), nullable=False),
                               Column('enrl_grade_code', None, ForeignKey('dim_grade.grade_code'), nullable=False),
                               Column('date_taken', Date, nullable=False),
                               Column('date_taken_day', SmallInteger, nullable=False),
                               Column('date_taken_month', SmallInteger, nullable=False),
                               Column('date_taken_year', SmallInteger, nullable=False),
                               Column('where_taken_id', None, ForeignKey('dim_where_taken.where_taken_id'), nullable=False),
                               Column('asmt_score', SmallInteger, nullable=False),
                               Column('asmt_score_min', SmallInteger, nullable=False),
                               Column('asmt_score_max', SmallInteger, nullable=False),
                               Column('asmt_claim_1_score', SmallInteger, nullable=True),
                               Column('asmt_claim_1_score_min', SmallInteger, nullable=True),
                               Column('asmt_claim_1_score_max', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score_min', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score_max', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score_min', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score_max', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score_min', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score_max', SmallInteger, nullable=True),
                               Column('asmt_create_date', Date, nullable=False),
                               )

    Index('fact_asmt_outcome_idx', assessment_outcome.c.asmnt_outcome_id, unique=True)

    return metadata
