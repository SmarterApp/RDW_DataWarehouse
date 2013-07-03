#!/bin/sh
echo "sudo -u root -s \"rm -fr /opt/wgen/edware-udl/*\""
sudo -u root -s rm -fr /opt/wgen/edware-udl/*
echo "sudo -u root -s \"/usr/sbin/userdel udl2\""
sudo -u root -s /usr/sbin/userdel udl2
