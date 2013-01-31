'''
Created on Jan 28, 2013

@author: tosako
'''
#
# encoding: utf-8
from sqlalchemy.schema import MetaData
from sqlalchemy.types import Enum
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

from sqlalchemy import Table, Column, Index
from sqlalchemy import BigInteger, SmallInteger, String, Date
from sqlalchemy import ForeignKey

__all__ = []
__version__ = 0.1
__date__ = '2013-01-31'
__updated__ = '2013-01-31'

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

    # For PR, Guam, US VI... etc
    country = Table('dim_country', metadata,
                    Column('country_id', String(2), primary_key=True),
                    Column('country', String(64), nullable=False),
                    )

    Index('dim_country_idx', country.c.country_id, unique=True)

    # Two-letter state - some countries have 3 or more, but two will do for US
    state_prov = Table('dim_state', metadata,
                       Column('state_id', String(2), primary_key=True),
                       Column('state', String(32), nullable=False)
                       )

    Index('dim_state_idx', state_prov.c.state_id, unique=True)

    institution = Table('dim_institution', metadata,
                    Column('institution_id', BigInteger, primary_key=True),
                    Column('institution_category', Enum('State Education Agency', 'Education Service Center', 'Local Education Agency', 'School', name='institution_category_enum'), nullable=False),
                    Column('institution_name', String(255), nullable=False),
                    Column('institution_address_1', String(255), nullable=True)
                    )

    Index('dim_institution_idx', institution.c.institution_id, unique=True)

    where_taken = Table('dim_where_taken', metadata,
                        Column('place_id', BigInteger, primary_key=True),
                        Column('address_1', String(32), nullable=False),
                        Column('address_2', String(32), nullable=True),
                        Column('address_3', String(32), nullable=True),
                        Column('city', String(32), nullable=False),
                        Column('state', None, ForeignKey('dim_state.state_id')),
                        Column('zip', String(10), nullable=False),
                        Column('country', None, ForeignKey('dim_country.country_id'))
                        )

    Index('dim_where_taken_idx', where_taken.c.place_id, unique=True)

    grades = Table('dim_grade', metadata,
                   Column('grade_id', String(2), primary_key=True),
                   Column('grade_desc', String(32)),
                   )

    Index('dim_grade_idx', grades.c.grade_id, unique=True)

    classes = Table('dim_class', metadata,
                    Column('class_id', BigInteger, primary_key=True),
                    Column('things', String(128)),
                    )

    Index('dim_class_idx', classes.c.class_id, unique=True)

    sections = Table('dim_section', metadata,
                     Column('section_id', BigInteger, primary_key=True),
                     Column('things', String(128)),
                     Column('class_id', None, ForeignKey('dim_class.class_id')),
                     )

    Index('dim_section_idx', sections.c.section_id, unique=True)

    students = Table('dim_student', metadata,
                     Column('student_id', BigInteger, primary_key=True),
                     #
                     Column('first_name', String(256), nullable=False),
                     Column('middle_name', String(256), nullable=True),
                     Column('last_name', String(256), nullable=False),
                     #
                     Column('address_1', String(32), nullable=False),
                     Column('address_2', String(32), nullable=True),
                     Column('address_3', String(32), nullable=True),
                     Column('city', String(32), nullable=False),
                     Column('state', None, ForeignKey('dim_state.state_id')),
                     Column('zip', String(10), nullable=False),
                     Column('country', None, ForeignKey('dim_country.country_id')),
                     #
                     Column('gender', String(6), nullable=False),
                     Column('institution_id', None, ForeignKey('dim_institution.institution_id')),
                     Column('email', String(256), nullable=False),
                     Column('dob', Date, nullable=False),
                     # Teacher?
                     )

    Index('dim_student_idx', students.c.student_id, unique=True)

    parents = Table('dim_parent', metadata,
                    Column('parent_uniq_id', BigInteger, primary_key=True),
                    Column('parent_id', BigInteger, nullable=False),
                    Column('first_name', String(128), nullable=False),
                    Column('last_name', String(256), nullable=False),
                    Column('student_id', None, ForeignKey('dim_student.student_id')),
                    )

    Index('dim_parent_uniq_idx', parents.c.parent_uniq_id, unique=True)
    Index('dim_parent_id_idx', parents.c.parent_id, unique=False)
    Index('dim_parent_student_idx', parents.c.parent_id, parents.c.student_id, unique=True)

    stdnt_tmp = Table('dim_stdnt_tmprl_data', metadata,
                      Column('stdnt_tmprl_id', BigInteger, primary_key=True),
                      Column('student_id', None, ForeignKey('dim_student.student_id')),
                      Column('effective_date', Date, nullable=False),
                      Column('end_date', Date, nullable=False),
                      Column('grade_id', None, ForeignKey('dim_grade.grade_id')),
                      Column('district_id', None, ForeignKey('dim_institution.institution_id')),
                      Column('school_id', None, ForeignKey('dim_institution.institution_id')),
                      Column('class_id', None, ForeignKey('dim_class.class_id')),
                      Column('section_id', None, ForeignKey('dim_section.section_id'))
                      )

    Index('dim_stdnt_tmprl_data_idx', stdnt_tmp.c.stdnt_tmprl_id, unique=True)

    assessment_type = Table('dim_asmt_type', metadata,
                            Column('asmt_type_id', BigInteger, primary_key=True),
                            Column('asmt_subject', String(16), nullable=False),
                            Column('asmt_type', String(16), nullable=False),
                            Column('asmt_period', String(16), nullable=False),
                            Column('asmt_version', String(16), nullable=False),
                            Column('asmt_grade', None, ForeignKey('dim_grade.grade_id'))
                            )

    Index('dim_asmt_type_idx', assessment_type.c.asmt_type_id, unique=True)

    assessment_outcome = Table('fact_asmt_outcome', metadata,
                               Column('asmnt_outcome_id', BigInteger, primary_key=True),
                               Column('asmt_type_id', None, ForeignKey('dim_asmt_type.asmt_type_id')),
                               Column('student_id', None, ForeignKey('dim_student.student_id')),
                               Column('stdnt_tmprl_id', None, ForeignKey('dim_stdnt_tmprl_data.stdnt_tmprl_id')),
                               Column('date_taken', Date, nullable=False),
                               Column('date_taken_day', SmallInteger, nullable=False),
                               Column('date_taken_month', SmallInteger, nullable=False),
                               Column('date_taken_year', SmallInteger, nullable=False),
                               Column('where_taken_id', None, ForeignKey('dim_where_taken.place_id')),
                               Column('asmt_score', SmallInteger, nullable=False),
                               Column('asmt_claim_1_name', String(255), nullable=True),
                               Column('asmt_claim_1_score', SmallInteger, nullable=True),
                               Column('asmt_claim_2_name', String(255), nullable=True),
                               Column('asmt_claim_2_score', SmallInteger, nullable=True),
                               Column('asmt_claim_3_name', String(255), nullable=True),
                               Column('asmt_claim_3_score', SmallInteger, nullable=True),
                               Column('asmt_claim_4_name', String(255), nullable=True),
                               Column('asmt_claim_4_score', SmallInteger, nullable=True),
                               Column('asmt_create_date', Date, nullable=False),
                               )

    Index('fact_asmt_outcome_idx', assessment_outcome.c.asmnt_outcome_id, unique=True)

    # Clone the assessment outcome, and add some columns
    # assessment_outcome_hist = assessment_outcome.name('hist_fact_asmt_outcome')
    # assessment_outcome_hist.append_column('hist_create_date', Date, nullable = False)

    hist_assessment_outcome = Table('hist_asmt_outcome', metadata,
                                    Column('asmnt_outcome_id', BigInteger, primary_key=True),  # NOTE sequence deleted
                                    Column('asmt_type_id', None, ForeignKey('dim_asmt_type.asmt_type_id')),
                                    Column('student_id', None, ForeignKey('dim_student.student_id')),
                                    Column('stdnt_tmprl_id', None, ForeignKey('dim_stdnt_tmprl_data.stdnt_tmprl_id')),
                                    Column('date_taken', Date, nullable=False),
                                    Column('date_taken_day', SmallInteger, nullable=False),
                                    Column('date_taken_month', SmallInteger, nullable=False),
                                    Column('date_taken_year', SmallInteger, nullable=False),
                                    Column('where_taken_id', None, ForeignKey('dim_where_taken.place_id')),
                                    Column('asmt_score', SmallInteger, nullable=False),
                                    Column('asmt_claim_1_name', String(255), nullable=True),
                                    Column('asmt_claim_1_score', SmallInteger, nullable=True),
                                    Column('asmt_claim_2_name', String(255), nullable=True),
                                    Column('asmt_claim_2_score', SmallInteger, nullable=True),
                                    Column('asmt_claim_3_name', String(255), nullable=True),
                                    Column('asmt_claim_3_score', SmallInteger, nullable=True),
                                    Column('asmt_claim_4_name', String(255), nullable=True),
                                    Column('asmt_claim_4_score', SmallInteger, nullable=True),
                                    Column('asmt_create_date', Date, nullable=False),
                                    #
                                    Column('hist_create_date', Date, nullable=False),
                                    )

    Index('hist_asmt_outcome_idx', hist_assessment_outcome.c.asmnt_outcome_id, unique=True)

    return metadata
