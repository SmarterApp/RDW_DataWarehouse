#!/bin/sh

echo "make option directory"
sudo -u root -s mkdir -p /opt/wgen/edware-udl/etc
# we need to fix permission later not to own by root but udl app user
sudo -u root -s chmod 775 /opt/wgen
sudo -u root -s chmod 775 /opt/wgen/edware-udl
sudo -u root -s chmod 777 /opt/wgen/edware-udl/etc
if [ `uname` == 'Linux' ]; then
    sudo -u root -s chown -R udl2.udl2 /opt/wgen/edware-udl/etc;
fi

echo "rebuild log directory"
sudo -u root -s rm -fr /var/log/wgen/edware-udl/logs

echo "make log directory"
sudo -u root -s mkdir -p /var/log/wgen/edware-udl/logs
# we need to fix permission later not to own by root but udl app user
sudo -u root -s chmod 775 /var/log/
sudo -u root -s chmod 775 /var/log/wgen/
sudo -u root -s chmod 775 /var/log/wgen/edware-udl/
sudo -u root -s chmod 777 /var/log/wgen/edware-udl/logs
if [ `uname` == 'Linux' ]; then
    sudo -u root -s chown -R udl2.udl2 /var/log/wgen/edware-udl/logs;
fi

echo "rebuild zones directory"
sudo -u root -s rm -fr /opt/wgen/edware-udl/zones

echo "make zones directory"
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup

sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing/work
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing/arrivals
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/landing/history

sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/work
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/departures
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/pickup/history

# For testing
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/datafiles
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/datafiles/keys
sudo -u root -s mkdir -p /opt/wgen/edware-udl/zones/tests

# we need to fix permission later not to own by root but udl app user
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup

sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/work
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/arrivals
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/history
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/work
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/departures
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/pickup/history

sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/landing/history
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/datafiles
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/datafiles/keys
sudo -u root -s chmod 777 /opt/wgen/edware-udl/zones/tests

# we need to fix owner to udl2
if [ `uname` == 'Linux' ]; then
    sudo -u root -s chown -R udl2.udl2 /opt/wgen/edware-udl/zones/ ;
fi