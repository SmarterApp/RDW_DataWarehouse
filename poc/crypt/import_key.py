import os
import gnupg
from pprint import pprint
gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 
key_data = open('/Users/Shared/Amplify/wgen_dev/edware/poc/crypt/data/foopubkey.txt').read()
import_result = gpg.import_keys(key_data)
pprint(import_result.count)
pprint(import_result.results)