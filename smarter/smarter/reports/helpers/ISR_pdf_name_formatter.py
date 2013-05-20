'''
Created on May 17, 2013

@author: tosako
'''
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import and_, Select
from edapi.exceptions import NotFoundException
import os

class ISR_pdf_name:
    def __init__(self, studentGuid, asmt_type='SUMMATIVE'):
        self.__studentGuid = studentGuid
        self.__asmt_type = asmt_type
        self.__result = None
        self.__queried = False

    def generate_filename(self):
        '''
        generate PDF filename for ISR
        '''
        result = self.__get_query_result()
        if result:
            first_record = result[0]
            asmt_period_year = str(first_record['asmt_period_year'])
        else:
            raise NotFoundException("There are no results for student id {0}".format(self.__studentGuid))
        filename = 'ISR-' + self.__studentGuid + '-' + asmt_period_year + '-' + self.__asmt_type
        return filename

    def generate_dirname(self):
        '''
        generate PDF directory name for ISR
        '''
        result = self.__get_query_result()
        if result:
            first_record = result[0]
            asmt_period_year = str(first_record['asmt_period_year'])
            school_guid = first_record['school_guid']
            asmt_grade = first_record['asmt_grade']
        else:
            raise NotFoundException("There are no results for student id {0}".format(self.__studentGuid))
        dirname = os.path.join('ISR', asmt_period_year, school_guid, asmt_grade)
        return dirname

    def __get_query_result(self):
        if self.__queried == False:
            self.__queried = True
            with SmarterDBConnection() as connection:
                query = self.__prepare_query(connection=connection)
                self.__result = connection.get_result(query)
        return self.__result

    def __prepare_query(self, connection):
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            dim_asmt = connection.get_table('dim_asmt')
            query = Select([dim_asmt.c.asmt_period_year.label("asmt_period_year"), fact_asmt_outcome.c.school_guid.label("school_guid"), fact_asmt_outcome.c.asmt_grade.label('asmt_grade')],
                                        from_obj=[fact_asmt_outcome
                                                  .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id,
                                                                   dim_asmt.c.most_recent,
                                                                   dim_asmt.c.asmt_type == self.__asmt_type))])
            query = query.where(and_(fact_asmt_outcome.c.most_recent, fact_asmt_outcome.c.status == 'C', fact_asmt_outcome.c.student_guid == self.__studentGuid))
            return query
