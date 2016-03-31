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
from edauth.security.utils import AESCipher


def encode(passphrase, string):
    '''
    Encrypt string using secret passphrase

    :param passphrase:  secret passphrase
    :param string: string to encrypt
    '''
    aes = AESCipher(passphrase)
    return aes.encrypt_url_safe(string).decode("utf-8")


def decode(passphrase, string):
    '''
    Decrypt string using passphrase key

    :param passphrase:  secret passphrase
    :param string: string to decrypt
    '''
    aes = AESCipher(passphrase)
    return aes.decrypt_url_safe(string)
