#!bash
#http://www.andrewzammit.com/blog/installing-jenkins-ci-on-centos-6-x-tomcat-with-an-ajp-proxy/
sudo su -
yum install screen;
yum install java-1.6.0-openjdk

wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo;
rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key;
yum install jenkins;

yum install httpd;

vi /etc/sysconfig/iptables;
#-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
#-A INPUT -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT

#*filter
#:INPUT ACCEPT [0:0]
#:FORWARD ACCEPT [0:0]
#:OUTPUT ACCEPT [0:0]
#-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#-A INPUT -p icmp -j ACCEPT
#-A INPUT -i lo -j ACCEPT
#-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
# added the following line
#-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
#-A INPUT -j REJECT --reject-with icmp-host-prohibited
#-A FORWARD -j REJECT --reject-with icmp-host-prohibited
#COMMIT

service iptables restart;

#apache/ajp reverse proxy should be set up after the environments have been secured.

grep ajp /etc/httpd/conf/httpd.conf

vi /etc/httpd/conf.d/vhosts.conf

#ADD The Following...
#NameVirtualHost *:80
#<VirtualHost *:80>
#        ServerName jenkins.host.tld
#        ProxyRequests Off
#        ProxyPreserveHost On
#        ProxyPass / ajp://127.0.0.1:8009/
#        ProxyPassReverse / ajp://127.0.0.1:8009/
#        ProxyPassReverseCookiePath / /
#</VirtualHost>

service httpd restart;

service jenkins restart;