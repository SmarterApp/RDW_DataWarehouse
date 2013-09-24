import os
import gnupg
from pprint import pprint

gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 
public_keys = gpg.list_keys()
private_keys = gpg.list_keys(True)
pprint(public_keys)
pprint(private_keys)