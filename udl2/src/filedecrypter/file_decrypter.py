import os
import subprocess
import csv
import math
import argparse
import datetime
import logging
import gnupg

logger = logging.getLogger(__name__)

gpg = gnupg.GPG(gnupghome='/Users/sravi/.gnupg')

def __is_file_exists(file_to_decrypt):
    '''
    check if file exists and readable
    '''
    return os.path.isfile(file_to_decrypt) and os.access(file_to_decrypt, os.R_OK)


def __is_valid__file(file_to_decrypt):
    '''
    Basic file validation checks before decrypting
    '''
    valid = False
    if __is_file_exists(file_to_decrypt):
        valid = True
        print("File exists and is readable -- %s " % file_to_decrypt)
    else:
        print("File missing or un-readable -- %s " % file_to_decrypt)        

    return valid


def __print_status(status):
    print ('ok: ', status.ok)
    print ('status: ', status.status)
    print ('stderr: ', status.stderr)

    if(status.ok):
        print('SUCCESS')
        print ('signer: ', status.username)
        print ('signer key id: ', status.key_id)
        print ('signer key fingerprint: ', status.fingerprint)
        print ('signer signature id: ', status.signature_id)
        print ('signer trust level: ', status.trust_level)
        print ('signer trust text: ', status.trust_text)
    else:
        print('FAILED')


def __decrypt_file_contents(file_to_decrypt, destination_dir, passphrase):
    '''
    verify signature, decrypt and write the decrypted file to the destination directory
    '''
    output_file = destination_dir + '/' + os.path.splitext(os.path.basename(file_to_decrypt))[0]
    with open(file_to_decrypt, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=passphrase, output=output_file)

    return status


def decrypt_file(file_to_decrypt, destination_dir, passphrase):
    '''
    Verify and Decrypt the file after needed validations
    '''
    if not __is_valid__file(file_to_decrypt):
        raise Exception('Invalid source file -- %s' % file_to_decrypt)

    status = __decrypt_file_contents(file_to_decrypt, destination_dir, passphrase)
    __print_status(status)
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file decrypter args')
    parser.add_argument('-i', '--input', dest='file_to_decrypt', help='file_to_expand')
    parser.add_argument('-o', '--output', dest='destination_dir', default='.', help='output directory')
    parser.add_argument('-p', '--passphrase', dest='passphrase', default=None, help='passphrase to access private verifier key')

    args = parser.parse_args()
    print("Input file is: " + args.file_to_decrypt)
    print("Passphrase: " + args.passphrase)
    if args.destination_dir:
        print("Decrypt files to: " + args.destination_dir)

    decrypt_file(args.file_to_decrypt, args.destination_dir, args.passphrase)