import json
from sqlalchemy.sql.expression import Select
from sqlalchemy.exc import IntegrityError
from smarter_score_batcher.database.tsb_connector import TSBDBConnection
from smarter_score_batcher.constant import Constants
from smarter_score_batcher.error.constants import ErrorsConstants
from smarter_score_batcher.error.error_file_generator import build_error_info_header, \
    build_err_list_from_object


def save_assessment(data):
    parameters = {key: value for key, value in zip(data.header, data.values)}
    with TSBDBConnection() as conn:
        ins = conn.get_table(Constants.TSB_ASMT).insert()
        conn.execute(ins, **parameters)


def save_metadata(asmtGuid, stateCode, metadata):
    parameters = {
        Constants.ASMT_GUID: asmtGuid,
        Constants.STATE_CODE: stateCode,
        Constants.CONTENT: json.dumps(metadata)
    }
    with TSBDBConnection() as conn:
        ins = conn.get_table(Constants.TSB_METADATA).insert()
        conn.execute(ins, **parameters)


def save_error_msg(asmtGuid, stateCode, err_code=None, err_source=None,
                   err_code_text=None, err_source_text=None, err_input=None):
    parameters = {
        Constants.ASMT_GUID: asmtGuid,
        Constants.STATE_CODE: stateCode,
        ErrorsConstants.ERR_CODE: err_code,
        ErrorsConstants.ERR_SOURCE: err_source,
        ErrorsConstants.ERR_CODE_TEXT: err_code_text,
        ErrorsConstants.ERR_SOURCE_TEXT: err_source_text,
        ErrorsConstants.ERR_INPUT: err_input
    }
    with TSBDBConnection() as conn:
        ins = conn.get_table(Constants.TSB_ERROR).insert()
        conn.execute(ins, **parameters)


def get_metadata(asmtGuid=None):
    with TSBDBConnection() as conn:
        tsb_metadata = conn.get_table(Constants.TSB_METADATA)
        query = Select([tsb_metadata])
        if asmtGuid:
            query = query.where(tsb_metadata.c.asmt_guid == asmtGuid)
        return conn.get_result(query)


def get_all_assessment_guids():
    with TSBDBConnection() as conn:
        all_guids = set()
        # query guids from metadata table
        tsb_metadata = conn.get_table(Constants.TSB_METADATA)
        query = Select([tsb_metadata.c.state_code, tsb_metadata.c.asmt_guid])
        assessments = conn.get_result(query)
        for assessment in assessments:
            state_code = assessment[Constants.STATE_CODE]
            asmt_guid = assessment[Constants.ASMT_GUID]
            all_guids.add((state_code, asmt_guid))
        # query guids from error message table
        tsb_error = conn.get_table(Constants.TSB_ERROR)
        query = Select([tsb_error.c.state_code, tsb_error.c.asmt_guid])
        error_asmt_guids = conn.get_result(query)
        for error_record in error_asmt_guids:
            state_code = error_record[Constants.STATE_CODE]
            asmt_guid = error_record[Constants.ASMT_GUID]
            all_guids.add((state_code, asmt_guid))
        return all_guids


def get_assessments(asmtGuid):
    with TSBDBConnection() as conn:
        tsb_asmt = conn.get_table(Constants.TSB_ASMT)
        query = Select([tsb_asmt]).where(tsb_asmt.c.AssessmentGuid == asmtGuid)
        assessments = conn.get_result(query)
        columns = []
        data = []
        guids = []
        for i, asmt in enumerate(assessments):
            row = []
            for j, (column, value) in enumerate(asmt.items()):
                if i == 0 and j > 0:  # first column is guid
                    columns.append(column)
                if j == 0:
                    guids.append(value)
                else:
                    row.append(value)
            data.append(row)
        return guids, data, columns


def get_error_message(asmtGuid):
    with TSBDBConnection() as conn:
        tsb_error = conn.get_table(Constants.TSB_ERROR)
        query = Select([tsb_error]).where(tsb_error.c.asmt_guid == asmtGuid)
        errors = conn.get_result(query)
        error_info = build_error_info_header()
        error_guids = []
        for error in errors:
            error_guids.append(error[Constants.TSB_ERROR_GUID])
            err_list = build_err_list_from_object(error)
            error_info[ErrorsConstants.TSB_ERROR].append(err_list)
        return error_guids, error_info


def delete_assessments(assessment_id, tsb_asmt_guids, tsb_error_guids):
    with TSBDBConnection() as conn:
        # delete error messages
        if tsb_error_guids:
            tsb_error = conn.get_table(Constants.TSB_ERROR)
            conn.execute(tsb_error.delete().where(tsb_error.c.tsb_error_rec_id.in_(tsb_error_guids)))

        # delete meta data in database
        if tsb_asmt_guids:
            tsb_asmt = conn.get_table(Constants.TSB_ASMT)
            conn.execute(tsb_asmt.delete().where(tsb_asmt.c.tsb_asmt_rec_id.in_(tsb_asmt_guids)))

        # delete assessment data in database
        if assessment_id:
            try:
                tsb_metadata = conn.get_table(Constants.TSB_METADATA)
                conn.execute(tsb_metadata.delete().where(tsb_metadata.c.asmt_guid == assessment_id))
            except IntegrityError:
                pass
