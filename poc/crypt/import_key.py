import os
import gnupg
import argparse
from pprint import pprint
from gnupg_props import *

gpg = gnupg.GPG(gnupghome=GNUPG_HOME)

parser = argparse.ArgumentParser()
parser.add_argument("--key_file", dest="key_file")
args = parser.parse_args()

key_data = open(args.key_file).read()
import_result = gpg.import_keys(key_data)
pprint(import_result.count)
pprint(import_result.results)