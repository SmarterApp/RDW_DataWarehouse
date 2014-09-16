'''
Created on Sep 15, 2014

@author: tosako
'''
import unittest
from edcore.notification.notification import create_notification_body, \
    send_notification
from edcore.database.utils.constants import LoadType, UdlStatsConstants
from unittest.mock import patch
import httpretty
from edcore.notification.constants import Constants
from edcore.notification.callback import post_notification


class Test(unittest.TestCase):

    def setUp(self):
        self.udl2_conf = {'notification_retries': 5, 'notification_timeout': 1}

    @patch('edcore.notification.notification.send_notification_email')
    @patch('edcore.notification.notification.post_notification')
    def test_send_notification_nocall(self, mock_post_notification, mock_send_notification_email):
        conf = {}
        send_notification(conf)
        self.assertFalse(mock_post_notification.called)
        self.assertFalse(mock_send_notification_email.called)

    @patch('edcore.notification.notification.update_udl_stats_by_batch_guid')
    @patch('edcore.notification.notification.send_notification_email')
    @patch('edcore.notification.notification.post_notification')
    def test_send_notification_callback(self, mock_post_notification, mock_send_notification_email, mock_update_udl_stats_by_batch_guid):
        mock_post_notification.return_value = None, None
        conf = {}
        conf[UdlStatsConstants.BATCH_GUID] = 'abc'
        conf[UdlStatsConstants.NOTIFICATION] = '{"callback_url": "http://127.0.0.1:50473", "academic_year": 2000, "sr_notification_timeout_interval": 1, "email_notification": "tosako@amplify.com", "sr_notification_retry_interval": 1, "sr_notification_max_attempts": 5, "reg_system_id": "800b3654-4406-4a90-9591-be84b67054df", "student_reg_guid": "009a34ee-4609-4b13-8ca2-ed1bc0386afb"}'
        conf[UdlStatsConstants.LOAD_TYPE] = LoadType.STUDENT_REGISTRATION
        conf[UdlStatsConstants.LOAD_STATUS] = UdlStatsConstants.UDL_STATUS_FAILED
        send_notification(conf)
        self.assertTrue(mock_post_notification.called)
        self.assertTrue(mock_send_notification_email.called)
        self.assertTrue(mock_update_udl_stats_by_batch_guid.called)

    def test_create_notification_body(self):
        load_type = LoadType.ASSESSMENT
        guid_batch = 'abc'
        batch_table = 'batch_table'
        id = 'efg'
        test_registration_id = 'hello'
        row_count = 100
        udl_load_status = UdlStatsConstants.MIGRATE_INGESTED
        udl_phase = 'W.hello'
        error_desc = 'error has occured'
        body = create_notification_body(load_type, guid_batch, batch_table, id, test_registration_id, row_count, udl_load_status, udl_phase, error_desc)
        self.assertEqual(body['testRegistrationId'], test_registration_id)
        self.assertEqual(body['rowCount'], 100)
        self.assertEqual(body['status'], 'Success')
        self.assertIn('Job completed successfully', body['message'])


    @httpretty.activate
    def test_post_notification_success_no_retries(self):
        # Create the notification request body.
        notification_body = {'status': Constants.SUCCESS, 'id': 'aaa-bbb-ccc', 'testRegistrationId': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([201])
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals(Constants.SUCCESS, notification_status)
        self.assertEquals(None, notification_error)

    @httpretty.activate
    def test_post_notification_pending(self):
        # Create the notification request body.
        notification_body = {'status': Constants.SUCCESS, 'id': 'aaa-bbb-ccc', 'testRegistrationId': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([408])
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals(Constants.PENDING, notification_status)
        self.assertEquals('408 Client Error: Request a Timeout', notification_error)

    @httpretty.activate
    def test_post_notification_failure(self):
        # Create the notification request body.
        notification_body = {'status': Constants.SUCCESS, 'id': 'aaa-bbb-ccc', 'testRegistrationId': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([401])
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals('401 Client Error: Unauthorized', notification_error)
        self.assertEquals(Constants.FAILURE, notification_status)

    @httpretty.activate
    def test_post_notification_pending_connection_error(self):
        # Create the notification request body.
        notification_body = {'status': Constants.SUCCESS, 'id': 'aaa-bbb-ccc', 'testRegistrationId': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = 'http://SomeBogusurl/SomeBogusEndpoint'
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals(Constants.PENDING, notification_status)
        self.assertRegex(notification_error, "Max retries exceeded with url")

    def test_create_notification_body_success(self):

        body = create_notification_body(LoadType.STUDENT_REGISTRATION, "guid_batch", "batch_table", "id", "test_reg_id", 100, UdlStatsConstants.MIGRATE_INGESTED, None, None)

        self.assertEquals(body['rowCount'], 100)
        self.assertEquals(body['id'], 'id')
        self.assertEquals(body['testRegistrationId'], 'test_reg_id')
        self.assertEquals(body['status'], 'Success')
        self.assertEquals(body['message'], ['Job completed successfully'])

    def test_create_notification_body_failure(self):

        body = create_notification_body(LoadType.STUDENT_REGISTRATION, "guid_batch", "batch_table", "id", "test_reg_id", 100, UdlStatsConstants.UDL_STATUS_FAILED, None, 'ERROR 3000')

        self.assertTrue('rowCount' not in body)
        self.assertEquals(body['id'], 'id')
        self.assertEquals(body['testRegistrationId'], 'test_reg_id')
        self.assertEquals(body['status'], 'Failed')
        self.assertEquals(body['message'], ['ERROR 3000'])

    def register_url(self, return_statuses):
        url = "http://MyTestUri/MyEndpoint"
        responses = [httpretty.Response(body={}, status=return_status) for return_status in return_statuses]
        httpretty.register_uri(httpretty.POST, url, responses=responses)
        return url

    def get_conf(self):
        conf = {'guid_batch': 'guid_batch',
                'batch_table': 'batch_table',
                'student_reg_guid': 'student_reg_guid',
                'reg_system_id': 'reg_system_id',
                'total_rows_loaded': 'total_rows_loaded',
                'callback_url': 'callback_url',
                'notification_timeout_interval': 'notification_timeout_interval'}
        return conf

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
