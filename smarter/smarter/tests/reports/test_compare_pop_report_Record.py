# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

'''
Created on Mar 9, 2013

@author: tosako
'''
import unittest
from smarter.reports.compare_pop_report import Record


class Test(unittest.TestCase):

    def test_empty_record(self):
        record = Record()
        self.assertEqual(0, len(record.subjects))
        self.assertIsNone(record.id)
        self.assertIsNone(record.name)

    def test_record(self):
        record = Record(inst_id='id1', name='name1')
        self.assertEqual(0, len(record.subjects))
        self.assertEqual('id1', record.id)
        self.assertEqual('name1', record.name)
        subjects = {'hello': 'test'}
        self.subjects = subjects
        self.assertDictEqual(self.subjects, subjects)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
