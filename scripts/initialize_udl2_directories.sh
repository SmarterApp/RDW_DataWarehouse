#!/bin/sh

echo "make option directory"
sudo mkdir -p /opt/wgen/edware-udl/etc

echo "make log directory"
sudo mkdir -p /var/log/wgen/edware-udl/logs

echo "make zones directory"
sudo mkdir -p /opt/wgen/edware-udl/zones/
sudo mkdir -p /opt/wgen/edware-udl/zones/landing
sudo mkdir -p /opt/wgen/edware-udl/zones/work
sudo mkdir -p /opt/wgen/edware-udl/zones/history