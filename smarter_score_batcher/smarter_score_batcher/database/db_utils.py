from smarter_score_batcher.database.tsb_connector import TSBDBConnection
from smarter_score_batcher.constant import Constants


def save_asmt_to_database(data):
    parameters = {key: value for key, value in zip(data.header, data.values)}
    with TSBDBConnection(tenant='cat') as conn:
        ins = conn.get_table(Constants.TSB_ASMT).insert()
        conn.execute(ins, **parameters)
