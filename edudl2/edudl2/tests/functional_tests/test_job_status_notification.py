__author__ = 'smuhit'

import httpretty
import unittest
import os
import csv
from sqlalchemy import select, func, and_
from edudl2.udl2_util.database_util import get_sqlalch_table_object, connect_db
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.W_job_status_notification import task as job_notify


class FunctionalTestJobStatusNotification(unittest.TestCase):

    def setUp(self):
        self.udl2_conn, self.udl_engine = connect_db(udl2_conf['udl2_db']['db_driver'], udl2_conf['udl2_db']['db_user'],
                                                     udl2_conf['udl2_db']['db_pass'], udl2_conf['udl2_db']['db_host'],
                                                     udl2_conf['udl2_db']['db_port'], udl2_conf['udl2_db']['db_name'])
        sr_data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "student_registration_data")
        self.successful_batch = os.path.join(sr_data_dir, "UDL_BATCH_success.csv")
        self.successful_batch_id = "17a2e644-be41-47d9-a730-74c1a4cfaae7"
        self.failed_batch = os.path.join(sr_data_dir, "UDL_BATCH_failure.csv")
        self.failed_batch_id = "1a109333-8587-4875-8839-293356469f9a"

    def tearDown(self):
        self.udl2_conn.close()
        self.udl_engine.dispose()

    #Load file to udl batch table. If empty is true, empties out the batch table first
    def load_to_udl_batch(self, file, empty=True):
        batch_table = get_sqlalch_table_object(self.udl2_conn, udl2_conf['udl2_db']['db_schema'], udl2_conf['udl2_db']['batch_table'])
        if empty:
            self.udl2_conn.execute(batch_table.delete())
            query = select([func.count()]).select_from(batch_table)
            count = self.udl2_conn.execute(query).fetchall()[0][0]
            self.assertEqual(count, 0, 'Could not empty out batch table correctly')
        dict_list = get_csv_dict_list(file)
        self.udl2_conn.execute(batch_table.insert(), dict_list)

    #Check batch table to see if the notification was successful
    def verify_notification_success(self, guid):
        batch_table = self.udl2_conn.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status],
                       and_(batch_table.c.guid_batch == guid, batch_table.c.udl_phase == 'udl2.W_job_status_notification.task'))
        result = self.udl2_conn.execute(query).fetchall()
        self.assertNotEqual(result, [])
        for row in result:
            status = row['udl_phase_step_status']
            self.assertEqual(status, 'SUCCESS', 'Notification did not succeed')

    @httpretty.activate
    @unittest.skip('In development')
    def test_successful_job_status(self):

        def request_callback(method, uri, headers, body):
            return(204, headers, body)

        httpretty.register_uri(httpretty.POST, "http://www.this_is_a_dummy_url.com", body=request_callback)
        self.load_to_udl_batch(self.successful_batch)
        msg = generate_message(self.successful_batch_id)
        job_notify(msg)
        self.verify_notification_success(self.successful_batch_id)


def get_csv_dict_list(filename):
    """
    Read the csv file and pull out the data and place in a list of dictionaries
    :param filename: The name of the file
    :return: A list of dictionaries mapping to the values in the csv file.
        Uses the first line as dict keys
    """
    row_dict_list = []
    with open(filename, 'r') as af:
        csv_reader = csv.DictReader(af)
        for row in csv_reader:
            clean_row = clean_dictionary_values(row)
            row_dict_list.append(clean_row)
    return row_dict_list


def clean_dictionary_values(val_dict):
    """
    Take a row dictionary and replace all empty strings with None value
    :param val_dict: The dictionary for the given row
    :return: A cleaned dictionary
    """
    for k, v in val_dict.items():
        if v == '':
            val_dict[k] = None

    return val_dict


def generate_message(guid):
    message = {
        mk.GUID_BATCH: guid,
        mk.LOAD_TYPE: udl2_conf['load_type']['student_registration'],
        mk.CALLBACK_URL: "http://www.this_is_a_dummy_url.com",
        mk.STUDENT_REG_GUID: "wxyz5678",
        mk.REG_SYSTEM_ID: "abcd1234"
    }
    return message

if __name__ == '__main__':
    unittest.main()
