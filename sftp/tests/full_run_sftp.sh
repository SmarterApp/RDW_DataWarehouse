#!/bin/bash
cd /Users/Shared/Amplify/edware/sftp
sudo python setup.py install
sleep 5
python sftp_driver.py --init
python sftp_driver.py --cleanup
