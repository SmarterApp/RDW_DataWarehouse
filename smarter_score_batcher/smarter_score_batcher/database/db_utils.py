import json
from sqlalchemy.sql.expression import Select
from smarter_score_batcher.database.tsb_connector import TSBDBConnection
from smarter_score_batcher.constant import Constants


def save_assessment(data, tenant):
    parameters = {key: value for key, value in zip(data.header, data.values)}
    with TSBDBConnection(tenant=tenant) as conn:
        ins = conn.get_table(Constants.TSB_ASMT).insert()
        conn.execute(ins, **parameters)


def save_metadata(asmtGuid, metadata, tenant):
    parameters = {
        Constants.ASMT_GUID: asmtGuid,
        Constants.CONTENT: json.dumps(metadata)
    }
    with TSBDBConnection(tenant=tenant) as conn:
        ins = conn.get_table(Constants.TSB_METADATA).insert()
        conn.execute(ins, **parameters)


def get_metadata_by_asmt_guid(asmtGuid, tenant):
    with TSBDBConnection(tenant=tenant) as conn:
        tsb_metadata = conn.get_table(Constants.TSB_METADATA)
        query = Select([tsb_metadata]).where(tsb_metadata.c.asmt_guid == asmtGuid)
        return conn.get_result(query)
