import json
from sqlalchemy.sql.expression import Select
from smarter_score_batcher.database.tsb_connector import TSBDBConnection
from smarter_score_batcher.constant import Constants, Status


TSB_TENENT = 'tsb'


def save_assessment(data):
    parameters = {key: value for key, value in zip(data.header, data.values)}
    with TSBDBConnection(tenant=TSB_TENENT) as conn:
        ins = conn.get_table(Constants.TSB_ASMT).insert()
        conn.execute(ins, **parameters)


def save_metadata(asmtGuid, stateCode, metadata):
    parameters = {
        Constants.ASMT_GUID: asmtGuid,
        Constants.STATE_CODE: stateCode,
        Constants.CONTENT: json.dumps(metadata),
        Constants.STATUS: Status.NEW
    }
    with TSBDBConnection(tenant=TSB_TENENT) as conn:
        ins = conn.get_table(Constants.TSB_METADATA).insert()
        conn.execute(ins, **parameters)


def get_metadata(asmtGuid=None):
    with TSBDBConnection(tenant=TSB_TENENT) as conn:
        tsb_metadata = conn.get_table(Constants.TSB_METADATA)
        query = Select([tsb_metadata]).where(tsb_metadata.c.status == Status.NEW)
        if asmtGuid:
            query = query.where(tsb_metadata.c.asmt_guid == asmtGuid)
        return conn.get_result(query)


def get_assessments(asmtGuid):
    with TSBDBConnection(tenant=TSB_TENENT) as conn:
        tsb_asmt = conn.get_table(Constants.TSB_ASMT)
        query = Select([tsb_asmt]).where(tsb_asmt.c.AssessmentGuid == asmtGuid)
        assessments = conn.get_result(query)
        # TODO: need to refactor below code
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


def delete_assessments(assessment_id, tsb_asmt_guids):
    # TODO: not in transaction?
    with TSBDBConnection(tenant=TSB_TENENT) as conn:
        tsb_metadata = conn.get_table(Constants.TSB_METADATA)
        tsb_asmt = conn.get_table(Constants.TSB_ASMT)
        # delete meta data in database
        conn.execute(tsb_asmt.delete().where(tsb_asmt.c.tsb_asmt_guid.in_(tsb_asmt_guids)))
        # delete assessment data in database
        conn.execute(tsb_metadata.delete().where(tsb_metadata.c.asmt_guid == assessment_id))
