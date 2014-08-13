import unittest
from smarter_score_batcher.mapping.item_level import ItemLevelCsvColumns


class TestCSVMetadata(unittest.TestCase):

    def test_get_item_level_csv_keys(self):
        items = ItemLevelCsvColumns.get_item_level_csv_keys(ItemLevelCsvColumns)
        items_from_class = [ItemLevelCsvColumns.KEY, ItemLevelCsvColumns.SEGMENT_ID, ItemLevelCsvColumns.POSTITION,
                            ItemLevelCsvColumns.CLIENT_ID, ItemLevelCsvColumns.OPERATIONAL, ItemLevelCsvColumns.ISSELECTED,
                            ItemLevelCsvColumns.FORMAT, ItemLevelCsvColumns.SCORE, ItemLevelCsvColumns.SCORE_STATUS,
                            ItemLevelCsvColumns.ADMIN_DATE, ItemLevelCsvColumns.NUMBER_VISITS, ItemLevelCsvColumns.STRAND,
                            ItemLevelCsvColumns.CONTENT_LEVEL, ItemLevelCsvColumns.PAGE_NUMBER, ItemLevelCsvColumns.PAGE_VISITS,
                            ItemLevelCsvColumns.PAGE_TIME, ItemLevelCsvColumns.DROPPED]

        self.assertEqual(items, items_from_class)

if __name__ == "__main__":
    unittest.main()
