'''
Created on Feb 27, 2013

@author: tosako
'''
from edschema.database.connector import DBConnection
import os
import csv
import logging
from sqlalchemy.types import Boolean
import datetime

logger = logging.getLogger(__name__)


__true_values = set(['true', 't', '1'])
__false_values = set(['false', 'f', '0'])


class DataException(Exception):
    '''
    Exception for Data Related problems
    '''
    pass


class DataImporterLengthException(DataException):
    '''
    Exception for Data Importer
    '''
    pass


class DataImporterCastException(Exception):
    '''
    Exception for Data Importer Cast
    '''
    pass


def __cast_data_type(column, value):
    '''
    cast value dynamically
    @param column: the column object
    @param value: the value to get casted
    '''
    # if value is not None and length is not 0 AND not nullable
    # get python_type property, then cast
    if (len(value) == 0):
        return None
    if (value is not None and len(value) != 0 or not column.nullable):
        try:
            # need to explicitly convert booleans because they are read from file as strings
            if isinstance(column.type, Boolean):
                if value.lower() in __true_values:
                    value = True
                elif value.lower() in __false_values:
                    value = False

            if column.type.python_type is datetime.datetime:
                if len(value) == 8:
                    value = datetime.datetime.strptime(value, '%H:%M:%S')
                elif len(value) == 14:
                    value = datetime.datetime.strptime(value, '%Y%m%d%H%M%S')
                elif len(value) == 19:
                    value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                else:
                    value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S%z')
            elif column.type.python_type is datetime.timedelta:
                value = datetime.timedelta(seconds=int(value))
            else:
                value = column.type.python_type(value)
        except:
            msg = 'Cast Exception: Column[%s.%s] value[%s] cast to[%s]' % (column.table.name, column.name, value, column.type.python_type)
            raise DataImporterCastException(msg)
    return value


def __check_data_length(column, value):
    '''
    @param column: the column object
    @param value: the value to be inserted into the column
    '''
    if value is None:
        return

    if column.type.python_type == str:
        if column.type.length is not None and column.type.length < len(value):
            msg = 'Length Exception: Column[%s.%s] max length is %d, but the length of value was %d. value[%s]' % (column.table.name, column.name, column.type.length, len(value), value)
            raise DataImporterLengthException(msg)


def __import_csv_file(csv_file, connection, table):
    '''
    @param csv_file: the csv file path
    @type csv_file: string
    @param connection: the connection object
    @param table: the table object we are importing into
    '''
    with open(csv_file) as file_obj:
        # first row of the csv file is the header names
        reader = csv.DictReader(file_obj, delimiter=',')
        for row in reader:
            new_row = {}
            try:
                for field_name in list(row.keys()):
                    # strip out spaces and \n
                    clean_field_name = field_name.rstrip()
                    value = row[field_name]
                    column = table.c[clean_field_name]
                    value = __cast_data_type(column, value)
                    __check_data_length(column, value)
                    new_row[clean_field_name] = value
                # Inserts to the table one row at a time
                connection.execute(table.insert().values(**new_row))
            except Exception as x:
                logger.exception(x)
                raise


def import_csv_dir(resources_dir, datasource_name=''):
    '''
    import data from csv files
    return
        True: load data successfully
        False: no data loaded or failed to load data

    @param resources_dir: the resource directory
    @type resources_dir: string
    @param datasource_name: the data source name
    @type datasource_name: string
    '''
    __success = False
    with DBConnection(name=datasource_name) as connection:
        metadata = connection.get_metadata()
        # Look through metadata and upload available imports with the same and and ext csv
        # use transaction.
        # if importing is okay. then commit the transaction; otherwise, roll back
        with connection.get_transaction() as _:
            __foundImport = False
            for table in metadata.sorted_tables:
                file = os.path.join(resources_dir, table.name + '.csv')
                # if import exists, upload it
                if os.path.exists(file):
                    # Found csv file
                    __import_csv_file(csv_file=file, connection=connection, table=table)
                    __foundImport = True
            __success = __foundImport
    return __success


def load_fact_asmt_outcome(datasource_name=''):
    '''
    load data from fact_asmt_outcome_vw to fact_asmt_outcome
    return
        True: load data successfully
        False: no data loaded or failed to load data

    @param resources_dir: the resource directory
    @type resources_dir: string
    @param datasource_name: the data source name
    @type datasource_name: string
    '''
    __success = False
    with DBConnection(name=datasource_name) as connection:
        metadata = connection.get_metadata()
        tables = [t.name for t in metadata.sorted_tables]
        if "fact_asmt_outcome" not in tables:
            return True
        fao = metadata.schema + ".fact_asmt_outcome" if metadata.schema is not None else "fact_asmt_outcome"
        fao_vw = metadata.schema + ".fact_asmt_outcome_vw" if metadata.schema is not None else "fact_asmt_outcome_vw"
        # Look through metadata and upload available imports with the same and and ext csv
        # use transaction.
        # if importing is okay. then commit the transaction; otherwise, roll back
        with connection.get_transaction() as _:
            connection.execute("INSERT INTO " +
                               "    " + fao + " " +
                               ("(SELECT " if metadata.schema is not None else "SELECT ") +
                               "     asmt_outcome_vw_rec_id, asmt_rec_id, student_rec_id, inst_hier_rec_id, " +
                               "     asmt_guid, student_id, state_code, district_id, school_id, " +
                               "     where_taken_id, where_taken_name, asmt_grade, enrl_grade, " +
                               "     date_taken, date_taken_day, " +
                               "     date_taken_month, date_taken_year, asmt_score, asmt_score_range_min, " +
                               "     asmt_score_range_max, asmt_perf_lvl, asmt_claim_1_score, " +
                               "     asmt_claim_1_score_range_min, asmt_claim_1_score_range_max, " +
                               "     asmt_claim_1_perf_lvl, asmt_claim_2_score, asmt_claim_2_score_range_min, " +
                               "     asmt_claim_2_score_range_max, asmt_claim_2_perf_lvl, asmt_claim_3_score, " +
                               "     asmt_claim_3_score_range_min, asmt_claim_3_score_range_max, " +
                               "     asmt_claim_3_perf_lvl, asmt_claim_4_score, asmt_claim_4_score_range_min, " +
                               "     asmt_claim_4_score_range_max, asmt_claim_4_perf_lvl, acc_asl_video_embed, " +
                               "     acc_noise_buffer_nonembed, acc_print_on_demand_items_nonembed, acc_braile_embed, acc_closed_captioning_embed, " +
                               "     acc_text_to_speech_embed, acc_abacus_nonembed, " +
                               "     acc_alternate_response_options_nonembed, acc_calculator_nonembed, " +
                               "     acc_multiplication_table_nonembed, acc_print_on_demand_nonembed, " +
                               "     acc_read_aloud_nonembed, acc_scribe_nonembed, acc_speech_to_text_nonembed, " +
                               "     acc_streamline_mode, from_date, to_date, rec_status, batch_guid " +
                               " FROM " +
                               "     " + fao_vw + " " +
                               (")" if metadata.schema is not None else ""))
    return __success
