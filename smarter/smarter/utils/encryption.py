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
