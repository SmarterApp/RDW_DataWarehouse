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
Created on Nov 18, 2015

@author: sshrestha
'''
import unittest
from smarter.utils.encryption import encode, decode


class Test(unittest.TestCase):

    def test_encode_decode(self):
        secret_key = 'test_secret_pass'
        string = 'Example'
        encoded = encode(secret_key, string)
        self.assertNotEqual(string, encoded)
        self.assertTrue(len(encoded) > 20)
        self.assertEqual(string, decode(secret_key, encoded))

if __name__ == "__main__":
    unittest.main()
