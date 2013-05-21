'''
Created on May 17, 2013

@author: tosako
'''
import os
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import Select, and_
from edapi.exceptions import NotFoundException


def generate_isr_report_path_by_student_guid(pdf_report_base_dir='/', student_guid=None, asmt_type='SUMMATIVE'):
    '''
    get report absolute path by student_guid.
    if the directroy path does not exist, then create it.
    For security, the directory will be created with only the owner can read-write.
    '''
    # find state_code, asmt_period_year, district_guid, school_guid, and asmt_grade from DB
    with SmarterDBConnection() as connection:
        fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
        dim_asmt = connection.get_table('dim_asmt')
        query = Select([fact_asmt_outcome.c.state_code.label("state_code"),
                        dim_asmt.c.asmt_period_year.label("asmt_period_year"),
                        fact_asmt_outcome.c.district_guid.label("district_guid"),
                        fact_asmt_outcome.c.school_guid.label("school_guid"),
                        fact_asmt_outcome.c.asmt_grade.label('asmt_grade')],
                       from_obj=[fact_asmt_outcome
                                 .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id,
                                                      dim_asmt.c.most_recent,
                                                      dim_asmt.c.asmt_type == asmt_type))])
        query = query.where(and_(fact_asmt_outcome.c.most_recent, fact_asmt_outcome.c.status == 'C', fact_asmt_outcome.c.student_guid == student_guid))
        result = connection.get_result(query)
        if result:
            first_record = result[0]
            state_code = first_record['state_code']
            asmt_period_year = str(first_record['asmt_period_year'])
            district_guid = first_record['district_guid']
            school_guid = first_record['school_guid']
            asmt_grade = first_record['asmt_grade']
        else:
            raise NotFoundException("There are no results for student id {0}".format(student_guid))
    # get absolute file path name
    file_path = generate_isr_absolute_file_path_name(pdf_report_base_dir=pdf_report_base_dir, state_code=state_code, asmt_period_year=asmt_period_year, district_guid=district_guid, school_guid=school_guid, asmt_grade=asmt_grade, student_guid=student_guid, asmt_type=asmt_type)
    return file_path


def generate_isr_absolute_file_path_name(pdf_report_base_dir='/', state_code=None, asmt_period_year=None, district_guid=None, school_guid=None, asmt_grade=None, student_guid=None, asmt_type='SUMMATIVE'):
    '''
    generate isr absolute file path name
    '''
    dirname = os.path.join(pdf_report_base_dir, state_code, asmt_period_year, district_guid, school_guid, asmt_grade, 'isr', asmt_type, student_guid + '.pdf')
    return dirname
