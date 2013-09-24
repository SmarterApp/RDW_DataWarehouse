import os
import gnupg
 
# uncomment the below line if you want to start fresh by removing all old keys generated
#os.system('rm -rf /Users/Shared/Amplify/wgen_dev/gpghome')
gpg = gnupg.GPG(gnupghome='/Users/Shared/Amplify/wgen_dev/gpghome')

#key1
input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, name_email='edware_dataprovider_1@amplify.com',passphrase='edware udl2')
key = gpg.gen_key(input_data)
print(key)

#key2
input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, name_email='amplify@amplify.com',passphrase='edware udl2')
key = gpg.gen_key(input_data)
print(key)