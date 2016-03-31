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
Created on Aug 12, 2014

@author: tosako
'''
import unittest
import os
from smarter_score_batcher.utils.xsd import XSD
import hashlib


class Test(unittest.TestCase):

    def test_XSD(self):
        here = os.path.abspath(os.path.dirname(__file__))
        xsd_file_path = os.path.abspath(os.path.join(here, '..', '..', '..', 'resources', 'sample_xsd.xsd'))
        xsd = XSD(xsd_file_path)
        m1 = hashlib.md5()
        m1.update(bytes(xsd.get_xsd(), 'utf-8'))
        m2 = hashlib.md5()
        with open(xsd_file_path) as f:
            m2.update(bytes(f.read(), 'utf-8'))
        self.assertEqual(m1.digest(), m2.digest())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
