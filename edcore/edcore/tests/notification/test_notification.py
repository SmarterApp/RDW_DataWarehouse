'''
Created on Sep 15, 2014

@author: tosako
'''
import unittest
from edcore.notification.notification import create_notification_body, \
    send_notification
from edcore.database.utils.constants import LoadType, UdlStatsConstants
from unittest.mock import patch


class Test(unittest.TestCase):

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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
