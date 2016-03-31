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

'''
Created on Nov 13, 2015

@author: tosako
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite
from public_report.copy_data import _delete_data, _generate_passphrase, \
    _get_dict, _randomize_id, _mask_id, _clear_batch_guid
from unittest.mock import patch
from edmigrate.database.migrate_public_connector import EdMigratePublicConnection
from sqlalchemy.sql.expression import func, select
import uuid


class Test(Unittest_with_edcore_sqlite):

    @patch('edmigrate.database.migrate_public_connector.EdMigratePublicConnection.get_datasource_name')
    def test__delete_data(self, mock_get_datasource_name):
        mock_get_datasource_name.return_value = 'edware.db.tomcat'
        _delete_data('tomcat')
        count = 1
        with EdMigratePublicConnection('') as public_conn:
            fact_asmt_outcome_vw = public_conn.get_table('fact_asmt_outcome')
            query = select([func.count().label('count')], from_obj=[fact_asmt_outcome_vw])
            count = public_conn.get_result(query)
        self.assertEqual(0, count[0].get('count'))

    def test__generate_passphrase(self):
        passphrase = _generate_passphrase(16)
        self.assertEqual(16, len(passphrase))
        passphrase = _generate_passphrase(32)
        self.assertEqual(32, len(passphrase))

    def test__get_dict(self):
        name = _generate_passphrase(16)
        a = _get_dict(name)
        self.assertEqual(0, len(a))
        key_name = _generate_passphrase(16)
        passphrase = _generate_passphrase(16)
        a[key_name] = passphrase
        b = _get_dict(name)
        self.assertEqual(1, len(b))
        self.assertEqual(passphrase, b[key_name])

    def test__randomize_id(self):
        fields1 = {'student_rec_id': 100, 'asmt_outcome_vw_rec_id': 100, 'test_id': 1234}
        _randomize_id(fields1)
        fields2 = {'student_rec_id': 100, 'asmt_outcome_vw_rec_id': 101}
        _randomize_id(fields2)
        self.assertNotEqual(fields1['student_rec_id'], 100)
        self.assertEqual(fields1['student_rec_id'], fields2['student_rec_id'])
        self.assertEqual(fields1['test_id'], 1234)
        self.assertNotEqual(fields1['student_rec_id'], fields2['asmt_outcome_vw_rec_id'])
        self.assertNotEqual(100, fields2['asmt_outcome_vw_rec_id'])
        self.assertNotEqual(fields1['asmt_outcome_vw_rec_id'], fields2['asmt_outcome_vw_rec_id'])

    def test__mask_id(self):
        student_id = str(uuid.uuid4())
        fields1 = {'student_id': student_id, 'test_id': student_id}
        fields2 = {'student_id': student_id, 'test_id': student_id}
        fields3 = {'student_id': student_id, 'test_id': student_id}
        _mask_id(fields1, 'mykey'.encode())
        _mask_id(fields2, 'mykey'.encode())
        _mask_id(fields3, 'mykey1'.encode())
        self.assertEqual(fields1['student_id'], fields2['student_id'])
        self.assertEqual(fields1['test_id'], student_id)
        self.assertEqual(fields2['test_id'], student_id)
        self.assertNotEqual(fields3['student_id'], student_id)
        self.assertNotEqual(fields3['student_id'], fields2['student_id'])

    def test__clear_batch_guid(self):
        fields = {'batch_guid': 'abcd', 'test_id': 'abcd'}
        _clear_batch_guid(fields)
        self.assertEqual(fields['batch_guid'], '')
        self.assertEqual(fields['test_id'], 'abcd')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
