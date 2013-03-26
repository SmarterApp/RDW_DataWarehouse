#pg922_yum_install.sh
#Add exclude to /etc/yum.repos.d/CentOS-Base.repo file [base] and [updates] sections:

#[base]
#...
#exclude=postgresql*
 
#[updates]
#...
#exclude=postgresql*

## CentOS 6 - x86_64 - 64-bit ##
rpm -Uvh http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-6.noarch.rpm

yum groupinstall "PostgreSQL Database Server PGDG"

service postgresql-9.2 initdb -D /opt/wgen/postgres/data

service postgresql-9.2 start

chkconfig postgresql-9.2 on
