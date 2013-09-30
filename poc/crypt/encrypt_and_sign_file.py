import os
import gnupg
import argparse
import time

from pprint import pprint
from gnupg_props import *

parser = argparse.ArgumentParser()
parser.add_argument("--source", dest="source_file")
parser.add_argument("--dest", dest="dest_file")
parser.add_argument("--sendto", dest="sendto")
parser.add_argument("--signwith", dest="signwith")
parser.add_argument("--passphrase", dest="passphrase", default=None)
args = parser.parse_args()

gpg = gnupg.GPG(gnupghome=GNUPG_HOME)

start=time.time()
with open(args.source_file, 'rb') as f:
    status = gpg.encrypt_file(f,args.sendto, sign=args.signwith, passphrase=args.passphrase, output=args.dest_file)
end=time.time()

print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)

if(status.ok):
	print('SUCCESS')
	if(os.path.isfile(args.source_file)):
		print ('source file size (B): ', os.path.getsize(args.source_file))
	if(os.path.isfile(args.dest_file)):
		print ('encrypted file size (B): ', os.path.getsize(args.dest_file))
		print ('signed with: ', args.signwith)
	print ('time taken (ms): ', round((end-start)*1000))
else:
	print('FAILED')