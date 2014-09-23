import unittest
from smarter_score_batcher import get_sub_settings_by_prefix


class TestInit(unittest.TestCase):
    def test_get_sub_settings_by_prefix(self):
        settings = {'a.b': 1, 'a.c': 'b', 'b.c': 2}
        self.assertEqual({'a.b': 1, 'a.c': 'b'}, get_sub_settings_by_prefix(settings, 'a'), 'Subsettings should be filtered')
        self.assertEqual({'b': 1, 'c': 'b'}, get_sub_settings_by_prefix(settings, 'a', True), 'Subsettings should be filtered and prefix removed')
