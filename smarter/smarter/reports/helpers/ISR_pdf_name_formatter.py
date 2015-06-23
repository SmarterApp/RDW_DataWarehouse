'''
Created on May 17, 2013

@author: tosako
'''
import os
from sqlalchemy.sql.expression import Select, and_, distinct
from edapi.exceptions import NotFoundException
from smarter.reports.helpers.constants import Constants, AssessmentType
from edcore.database.edcore_connector import EdCoreDBConnection


def generate_isr_report_path_by_student_id(state_code, date_taken=None, asmt_year=None, pdf_report_base_dir='/', student_ids=None, asmt_type=AssessmentType.SUMMATIVE, grayScale=True, lang='en'):
    '''
    Get Individual Student Report absolute path by student_id.
    If the directory path does not exist, then create it.
    For security, the directory will be created with only the owner can read-write.
    '''
    if date_taken is None and asmt_year is None:
        raise AttributeError('Need one of date_taken or asmt_year')

    file_paths = {}
    if type(student_ids) is not list:
        student_ids = [student_ids]
    # find state_code, asmt_period_year, district_id, school_id, and asmt_grade from DB
    with EdCoreDBConnection(state_code=state_code) as connection:
        if asmt_type == AssessmentType.INTERIM_ASSESSMENT_BLOCKS:
            query = generate_query_for_iab(connection, student_ids, asmt_year)
        else:
            query = generate_query_for_summative_or_interim(connection, asmt_type, student_ids, asmt_year, date_taken)

        results = connection.get_result(query)
        if len(results) != len(student_ids):
            raise NotFoundException("student count does not match with result count")
        for result in results:
            student_id = result[Constants.STUDENT_ID]
            state_code = result[Constants.STATE_CODE]
            asmt_period_year = str(result[Constants.ASMT_PERIOD_YEAR])
            date_taken = str(result[Constants.DATETAKEN]) if result.get(Constants.DATETAKEN) is not None else None
            district_id = result[Constants.DISTRICT_ID]
            school_id = result[Constants.SCHOOL_ID]
            asmt_grade = result.get(Constants.ASMT_GRADE)

            # get absolute file path name
            file_path = generate_isr_absolute_file_path_name(pdf_report_base_dir=pdf_report_base_dir, state_code=state_code, asmt_period_year=asmt_period_year, district_id=district_id, school_id=school_id, asmt_grade=asmt_grade, student_id=student_id, asmt_type=asmt_type, grayScale=grayScale, lang=lang, date_taken=date_taken)
            file_paths[student_id] = file_path
    return file_paths


def generate_isr_absolute_file_path_name(pdf_report_base_dir='/', state_code=None, asmt_period_year=None, district_id=None, school_id=None, asmt_grade=None, student_id=None, asmt_type=AssessmentType.SUMMATIVE, grayScale=False, lang='en', date_taken=None):
    '''
    Generate Individual Student Report absolute file path name
    '''
    dirname = os.path.join(pdf_report_base_dir, state_code, asmt_period_year, district_id, school_id)
    if asmt_grade is not None:
        dirname = os.path.join(dirname, asmt_grade)
    dirname = os.path.join(dirname, 'isr', asmt_type, student_id + (('.' + date_taken) if date_taken is not None else '') + '.' + lang)
    return dirname + (".g.pdf" if grayScale else ".pdf")


def generate_query_for_summative_or_interim(connection, asmt_type, student_ids, asmt_year, date_taken):
    fact_table = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
    dim_asmt = connection.get_table(Constants.DIM_ASMT)
    query = Select([distinct(fact_table.c.student_id).label(Constants.STUDENT_ID),
                    fact_table.c.state_code.label(Constants.STATE_CODE),
                    dim_asmt.c.asmt_period_year.label(Constants.ASMT_PERIOD_YEAR),
                    fact_table.c.date_taken.label(Constants.DATETAKEN),
                    fact_table.c.district_id.label(Constants.DISTRICT_ID),
                    fact_table.c.school_id.label(Constants.SCHOOL_ID),
                    fact_table.c.asmt_grade.label(Constants.ASMT_GRADE)],
                   from_obj=[fact_table
                             .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_table.c.asmt_rec_id,
                                                  dim_asmt.c.rec_status == Constants.CURRENT,
                                                  dim_asmt.c.asmt_type == asmt_type,
                                                  dim_asmt.c.asmt_period_year == asmt_year))])
    query = query.where(and_(fact_table.c.rec_status == Constants.CURRENT, fact_table.c.student_id.in_(student_ids)))
    if date_taken is not None:
        query = query.where(and_(fact_table.c.date_taken == date_taken))
    return query


def generate_query_for_iab(connection, student_ids, asmt_year):
    fact_table = connection.get_table(Constants.FACT_BLOCK_ASMT_OUTCOME)
    dim_asmt = connection.get_table(Constants.DIM_ASMT)
    query = Select([distinct(fact_table.c.student_id).label(Constants.STUDENT_ID),
                    fact_table.c.state_code.label(Constants.STATE_CODE),
                    dim_asmt.c.asmt_period_year.label(Constants.ASMT_PERIOD_YEAR),
                    fact_table.c.district_id.label(Constants.DISTRICT_ID),
                    fact_table.c.school_id.label(Constants.SCHOOL_ID)],
                   from_obj=[fact_table
                             .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_table.c.asmt_rec_id,
                                                  dim_asmt.c.rec_status == Constants.CURRENT,
                                                  dim_asmt.c.asmt_type == AssessmentType.INTERIM_ASSESSMENT_BLOCKS,
                                                  dim_asmt.c.asmt_period_year == asmt_year))])
    query = query.where(and_(fact_table.c.rec_status == Constants.CURRENT, fact_table.c.student_id.in_(student_ids)))
    return query
