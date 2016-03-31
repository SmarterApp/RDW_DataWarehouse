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

import unittest
from smarter_score_batcher.processing.item_level import ItemLevelCsvColumns


class TestCSVMetadata(unittest.TestCase):

    def test_get_item_level_csv_keys(self):
        items = ItemLevelCsvColumns.get_item_level_csv_keys()
        items_from_class = [ItemLevelCsvColumns.KEY, ItemLevelCsvColumns.SEGMENT_ID, ItemLevelCsvColumns.POSTITION,
                            ItemLevelCsvColumns.CLIENT_ID, ItemLevelCsvColumns.OPERATIONAL, ItemLevelCsvColumns.ISSELECTED,
                            ItemLevelCsvColumns.FORMAT, ItemLevelCsvColumns.SCORE, ItemLevelCsvColumns.SCORE_STATUS,
                            ItemLevelCsvColumns.ADMIN_DATE, ItemLevelCsvColumns.NUMBER_VISITS, ItemLevelCsvColumns.STRAND,
                            ItemLevelCsvColumns.CONTENT_LEVEL, ItemLevelCsvColumns.PAGE_NUMBER, ItemLevelCsvColumns.PAGE_VISITS,
                            ItemLevelCsvColumns.PAGE_TIME, ItemLevelCsvColumns.DROPPED]

        self.assertEqual(items, items_from_class)

if __name__ == "__main__":
    unittest.main()
