#!/bin/sh

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