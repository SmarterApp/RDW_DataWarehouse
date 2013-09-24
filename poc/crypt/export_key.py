import os
import gnupg
from pprint import pprint
gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 
# key fingerprint can be obtained from above code block's output
key = "D38E8783385C9D2ED1AB96FA6ECB0274D8EE6B06"
 
 
# print the public/private key parts for the above key located
ascii_public_key = gpg.export_keys(key)
ascii_private_key = gpg.export_keys(key, True)
print(ascii_public_key)
print(ascii_private_key)
 
# writing keys to a file
with open('data/mykeyfile.asc', 'w') as f:
    f.write(ascii_public_key)
    f.write(ascii_private_key)