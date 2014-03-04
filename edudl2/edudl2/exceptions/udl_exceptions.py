__author__ = 'swimberly'


class DeleteRecordNotFound(Exception):
    def __init__(self, batch_guid, rows, schema_and_table):
        self.batch_guid = batch_guid
        self.rows = rows
        self.schema_and_table = schema_and_table

    def __str__(self):
        return "DeleteRecordNotFound for batch_guid: {batch_guid}, "\
               "{total_rows} record(s) not found in {schema}".format(batch_guid=self.batch_guid,
                                                                     total_rows=len(self.rows),
                                                                     schema=self.schema_and_table)
