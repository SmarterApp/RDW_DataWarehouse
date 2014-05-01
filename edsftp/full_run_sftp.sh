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