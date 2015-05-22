
def get_udl_record_by_batch_guid(batch_guid, tenant):
    records = []
    with EdCoreDBConnection(tenant=tenant) as connection:
        fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
        fact_block_asmt_outcome = connection.get_table('fact_block_asmt_outcome')
        select_fao = select(fact_asmt_outcome.c.student_id.label(STUDENT_ID), fact_asmt_outcome.c.asmt_guid.label(ASMT_GUID)).where(fact_asmt_outcome.c.batch_guid=batch_guid)
        select_fbao = select(fact_block_asmt_outcome.c.student_id.label(STUDENT_ID), fact_block_asmt_outcome.c.asmt_guid.label(ASMT_GUID)).where(fact_block_asmt_outcome.c.batch_guid=batch_guid)
        records = connection.get_result(select_fao.union(select_fbao))
    return records

def get_intput_file(batch_guid):
    input_file = ''
    with get_udl_connection() as connector:
        batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
        s = select([batch_table.c.input_file.label('input_file')]).where(and_(batch_table.c.udl_phase='udl2.W_file_arrived.task', batch_table.c.guid_batch))
        results = connector.get_result(s)
        if results:
            input_file = results[0]['input_file']
    return input_file
