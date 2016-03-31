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

import unittest
from hpz.database.hpz_connector import create_sqlalchemy
from unittest.mock import patch

__author__ = 'npandey'


class HPZConnectorTest(unittest.TestCase):

    @patch('hpz.database.hpz_connector.setup_db_connection_from_ini')
    def test_create_sqlalchemy(self, connector_mock):
        connector_mock.return_value = None
        namespace = 'ns'
        settings = {'hpz.db.url': 'htttp://test.com', 'hpz.db.schema_name': 'schema1', 'hpz.db.pool_size': 20}
        allow_schema_create = False

        create_sqlalchemy(namespace, settings, allow_schema_create, None)

        final_settings = {'url': 'htttp://test.com', 'schema_name': 'schema1', 'pool_size': 20}
        connector_mock.assert_called_with(final_settings, '', None, namespace, allow_schema_create)
