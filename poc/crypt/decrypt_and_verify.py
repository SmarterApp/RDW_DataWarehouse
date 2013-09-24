import os
import gnupg
from pprint import pprint
gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 
with open('/Users/Shared/Amplify/wgen_dev/edware/poc/crypt/data/foo1.txt.gpg.gpg', 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='edware udl2', output='/Users/Shared/Amplify/wgen_dev/edware/poc/crypt/data/foo1-verified-decrypted.txt')
 
print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)
print ('signer: ', status.username)
print ('signer key id: ', status.key_id)
print ('signer key fingerprint: ', status.fingerprint)
print ('signer signature id: ', status.signature_id)
print ('signer trust level: ', status.trust_level)
print ('signer trust text: ', status.trust_text)