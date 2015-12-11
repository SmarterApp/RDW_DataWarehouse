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
