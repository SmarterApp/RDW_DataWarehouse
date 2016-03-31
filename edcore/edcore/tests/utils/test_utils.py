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
Created on Sep 1, 2013

@author: dip
'''
import unittest
from edcore.utils.utils import merge_dict, delete_multiple_entries_from_dictionary_by_list_of_keys,\
    reverse_map, get_config_from_ini


class TestUtils(unittest.TestCase):

    def test_merge_dict(self):
        self.assertDictEqual(merge_dict({}, {}), {})
        self.assertDictEqual(merge_dict({'a': 'b'}, {'c': 'd'}),
                             {'a': 'b', 'c': 'd'})
        self.assertDictEqual(merge_dict({'a': 'b'}, {'a': 'd'}), {'a': 'b'})

    def test_delete_multiple_entries_from_dictionary_by_list_of_keys(self):
        self.assertDictEqual(delete_multiple_entries_from_dictionary_by_list_of_keys({}, ['a']), {})
        self.assertDictEqual(delete_multiple_entries_from_dictionary_by_list_of_keys({'a': 1}, 'b'), {'a': 1})
        self.assertDictEqual(delete_multiple_entries_from_dictionary_by_list_of_keys({'a': 1}, 'a'), {})

    def test_get_config_from_ini(self):
        settings = {'a.b': 1, 'a.c': 'b', 'b.c': 2}
        self.assertEqual({'a.b': 1, 'a.c': 'b'}, get_config_from_ini(settings, 'a'), 'Subsettings should be filtered')
        self.assertEqual({'b': 1, 'c': 'b'}, get_config_from_ini(settings, 'a', True), 'Subsettings should be filtered and prefix removed')

    def test_reverse_map(self):
        _map = {'a': 'b', 'c': 'd'}
        reverse = reverse_map(_map)
        self.assertEqual(reverse['b'], 'a')

    def test_reverse_empty(self):
        _map = {}
        reverse = reverse_map(_map)
        self.assertEqual(len(reverse.keys()), 0)

if __name__ == "__main__":
    unittest.main()
