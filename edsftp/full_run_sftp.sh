# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

!/bin/bash
cd /opt/wgen/edware-udl/udl2/edware/edsftp
source /opt/wgen/edware-udl/udl2/python3.3/bin/activate
sudo python setup.py install
sleep 5
python sftp_driver.py --init
python sftp_driver.py -s -t test_tenant
python sftp_driver.py -a -u arrival_user -t test_tenant -r sftparrivals
python sftp_driver.py -a -u departure_user -t test_tenant -r tenantadmin
python sftp_driver.py --remove-user -u arrival_user
python sftp_driver.py --remove-user -u departure_user
python sftp_driver.py --remove-tenant -t test_tenant
python sftp_driver.py --cleanup