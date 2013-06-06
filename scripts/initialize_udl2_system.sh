#!/bin/sh

# create udl2 system users for
echo "create udl2 users to run udl2 celery and own the zone area for work"
sudo -u root -s "useradd -h /opt/wgen/edware-udl/udl2 -r -s /bin/sh udl2"

# install virtualenv-3.3
echo "install virtualenv-3.3 for celery"
cd /opt/wgen/edware-udl/udl2
sudo -u udl2 -s "virtualenv-3.3 --distribute python3.3"

# install virtualenv-2.7
echo "install virtual-2.7 for flower"
cd /opt/wgen/edware-udl/udl2
sudo -u udl2 -s "virtualenv-2.7 --distribute python2.7"

# pull code from git
echo "pull code from git"
cd /opt/wgen/edware-udl/udl2
sudo -u udl2 -s "git clone ssh://git@github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0"

#install all python dependency for udl2 code to python 3.3
echo "install all python dependency code for udl2"
cd /opt/wgen/edware-udl2/udl2/edware-udl2-2.0
source /opt/wgen/edware-udl2/udl2/python3.3/bin/activate
sudo -u udl2 -s "python3.3 setup.py install"

#install all python dependency for flower to monitor celery
echo "install all python dependency code for flower to minitor celery"
source /opt/wgen/edware-udl2/udl2/python2.7/bin/activate
sudo -u udl2 -s "pip-2.7 install flower"

