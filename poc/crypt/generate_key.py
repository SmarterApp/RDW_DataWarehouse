import os
import gnupg
import argparse
from gnupg_props import *
 
gpg = gnupg.GPG(gnupghome=GNUPG_HOME)

parser = argparse.ArgumentParser()
parser.add_argument("--email", dest="name_email")
parser.add_argument("--passphrase", dest="passphrase", default=None)
args = parser.parse_args()

#key1
input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, name_email=args.name_email,passphrase=args.passphrase)
key = gpg.gen_key(input_data)
print('Generated key: '+ str(key))