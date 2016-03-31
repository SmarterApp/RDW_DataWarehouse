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
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.helpers.percentage_calc import normalize_percentages


class Test(unittest.TestCase):

    def test_normalize_percentages(self):
        intervals = [13.62, 47.98, 9.59, 28.78]
        intervals = normalize_percentages(intervals)
        self.assertEqual([14, 48, 9, 29], intervals)

        intervals = [33.33, 33.33, 33.33]
        intervals = normalize_percentages(intervals)
        self.assertEqual([33, 33, 34], intervals)

        intervals = [33.34, 33.33, 33.33]
        intervals = normalize_percentages(intervals)
        self.assertEqual([34, 33, 33], intervals)

        intervals = [16.666, 16.666, 16.666, 16.666, 16.666, 16.666]
        intervals = normalize_percentages(intervals)
        self.assertEqual([16, 16, 17, 17, 17, 17], intervals)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
