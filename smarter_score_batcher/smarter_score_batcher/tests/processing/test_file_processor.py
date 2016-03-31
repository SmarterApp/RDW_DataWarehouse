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
Created on Nov 25, 2014

@author: tosako
'''
import unittest
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite
from smarter_score_batcher.utils.meta import extract_meta_names
from smarter_score_batcher.utils.constants import Constants
from smarter_score_batcher.tests.processing.utils import read_data
from smarter_score_batcher.processing.file_processor import process_assessment_data
from smarter_score_batcher.database.db_utils import get_assessments, get_metadata, get_all_assessment_guids
from smarter_score_batcher.database.tsb_connector import TSBDBConnection


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Test(Unittest_with_tsb_sqlite):

    def test_process_assessment_data(self):
        data = read_data("assessment.xml")
        meta = extract_meta_names(data)
        root = ET.fromstring(data)
        process_assessment_data(root, meta)
        # test asmt guids
        asmt_guids = get_all_assessment_guids()
        self.assertIsNotNone(asmt_guids)
        state_code, asmt_guid = next(iter(asmt_guids))
        self.assertEqual(state_code, 'CA')
        self.assertEqual(asmt_guid, 'SBAC-FT-SomeDescription-ELA-7')
        # test metadata
        with TSBDBConnection() as conn:
            asmt_meta = get_metadata(conn, asmt_guid)
        self.assertIsNotNone(asmt_meta)
        self.assertIsNotNone(asmt_meta[0][Constants.CONTENT])
        assessments = get_assessments(asmt_guid)
        self.assertIsNotNone(assessments)
        self.assertEqual(len(assessments), 3)
        guids, rows, headers = assessments
        self.assertEqual(len(guids), 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(headers), 90)


if __name__ == "__main__":
    unittest.main()
