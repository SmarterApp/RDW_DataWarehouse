import unittest
from hpz.database.hpz_connector import create_sqlalchemy
from unittest.mock import patch

__author__ = 'npandey'


class HPZConnectorTest(unittest.TestCase):

    @patch('hpz.database.hpz_connector.setup_db_connection_from_ini')
    def test_create_sqlalchemy(self, connector_mock):
        connector_mock.return_value = None
        namespace = 'ns'
        settings = {'hpz.db.url': 'htttp://test.com', 'hpz.db.schema_name': 'schema1'}
        allow_schema_create = False

        create_sqlalchemy(namespace, settings, allow_schema_create, None)

        final_settings = {'url': 'htttp://test.com', 'schema_name': 'schema1'}
        connector_mock.assert_called_with(final_settings, '', None, namespace, allow_schema_create)
