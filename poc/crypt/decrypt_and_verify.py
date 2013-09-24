import os
import gnupg
import argparse
import time

from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("--source", dest="source_file")
parser.add_argument("--dest", dest="dest_file")
parser.add_argument("--passphrase", dest="passphrase", default=None)
args = parser.parse_args()

gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')

start=time.time()
with open(args.source_file, 'rb') as f:
    status = gpg.decrypt_file(f, passphrase=args.passphrase, output=args.dest_file)
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
	print ('time taken (ms): ', round((end-start)*1000))
	print ('signer: ', status.username)
	print ('signer key id: ', status.key_id)
	print ('signer key fingerprint: ', status.fingerprint)
	print ('signer signature id: ', status.signature_id)
	print ('signer trust level: ', status.trust_level)
	print ('signer trust text: ', status.trust_text)
else:
	print('FAILED') 