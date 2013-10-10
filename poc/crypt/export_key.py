import os
import gnupg
import argparse

from pprint import pprint
from gnupg_props import *
 
gpg = gnupg.GPG(gnupghome=GNUPG_HOME)
 
parser = argparse.ArgumentParser()
parser.add_argument("--key", dest="key")
args = parser.parse_args()
 
# print the public/private key parts for the above key located
ascii_public_key = gpg.export_keys(args.key)
ascii_private_key = gpg.export_keys(args.key, True)
print(ascii_public_key)
print(ascii_private_key)
 
# writing keys to a file
with open('DD87CFFF75C7BEC2.asc', 'w') as f:
    f.write(ascii_public_key)
    f.write(ascii_private_key)