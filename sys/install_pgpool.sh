wget http://yum.pgrpms.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch.rpm
rpm -Uvh pgdg-redhat91-9.1-5.noarch.rpm
yum install pgpool-II-91

#Configure pgpool.conf
#Copy the /etc/pgpool-II-91/pgpool.conf.sample to /etc/pgpool-II-91/pgpool.conf
cp /etc/pgpool-II-91/pgpool.conf.sample /etc/pgpool-II-91/pgpool.conf

