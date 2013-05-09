#!/bin/sh

echo "make option directory"
sudo mkdir -p /opt/wgen/edware-udl/etc
# we need to fix permission later not to own by root by udl app user
chmod 755 /opt/wgen
chmod 755 /opt/wgen/edware-udl
chmod 777 /opt/wgen/edware-udl/etc

echo "make log directory"
sudo mkdir -p /var/log/wgen/edware-udl/logs
# we need to fix permission later not to own by root by udl app user
chmod 755 /var/log/
chmod 755 /var/log/wgen
chmod 755 /var/log/wgen/edware-udl/
chmod 777 /var/log/wgen/edware-udl/logs

echo "make zones directory"
sudo mkdir -p /opt/wgen/edware-udl/zones/
sudo mkdir -p /opt/wgen/edware-udl/zones/landing
sudo mkdir -p /opt/wgen/edware-udl/zones/work
sudo mkdir -p /opt/wgen/edware-udl/zones/history
# we need to fix permission later not to own by root by udl app user
chmod 755 /opt/wgen/edware-udl/zones
chmod 777 /opt/wgen/edware-udl/zones/landing
chmod 777 /opt/wgen/edware-udl/zones/work
chmod 777 /opt/wgen/edware-udl/zones/history