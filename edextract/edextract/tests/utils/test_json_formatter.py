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
Created on Dec 5, 2013

@author: dip
'''
import unittest
from edextract.utils.json_formatter import format_json, set_value
from collections import OrderedDict
import json


class TestJsonFormatter(unittest.TestCase):

    def test_format_json_empty_input(self):
        mapping = {}
        formatted = format_json(mapping)
        self.assertIsInstance(formatted, OrderedDict)
        self.assertEqual(len(formatted.keys()), 0)

    def test_format_json_no_dot_notation(self):
        mapping = OrderedDict()
        mapping["one"] = 1
        mapping["two"] = 2
        mapping["three"] = 3
        formatted = format_json(mapping)
        results = json.dumps(formatted)
        self.assertEqual(results, '{"one": "1", "two": "2", "three": "3"}')

    def test_format_json_values_are_strings(self):
        mapping = OrderedDict()
        mapping["one"] = 1
        mapping["two"] = "ste"
        mapping["three"] = None
        formatted = format_json(mapping)
        self.assertEqual(formatted["one"], str(mapping["one"]))
        self.assertEqual(formatted["two"], str(mapping["two"]))
        self.assertEqual(formatted["three"], "")

    def test_format_json_values_with_dot_notation(self):
        mapping = OrderedDict()
        mapping["one.a.b"] = 1
        mapping["one.a.c"] = 2
        mapping["two.a.b.c.d"] = 3
        mapping["three"] = 3
        formatted = format_json(mapping)
        self.assertEqual(formatted["one"]["a"]["b"], "1")
        self.assertEqual(formatted["one"]["a"]["c"], "2")
        self.assertEqual(formatted["three"], "3")
        self.assertEqual(formatted["two"]["a"]["b"]["c"]["d"], "3")

    def test_set_value_multi_keys(self):
        mapping = OrderedDict()
        set_value(mapping, ["one", "a", "b"], 1)
        self.assertEqual(mapping["one"]["a"]["b"], "1")

    def test_set_value_one_key(self):
        mapping = OrderedDict()
        set_value(mapping, ["one"], 1)
        self.assertEqual(mapping["one"], "1")


if __name__ == "__main__":
    unittest.main()
