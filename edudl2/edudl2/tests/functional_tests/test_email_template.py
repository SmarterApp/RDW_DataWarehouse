import asyncore
from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.tests.utils.smtp_test import SMTPTestServer
from edudl2.udl2_util.util import send_email_from_template
from edudl2.udl2.celery import udl2_conf

class UDLEmailTemplateTest(UDLTestHelper):
    def setUp(self):
        super(UDLEmailTemplateTest, self).setUp()

        self.smtp_server = SMTPTestServer(("localhost", 8025), None)

    def tearDown(self):
        super(UDLEmailTemplateTest, self).tearDown()

        self.smtp_server.end()

    def test_email(self):
        udl2_conf["mail_server_host"] = "localhost"
        udl2_conf["mail_server_port"] = 8025

        email_info = {
            "task_id": "1234",
            "batch_guid": "1234",
            "load_type": "1234",
            "udl_phase": "1234",
            "udl_phase_step": "1234",
            "failure_time": "1234",
            }

        send_email_from_template("exception_email", email_info)

        self.assertEqual(len(self.smtp_server.messages), 1)
        self.assertEqual(self.smtp_server.messages[0]["mail_from"], udl2_conf["exception_email"]["mail_from"])
        self.assertIn(udl2_conf["exception_email"]["mail_to"], self.smtp_server.messages[0]["mail_to"])
