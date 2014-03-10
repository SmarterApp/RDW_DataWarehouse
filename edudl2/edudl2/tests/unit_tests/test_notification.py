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
    def test_post_notification(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([201])
        notification_status, notification_messages = post_notification(callback_url, 5, 1, notification_body)

        # Verify results.
        self.assertEquals(mk.SUCCESS, notification_status)
        self.assertEquals(None, notification_messages)

    @httpretty.activate
    def test_post_notification_success_with_retries(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([408, 408, 201])
        start_time = datetime.datetime.now()
        notification_status, notification_messages = post_notification(callback_url, 5, 1, notification_body)

        # Verify results.
        end_time = datetime.datetime.now()
        self.assertEquals(mk.SUCCESS, notification_status)
        self.assertEquals(3, len(notification_messages))
        self.assertEquals('408 Client Error: Request a Timeout', notification_messages[0])
        self.assertEquals('Retry 1 - 408 Client Error: Request a Timeout', notification_messages[1])
        self.assertEquals('Retry 2 - 201 Created: Job completed successfully', notification_messages[2])
        self.assertGreaterEqual((end_time - start_time).seconds, 2)  # Cumulative retry intervals.

    @httpretty.activate
    def test_post_notification_failure_with_retries(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = self.register_url([408])
        start_time = datetime.datetime.now()
        notification_status, notification_messages = post_notification(callback_url, 5, 1, notification_body)

        # Verify results.
        end_time = datetime.datetime.now()
        self.assertEquals(mk.FAILURE, notification_status)
        self.assertEquals(5, len(notification_messages))
        self.assertEquals('408 Client Error: Request a Timeout', notification_messages[0])
        self.assertEquals('Retry 1 - 408 Client Error: Request a Timeout', notification_messages[1])
        self.assertEquals('Retry 2 - 408 Client Error: Request a Timeout', notification_messages[2])
        self.assertEquals('Retry 3 - 408 Client Error: Request a Timeout', notification_messages[3])
        self.assertEquals('Retry 4 - 408 Client Error: Request a Timeout', notification_messages[4])
        self.assertGreaterEqual((end_time - start_time).seconds, 5)  # Cumulative retry intervals.

    @unittest.skip('Skip until we find out how to make POST requests actually timeout')
    @httpretty.activate
    def test_post_notification_timeout(self):
        # Create the notification request body.
        notification_body = {'status': mk.SUCCESS, 'id': 'aaa-bbb-ccc', 'test_registration_id': '111-222-333', 'message': ''}

        # Send the status.
        callback_url = 'http://SomeBogusurl/SomeBogusEndpoint'
        notification_status, notification_messages = post_notification(callback_url, 5, 1, notification_body)

        # Verify results.
        self.assertEquals(mk.FAILURE, notification_status)
        self.assertEquals(1, len(notification_messages))
        self.assertEquals('Job completed successfully', notification_messages[0])

    def register_url(self, return_statuses):
        url = "http://MyTestUri/MyEndpoint"
        responses = [httpretty.Response(body={}, status=return_status) for return_status in return_statuses]
        httpretty.register_uri(httpretty.POST, url, responses=responses)
        return url


if __name__ == '__main__':
    unittest.main()
