#!/bin/sh
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


echo "make option directory"
sudo -u root -s mkdir -p /opt/edware/conf
# we need to fix permission later not to own by root but udl app user
sudo -u root -s chmod 775 /opt/edware
sudo -u root -s chmod 777 /opt/edware/conf
if [ `uname` == 'Linux' ]; then
    sudo -u root -s chown -R udl2.udl2 /opt/edware/conf;
fi

echo "rebuild log directory"
sudo -u root -s rm -fr /opt/edware/log

echo "make log directory"
sudo -u root -s mkdir -p /opt/edware/log
# we need to fix permission later not to own by root but udl app user
sudo -u root -s chmod 775 /opt/edware/
sudo -u root -s chmod 777 /opt/edware/log
if [ `uname` == 'Linux' ]; then
    sudo -u root -s chown -R udl2.udl2 /opt/edware/log;
fi

echo "rebuild zones directory"
sudo -u root -s rm -fr /opt/edware/zones

echo "make zones directory"
sudo -u root -s mkdir -p /opt/edware/zones
sudo -u root -s mkdir -p /opt/edware/zones/landing
sudo -u root -s mkdir -p /opt/edware/zones/pickup

sudo -u root -s mkdir -p /opt/edware/zones/landing/work
sudo -u root -s mkdir -p /opt/edware/zones/landing/arrivals
sudo -u root -s mkdir -p /opt/edware/zones/landing/history

sudo -u root -s mkdir -p /opt/edware/zones/pickup/work
sudo -u root -s mkdir -p /opt/edware/zones/pickup/departures
sudo -u root -s mkdir -p /opt/edware/zones/pickup/history

# For testing
sudo -u root -s mkdir -p /opt/edware/zones/datafiles
sudo -u root -s mkdir -p /opt/edware/zones/datafiles/keys
sudo -u root -s mkdir -p /opt/edware/zones/tests

# we need to fix permission later not to own by root but udl app user
sudo -u root -s chmod 777 /opt/edware/zones/
sudo -u root -s chmod 777 /opt/edware/zones/landing
sudo -u root -s chmod 777 /opt/edware/zones/pickup

sudo -u root -s chmod 777 /opt/edware/zones/landing/work
sudo -u root -s chmod 777 /opt/edware/zones/landing/arrivals
sudo -u root -s chmod 777 /opt/edware/zones/landing/history
sudo -u root -s chmod 777 /opt/edware/zones/pickup/work
sudo -u root -s chmod 777 /opt/edware/zones/pickup/departures
sudo -u root -s chmod 777 /opt/edware/zones/pickup/history

sudo -u root -s chmod 777 /opt/edware/zones/landing/history
sudo -u root -s chmod 777 /opt/edware/zones/datafiles
sudo -u root -s chmod 777 /opt/edware/zones/datafiles/keys
sudo -u root -s chmod 777 /opt/edware/zones/tests

# we need to fix owner to udl2
if [ `uname` == 'Linux' ]; then
    sudo -u root -s chown -R udl2.udl2 /opt/edware/zones/ ;
fi