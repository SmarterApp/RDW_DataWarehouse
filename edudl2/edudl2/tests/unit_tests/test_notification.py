__author__ = 'tshewchuk'

"""
Unit tests for notification module.
"""

import unittest
import httpretty
from unittest.mock import patch
from edcore.callback_notification.Constants import Constants
from edudl2.notification.notification import create_notification_body, post_udl_job_status
from edcore.callback_notification.callback import post_notification


class TestNotification(unittest.TestCase):

    def setUp(self):
        self.udl2_conf = {'sr_notification_retries': 5, 'sr_notification_timeout': 1}

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

    @patch('edudl2.notification.notification.get_notification_message')
    @patch('edudl2.notification.notification._retrieve_status')
    def test_create_notification_body_success(self, mock__retrieve_status, mock_get_notification_message):
        mock__retrieve_status.return_value = Constants.SUCCESS
        mock_get_notification_message.return_value = ['Completed Successfully']

        body = create_notification_body("guid_batch", "batch_table", "id", "test_reg_id", 100)

        self.assertEquals(body['rowCount'], 100)
        self.assertEquals(body['id'], 'id')
        self.assertEquals(body['testRegistrationId'], 'test_reg_id')
        self.assertEquals(body['status'], 'Success')
        self.assertEquals(body['message'], ['Completed Successfully'])

    @patch('edudl2.notification.notification.get_notification_message')
    @patch('edudl2.notification.notification._retrieve_status')
    def test_create_notification_body_failure(self, mock__retrieve_status, mock_get_notification_message):
        mock__retrieve_status.return_value = Constants.FAILURE
        mock_get_notification_message.return_value = ['ERROR 3000']

        body = create_notification_body("guid_batch", "batch_table", "id", "test_reg_id", 100)

        self.assertTrue('rowCount' not in body)
        self.assertEquals(body['id'], 'id')
        self.assertEquals(body['testRegistrationId'], 'test_reg_id')
        self.assertEquals(body['status'], 'Failed')
        self.assertEquals(body['message'], ['ERROR 3000'])

    @patch('edudl2.notification.notification.create_notification_body')
    @patch('edudl2.notification.notification.post_notification')
    def test_post_udl_job_status(self, mock_post_notification, mock_create_notification_body):
        body = {'test': 'test'}
        mock_create_notification_body.return_value = body
        mock_post_notification.return_value = Constants.SUCCESS, None

        conf = self.get_conf()
        result_status, result_error = post_udl_job_status(conf)

        mock_create_notification_body.assert_called_with('guid_batch', 'batch_table', 'student_reg_guid', 'reg_system_id', 'total_rows_loaded')
        mock_post_notification.assert_called_with('callback_url', 'sr_notification_timeout_interval', body)
        self.assertEquals(result_status, Constants.SUCCESS)
        self.assertEquals(result_error, None)

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
                'sr_notification_timeout_interval': 'sr_notification_timeout_interval'}
        return conf


if __name__ == '__main__':
    unittest.main()
