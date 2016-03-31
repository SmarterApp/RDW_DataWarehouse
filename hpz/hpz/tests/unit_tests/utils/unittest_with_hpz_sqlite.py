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

from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from hpz.database.metadata import generate_metadata
from hpz.database.hpz_connector import HPZ_NAMESPACE


class Unittest_with_hpz_sqlite(Unittest_with_sqlite):

    @classmethod
    def setUpClass(cls, force_foreign_keys=True):
        super().setUpClass(datasource_name=HPZ_NAMESPACE, metadata=generate_metadata())

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
