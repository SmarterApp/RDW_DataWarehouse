import os
import gnupg
import argparse
import time

from pprint import pprint

gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')
 

parser = argparse.ArgumentParser()
parser.add_argument("--source", dest="source_file")
parser.add_argument("--dest", dest="dest_file")
parser.add_argument("--sendto", dest="sendto")
parser.add_argument("--signwith", dest="signwith")
parser.add_argument("--passphrase", dest="passphrase")
args = parser.parse_args()

start=time.time()
with open(args.source_file, 'rb') as f:
    status = gpg.encrypt_file(f,args.sendto, sign=args.signwith, passphrase=args.passphrase, output=args.dest_file)
end=time.time()

print ('ok: ', status.ok)
print ('status: ', status.status)
print ('stderr: ', status.stderr)
print ('source file size (B): ', os.path.getsize(args.source_file))
print ('time taken (ms): ', round((end-start)*1000))
print ('encrypted file size (B): ', os.path.getsize(args.dest_file))
print ('signed with: ', args.signwith)