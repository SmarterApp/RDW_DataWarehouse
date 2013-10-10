import os
import subprocess
import csv
import math
import argparse
import datetime
import logging
import gnupg

logger = logging.getLogger(__name__)


def _is_file_exists(file_to_decrypt):
    '''
    check if file exists and readable
    '''
    return os.path.isfile(file_to_decrypt) and os.access(file_to_decrypt, os.R_OK)


def _is_valid__file(file_to_decrypt):
    '''
    Basic file validation checks before decrypting
    '''
    valid = False
    if _is_file_exists(file_to_decrypt):
        valid = True
        logger.log("File exists and is readable -- %s " % file_to_decrypt)
    else:
        logger.error("File missing or un-readable -- %s " % file_to_decrypt)

    return valid


def _print_status(status):
    logger.info('ok: ', status.ok)
    logger.debug('status: ', status.status)
    logger.debug('stderr: ', status.stderr)
    if(status.ok):
        logger.debug('signer: ', status.username)
        logger.debug('signer key id: ', status.key_id)
        logger.debug('signer key fingerprint: ', status.fingerprint)
        logger.debug('signer signature id: ', status.signature_id)
        logger.debug('signer trust level: ', status.trust_level)
        logger.debug('signer trust text: ', status.trust_text)


def _decrypt_file_contents(file_to_decrypt, output_file, passphrase, gpg_home):
    '''
    verify signature, decrypt and write the decrypted file to the destination directory
    '''
    gpg = gnupg.GPG(gnupghome=gpg_home)
    with open(file_to_decrypt, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=passphrase, output=output_file)
    return status


def decrypt_file(file_to_decrypt, destination_dir, passphrase, gpg_home):
    '''
    Verify and Decrypt the file after needed validations
    '''
    if not _is_valid__file(file_to_decrypt):
        raise Exception('Invalid source file -- %s' % file_to_decrypt)

    output_file = destination_dir + '/' + os.path.splitext(os.path.basename(file_to_decrypt))[0]
    status = _decrypt_file_contents(file_to_decrypt, output_file, passphrase, gpg_home)

    _print_status(status)

    if not status.ok:
        raise Exception('Decryption Failed')
    if status.trust_level is None or status.trust_level < 4:
        raise Exception('Verification Failed. Signature not trusted')
    return (status, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process file decrypter args')
    parser.add_argument('-i', '--input', dest='file_to_decrypt', help='file_to_expand')
    parser.add_argument('-o', '--output', dest='destination_dir', default='.', help='output directory')
    parser.add_argument('-p', '--passphrase', dest='passphrase', default=None, help='passphrase to access private verifier key')
    parser.add_argument('-gh', '--gpghome', dest='gpg_home', help='GPG Home directory for keys')

    args = parser.parse_args()
    print("Input file is: " + args.file_to_decrypt)
    print("Passphrase: " + args.passphrase)
    if args.destination_dir:
        print("Decrypt files to: " + args.destination_dir)

    decrypt_file(args.file_to_decrypt, args.destination_dir, args.passphrase, args.gpg_home)
