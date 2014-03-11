__author__ = 'tshewchuk'

"""
Unit tests for notification module.
"""

import unittest
import httpretty
import datetime

from edudl2.udl2 import message_keys as mk
from edudl2.notification.notification import post_notification


class TestNotification(unittest.TestCase):

    def setUp(self):
        self.udl2_conf = {'sr_notification_retries': 5, 'sr_notification_timeout': 1}

    @httpretty.activate
    def test_post_notification_success_no_retries(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([201])
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals(mk.SUCCESS, notification_status)
        self.assertEquals(None, notification_error)

    @httpretty.activate
    def test_post_notification_pending(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([408])
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals(mk.PENDING, notification_status)
        self.assertEquals('408 Client Error: Request a Timeout', notification_error)

    @httpretty.activate
    def test_post_notification_failure(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([401])
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals('401 Client Error: Unauthorized', notification_error)
        self.assertEquals(mk.FAILURE, notification_status)

    @httpretty.activate
    def test_post_notification_pending_connection_error(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = 'http://SomeBogusurl/SomeBogusEndpoint'
        notification_status, notification_error = post_notification(callback_url, 1, notification_body)

        # Verify results.
        self.assertEquals(mk.PENDING, notification_status)
        self.assertRegex(notification_error, 'nodename nor servname provided, or not known')

    def register_url(self, return_statuses):
        url = "http://MyTestUri/MyEndpoint"
        responses = [httpretty.Response(body={}, status=return_status) for return_status in return_statuses]
        httpretty.register_uri(httpretty.POST, url, responses=responses)
        return url


if __name__ == '__main__':
    unittest.main()
