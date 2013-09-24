import os
import gnupg
from pprint import pprint
gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 
with open('data/my-encrypted.txt.gpg', 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='edware udl2', output='data/my-decrypted.txt')
 
print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)