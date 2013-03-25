#py33_centos_install.sh
#Add exclude to /etc/yum.repos.d/CentOS-Base.repo file [base] and [updates] sections:

#[base]
#...
#exclude=postgresql*
 
#[updates]
#...
#exclude=postgresql*

## CentOS 6 - x86_64 - 64-bit ##
sudo su -

rpm -Uvh http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-6.noarch.rpm

yum groupinstall "PostgreSQL Database Server PGDG"

yum install gcc openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel httpd httpd-devel
cd /usr/local/src
wget http://www.python.org/ftp/python/3.3.0/Python-3.3.0.tar.bz2
tar -xjf Python-3.3.0.tar.bz2
cd Python-3.3.0

./configure --enable-shared --prefix=/opt/python3
make clean
make 
make install

echo '/opt/python3/lib/' >> /etc/ld.so.conf.d/local-lib.conf;

/sbin/ldconfig

#check to make sure all of the python libs are properly linked
ldd /opt/python3/bin/python3.3


cd /opt/python3/bin
ln -s python3.3 python

cd ~
vi .bash_profile
# update .bash_profile
# PATH=/opt/python3/bin/:$PATH:$HOME/bin:/usr/pgsql-9.2/bin/
. .bash_profile

python -V

cd /usr/local/src
curl -O http://python-distribute.org/distribute_setup.py
python distribute_setup.py

# psycopg2
yum install postgresql-devel

easy_install psycopg2

#pyramid
easy_install pyramid;

# check the Makefile to ensure it is loading the right name of the python binary
# if make breaks, edit accordingly
cd /usr/local/
wget http://modwsgi.googlecode.com/files/mod_wsgi-3.4.tar.gz
tar xvfz mod_wsgi-3.4.tar.gz
cd /usr/local/src/mod_wsgi-3.4
./configure --with-apxs=/usr/sbin/apxs --with-python=/opt/python3/bin/python3.3
make
make install

#update httpd.conf to pickup pyramid/mod_wsgi requests