import os
import gnupg
from pprint import pprint
gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 
#open('data/my-unencrypted.txt', 'w').write('EdWare Secret Data')
with open('data/my-unencrypted.txt', 'rb') as f:
    status = gpg.encrypt_file(f,'edware_dataprovider_1@amplify.com', output='data/my-encrypted.txt.gpg')
 
print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)