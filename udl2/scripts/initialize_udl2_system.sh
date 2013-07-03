#!/bin/sh
echo "make udl2 system user home"

sudo -u root -s "mkdir -p /opt/wgen/edware-udl/udl2/"
sudo -u root -s "chmod 777 /opt/wgen/edware-udl/udl2"
sudo -u root -s "mkdir -p /opt/wgen/edware-udl/udl2/.ssh"
sudo -u root -s "chmod 777 /opt/wgen/edware-udl/udl2/.ssh"

# create udl2 system users for
if [ `uname` == 'Linux' ]; then
    echo "create udl2 users to run udl2 celery and own the zone area for work"
    sudo -u root -s "useradd -d /opt/wgen/edware-udl/udl2 -r -s /bin/sh udl2"
    sudo -u root -s "passwd udl2"
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2"
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2/.ssh"
    sudo -u root -s "echo 'umask 0002' > /opt/wgen/edware-udl/udl2/.bashrc"
    sudo -u root -s "echo 'umask 0002' > /opt/wgen/edware-udl/udl2/.bash_profile"
    sudo -u root -s "echo 'umask 0002' > /opt/wgen/edware-udl/udl2/.profile"
    sudo -u root -s "echo 'umask 0002' > /opt/wgen/edware-udl/udl2/.login"
    sudo -u root -s "echo 'umask 0002' > /opt/wgen/edware-udl/udl2/.bash_login"
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2/.bash*"
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2/.profile"
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2/.loging"
fi
# create directories
sudo -u root -s "./initialize_udl2_directories.sh"

# copy current udl2 installation's code ssh
echo `pwd`
export CODE_DIR=`pwd`
echo "copy udl2 installations' ssh keys"

if [ `uname` == 'Linux' ]; then
    sudo -u root -s "cp `pwd`/../git/id_rsa /opt/wgen/edware-udl/udl2/.ssh"
    sudo -u root -s "cp `pwd`/../git/id_rsa.pub /opt/wgen/edware-udl/udl2/.ssh" 
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2/.ssh/id_rsa.pub"
    sudo -u root -s "chown udl2.udl2 /opt/wgen/edware-udl/udl2/.ssh/id_rsa"
    sudo -u root -s "chmod 600 /opt/wgen/edware-udl/udl2/.ssh/id_rsa.pub"
    sudo -u root -s "chmod 600 /opt/wgen/edware-udl/udl2/.ssh/id_rsa"
    sudo -u root -s "chmod 755 /opt/wgen/edware-udl/udl2/.ssh"
fi

# install virtualenv-3.3
echo "install virtualenv-3.3 for celery, due to python3 rpm install path under /opt/python3/bin, we need to specifiy the path"
cd /opt/wgen/edware-udl/udl2
echo "/opt/python3/bin/virtualenv-3.3 --distribute python3.3"

if [ `uname` == 'Linux' ]; then
    su - udl2 -c "/opt/python3/bin/virtualenv-3.3 --distribute python3.3"
else
    su - root -c "virtualenv-3.3 --distribute python3.3"
fi

# install virtualenv-2.7
echo "install virtual-2.7 for flower"
cd /opt/wgen/edware-udl/udl2
echo "virtualenv-2.7 --distribute python2.7"
if [ `uname` == 'Linux' ]; then
    su - udl2 -c "/usr/bin/virtualenv-2.7 --distribute python2.7";
else
    su - root -c "virtualenv-2.7 --distribute python2.7";
fi
# pull code from git
#echo "pull code from git"
#cd /opt/wgen/edware-udl/udl2
#su udl2 -c "git clone ssh://git@github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0"

#install all python dependency for udl2 code to python 3.3
echo "install all python dependency code for udl2"
cd  $CODE_DIR
cd ../

if [ `uname` == 'Linux' ]; then
    su - udl2 -c "source /opt/wgen/edware-udl/udl2/python3.3/bin/activate; /opt/wgen/edware-udl/udl2/python3.3/bin/python3.3 setup.py install";
else
    su - root -c "source /opt/wgen/edware-udl/udl2/python3.3/bin/activate; /opt/wgen/edware-udl/udl2/python3.3/bin/python3.3 setup.py install";
fi 
#install all python dependency for flower to monitor celery
echo "install all python dependency code for flower to minitor celery"
if [ `uname` == 'Linux' ]; then
    su - udl2 -c "source /opt/wgen/edware-udl/udl2/python2.7/bin/activate; /opt/wgen/edware-udl/udl2/python2.7/bin/pip-2.7 install flower";
else
    su - root -c "source /opt/wgen/edware-udl/udl2/python2.7/bin/activate; /opt/wgen/edware-udl/udl2/python2.7/bin/pip-2.7 install flower";
fi