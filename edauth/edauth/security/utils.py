'''
Created on Feb 22, 2013

@author: tosako
'''
import zlib
import base64


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
