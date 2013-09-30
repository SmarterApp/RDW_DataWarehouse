import os
import gnupg
from pprint import pprint
from gnupg_props import *
 
gpg = gnupg.GPG(gnupghome=GNUPG_HOME)
 
public_keys = gpg.list_keys()
private_keys = gpg.list_keys(True)
pprint(public_keys)
pprint(private_keys)