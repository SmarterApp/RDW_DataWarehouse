# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

import os
from edudl2.tests.utils.unittest import UDLTestCase
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf
from edudl2.database.udl2_connector import initialize_all_db


class IntegrationTestCase(UDLTestCase):

    @classmethod
    def setUpClass(cls):
        # test source files
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        initialize_all_db(udl2_conf, udl2_flat_conf)
        super().setUpClass(data_dir=data_dir)
