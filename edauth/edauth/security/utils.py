'''
Created on Feb 22, 2013

@author: tosako
'''
import zlib
import base64
from Crypto.Cipher import AES
from Crypto import Random
from zope import interface, component
from zope.interface.declarations import implementer
from edauth.utils import enum


SECURITY_EVENT_TYPE = enum(INFO=0, WARN=1)


def deflate_base64_encode(data_byte_string):
    '''
    deflate and encode string to base64
    '''
    compressed = zlib.compress(data_byte_string)
    # Strip away the first 2 bytes (header) and 4 bytes (checksum)
    return base64.b64encode(compressed[2:-4])


def inflate_base64_decode(data_byte_string):
    '''
    inflate and decode base64 to string
    '''
    base_decoded = base64.b64decode(data_byte_string)
    return zlib.decompress(base_decoded, -15)


def _get_cipher():
    return component.getUtility(ICipher)


class ICipher(interface.Interface):
    '''
    simple cipher interface
    '''
    def encrypt(self, data):
        pass

    def decrypt(self, data):
        pass


@implementer(ICipher)
class AESCipher:
    '''
    AES implementation
    '''
    block_size = AES.block_size
    padding = b'\x00'

    def __init__(self, key):
        self.key = key.encode()
        if len(key) not in AES.key_size:
            raise Exception('KeySize for AES cipher is wrong')

    def pad_data(self, s):
        padding_length = self.block_size - len(s) % self.block_size
        if (padding_length == self.block_size):
            return s
        return s + padding_length * self.padding

    def unpad_data(self, s):
        return s.rstrip(self.padding)

    def encrypt(self, s):
        data = s.encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return deflate_base64_encode(iv + cipher.encrypt(self.pad_data(data)))

    def decrypt(self, s):
        data = inflate_base64_decode(s)
        iv = data[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad_data(cipher.decrypt(data[self.block_size:])).decode('UTF-8')
