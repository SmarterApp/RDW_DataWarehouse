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
