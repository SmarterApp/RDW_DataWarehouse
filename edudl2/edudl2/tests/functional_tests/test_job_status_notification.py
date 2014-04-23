from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.database.udl2_connector import get_udl_connection

__author__ = 'smuhit'

import httpretty
import os
import csv
import re
from sqlalchemy import select, func, and_
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.W_job_status_notification import task as job_notify
from edudl2.udl2.constants import Constants


@httpretty.activate
class FunctionalTestJobStatusNotification(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTestJobStatusNotification, cls).setUpClass()

    def setUp(self):
        sr_data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "student_registration_data")
        self.successful_batch = os.path.join(sr_data_dir, "UDL_BATCH_success.csv")
        self.successful_batch_id = "17a2e644-be41-47d9-a730-74c1a4cfaae7"
        self.failed_batch = os.path.join(sr_data_dir, "UDL_BATCH_failure.csv")
        self.failed_err_list = os.path.join(sr_data_dir, "ERR_LIST.csv")
        self.failed_batch_id = "1a109333-8587-4875-8839-293356469f9a"

    #Load file to udl batch table. If empty is true, empties out the batch table first
    def load_to_table(self, file, empty=True, table=udl2_conf['udl2_db']['batch_table']):
        with get_udl_connection() as conn:
            t = conn.get_table(table)
            if empty:
                conn.execute(t.delete())
                query = select([func.count()]).select_from(t)
                count = conn.execute(query).fetchall()[0][0]
                self.assertEqual(count, 0, 'Could not empty out batch table correctly')
            dict_list = get_csv_dict_list(file)
            conn.execute(t.insert().values(dict_list))

    #Check batch table to see if the notification was successful
    def verify_notification_success(self, guid):
        with get_udl_connection() as conn:
            batch_table = conn.get_table(udl2_conf['udl2_db']['batch_table'])
            query = select([batch_table.c.udl_phase_step_status],
                           and_(batch_table.c.guid_batch == guid, batch_table.c.udl_phase == 'UDL_JOB_STATUS_NOTIFICATION'))
            result = conn.execute(query).fetchall()
            self.assertNotEqual(result, [])
            for row in result:
                status = row['udl_phase_step_status']
                self.assertEqual(status, 'SUCCESS', 'Notification did not succeed')

    #Check batch table to see if the notification failed, with a given number of attempts
    def verify_notification_failed(self, guid, attempts):
        with get_udl_connection() as conn:
            batch_table = conn.get_table(udl2_conf['udl2_db']['batch_table'])
            query = select([batch_table.c.udl_phase_step_status, batch_table.c.error_desc],
                           and_(batch_table.c.guid_batch == guid, batch_table.c.udl_phase == 'UDL_JOB_STATUS_NOTIFICATION'))
            result = conn.execute(query).fetchall()
            self.assertNotEqual(result, [])
            for row in result:
                status = row['udl_phase_step_status']
                self.assertEqual(status, 'FAILURE', 'Notification did not fail')
                actual_attempts = len(re.findall(r'","', row['error_desc'])) + 1
                self.assertEqual(attempts, actual_attempts)

    #Check the body of the notification on a successful UDL run
    def verify_successful_request_body(self, request):
        self.assertEquals(request['status'], 'Success')
        self.assertEquals(request['id'], 'wxyz5678')
        self.assertEquals(request['message'], ['Job completed successfully'])
        self.assertEquals(request['testRegistrationId'], 'abcd1234')
        self.assertEquals(request['rowCount'], 100)
        self.assertEquals(len(request), 5)

    #Check the body of the notification on a failed UDL run
    def verify_failed_request_body(self, request):
        self.assertEquals(request['status'], 'Failed')
        self.assertEquals(len(request['message']), 2)
        self.assertTrue('simple file validator error' in request['message'][0])
        self.assertTrue('5000' in request['message'][1])
        self.assertEquals(request['testRegistrationId'], 'abcd1234')
        self.assertEquals(request['id'], 'wxyz5678')
        self.assertTrue('rowCount' not in request)
        self.assertEquals(len(request), 4)

    def verify_header(self, headers):
        self.assertEquals(headers['Content-type'], 'application/json')

    def test_notification_failed_with_non_retryable_error_code(self):
        httpretty.register_uri(httpretty.POST, "http://www.this_is_a_dummy_url.com", status=401)
        self.load_to_table(self.successful_batch)
        msg = generate_message(self.successful_batch_id)
        job_notify(msg)

        request = httpretty.last_request().parsed_body

        self.verify_successful_request_body(request)
        self.verify_header(httpretty.last_request().headers)
        self.verify_notification_failed(self.successful_batch_id, 1)

    def test_successful_job_status(self):
        httpretty.register_uri(httpretty.POST, "http://www.this_is_a_dummy_url.com", status=204)
        self.load_to_table(self.successful_batch)
        msg = generate_message(self.successful_batch_id)
        job_notify(msg)

        request = httpretty.last_request().parsed_body

        self.verify_successful_request_body(request)
        self.verify_header(httpretty.last_request().headers)
        self.verify_notification_success(self.successful_batch_id)

    def test_failure_job_status(self):

        httpretty.register_uri(httpretty.POST, "http://www.this_is_a_dummy_url.com")
        self.load_to_table(self.failed_batch)
        self.load_to_table(self.failed_err_list, table=udl2_conf['udl2_db'][mk.ERR_LIST_TABLE])
        msg = generate_message(self.failed_batch_id)
        job_notify(msg)

        request = httpretty.last_request().parsed_body

        self.verify_failed_request_body(request)
        self.verify_header(httpretty.last_request().headers)
        self.verify_notification_success(self.failed_batch_id)


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
        mk.LOAD_TYPE: Constants.LOAD_TYPE_STUDENT_REGISTRATION,
        mk.CALLBACK_URL: "http://www.this_is_a_dummy_url.com",
        mk.STUDENT_REG_GUID: "wxyz5678",
        mk.REG_SYSTEM_ID: "abcd1234",
        mk.TOTAL_ROWS_LOADED: 100
    }
    return message
