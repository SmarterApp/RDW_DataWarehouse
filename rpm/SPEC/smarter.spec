# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

Name:		smarter%(echo ${SMARTER_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	SMARTER EdWare Reporting Web Application

Group:		WSGI Web Application
License: Amplify Education, Inc and ASL 2.0
URL:		http://www.amplify.com
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python3
BuildRequires:	python3-libs npm
Requires:	xmlsec1 python3-mod_wsgi xmlsec1-openssl xmlsec1-openssl-devel postgresql92-devel python3-libs
AutoReqProv: no

# force python3 to be passed to brp-python-bytecompile
BuildRequires: python3-devel
%global __python %{__python3}

%define _unpackaged_files_terminate_build 0

%description
EdWare smarter 
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})

%prep
rm -rf virtualenv/smarter
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter %{buildroot}/opt/edware
cp -r ${WORKSPACE}/scripts %{buildroot}/opt/edware
cp -r ${WORKSPACE}/assets %{buildroot}/opt/edware/assets
touch %{buildroot}/opt/edware/assets/__init__.py

%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv/smarter
source virtualenv/smarter/bin/activate

cp ${WORKSPACE}/scripts/repmgr_cleanup.sh virtualenv/smarter/bin/

# compile assets into BUILDROOT/opt/edware/assets
cd %{buildroot}/opt/edware/scripts
BUILDROOT=%{buildroot}
WORKSPACE_PATH=${BUILDROOT//\//\\\/}
sed -i.bak "s/assets.directory = \/path\/assets/assets.directory = ${WORKSPACE_PATH}\/opt\/edware\/assets/g" compile_assets.ini
sed -i.bak "s/smarter.directory = \/path\/smarter/smarter.directory = ${WORKSPACE_PATH}\/opt\/edware\/smarter/g" compile_assets.ini
python compile_assets.py
cd -

cd ${WORKSPACE}/config
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edcore
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edschema
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edauth
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edapi
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edworker
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/services
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edextract
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/edmigrate
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/smarter_common
python setup.py clean --all
easy_install -Z .
cd -
cd ${WORKSPACE}/hpz_client
python setup.py clean --all
easy_install -Z .
cd -
cd %{buildroot}/opt/edware/smarter
rm -rf assets
mv ../assets .
python setup.py clean --all
easy_install -Z .
cd -

deactivate
echo -e "/opt/edware/smarter\n." > virtualenv/smarter/lib/python3.3/site-packages/smarter.egg-link

%install
mkdir -p %{buildroot}/opt/virtualenv
cp -r virtualenv/smarter %{buildroot}/opt/virtualenv
find %{buildroot}/opt/virtualenv/smarter/bin -type f -exec sed -i -r 's/(\/[^\/]*)*\/rpmbuild\/BUILD/\/opt/g' {} \;

mkdir -p %{buildroot}/opt/edware/smarter
cp ${WORKSPACE}/smarter/smarter.wsgi %{buildroot}/opt/edware/smarter/
mkdir -p %{buildroot}/opt/edware/conf
cp ${WORKSPACE}/config/generate_ini.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/config/settings.yaml %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/config/comparing_populations_precache_filters.json %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/services/config/linux/opt/edware/conf/celeryd-services.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/edextract/config/linux/opt/edware/conf/celeryd-edextract.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/edmigrate/config/linux/opt/edware/conf/celeryd-edmigrate.conf %{buildroot}/opt/edware/conf/
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/services/config/linux/etc/rc.d/init.d/celeryd-services %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/edextract/config/linux/etc/rc.d/init.d/celeryd-edextract %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/edmigrate/config/linux/etc/rc.d/init.d/celeryd-edmigrate %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/edmigrate/config/linux/etc/rc.d/init.d/edmigrate-conductor %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/edmigrate/config/linux/etc/rc.d/init.d/repmgrd %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/edmigrate/config/linux/etc/rc.d/init.d/repmgrd-watcher %{buildroot}/etc/rc.d/init.d/

%clean

%files
%defattr(644,root,root,755)
/opt/edware/smarter/smarter.wsgi
/opt/edware/conf/generate_ini.py
/opt/edware/conf/settings.yaml
/opt/edware/conf/comparing_populations_precache_filters.json
/opt/edware/conf/celeryd-services.conf
/opt/edware/conf/celeryd-edextract.conf
/opt/edware/conf/celeryd-edmigrate.conf
/opt/virtualenv/smarter/include/*
/opt/virtualenv/smarter/lib/*
/opt/virtualenv/smarter/lib64
/opt/virtualenv/smarter/bin/activate
/opt/virtualenv/smarter/bin/activate.csh
/opt/virtualenv/smarter/bin/activate.fish
/opt/virtualenv/smarter/bin/activate_this.py
%attr(755,root,root) /opt/virtualenv/smarter/bin/bfg2pyramid
%attr(755,root,root) /opt/virtualenv/smarter/bin/easy_install
%attr(755,root,root) /opt/virtualenv/smarter/bin/easy_install-3.3
%attr(755,root,root) /opt/virtualenv/smarter/bin/initialize_smarter_db
%attr(755,root,root) /opt/virtualenv/smarter/bin/mako-render
%attr(755,root,root) /opt/virtualenv/smarter/bin/pcreate
%attr(755,root,root) /opt/virtualenv/smarter/bin/pip
%attr(755,root,root) /opt/virtualenv/smarter/bin/pip3
%attr(755,root,root) /opt/virtualenv/smarter/bin/prequest
%attr(755,root,root) /opt/virtualenv/smarter/bin/proutes
%attr(755,root,root) /opt/virtualenv/smarter/bin/pserve
%attr(755,root,root) /opt/virtualenv/smarter/bin/pshell
%attr(755,root,root) /opt/virtualenv/smarter/bin/ptweens
%attr(755,root,root) /opt/virtualenv/smarter/bin/pviews
%attr(755,root,root) /opt/virtualenv/smarter/bin/pygmentize
%attr(755,root,root) /opt/virtualenv/smarter/bin/python3.3
%attr(755,root,root) /opt/virtualenv/smarter/bin/celery
%attr(755,root,root) /opt/virtualenv/smarter/bin/celery
%attr(755,root,root) /opt/virtualenv/smarter/bin/celerybeat
%attr(755,root,root) /opt/virtualenv/smarter/bin/celeryctl
%attr(755,root,root) /opt/virtualenv/smarter/bin/celeryd
%attr(755,root,root) /opt/virtualenv/smarter/bin/celeryd-multi
%attr(755,root,root) /opt/virtualenv/smarter/bin/celeryev
%attr(755,root,root) /opt/virtualenv/smarter/bin/python
%attr(755,root,root) /opt/virtualenv/smarter/bin/python3
%attr(755,root,root) /opt/virtualenv/smarter/bin/repmgr_cleanup.sh
%attr(755,root,root) /etc/rc.d/init.d/celeryd-services
%attr(755,root,root) /etc/rc.d/init.d/celeryd-edextract
%attr(755,root,root) /etc/rc.d/init.d/celeryd-edmigrate
%attr(755,root,root) /etc/rc.d/init.d/edmigrate-conductor
%attr(755,root,root) /etc/rc.d/init.d/repmgrd
%attr(755,root,root) /etc/rc.d/init.d/repmgrd-watcher

%pre
id celery > /dev/null 2>&1
if [ $? != 0 ]; then
   useradd celery
   usermod -G fuse celery
fi
if [ ! -d /opt/edware/log ]; then
    mkdir -p /opt/edware/log
fi
if [ ! -d /var/log/celery-services ]; then
    mkdir -p /var/log/celery-services
    chown celery.celery /var/log/celery-services
fi
if [ ! -d /var/log/celery-edextract ]; then
    mkdir -p /var/log/celery-edextract
    chown celery.celery /var/log/celery-edextract
fi
if [ ! -d /var/log/celery-edmigrate ]; then
    mkdir -p /var/log/celery-edmigrate
    chown celery.celery /var/log/celery-edmigrate
fi
if [ ! -d /var/log/repmgrd ]; then
    mkdir -p /var/log/repmgrd
    if id -u postgres > /dev/null 2>&1 ; then
        chown postgres.postgres /var/log/repmgrd
    fi
fi
if [ ! -d /var/run/repmgrd ]; then
    mkdir -p /var/run/repmgrd
    if id -u postgres > /dev/null 2>&1; then
        chown postgres.postgres /var/run/repmgrd
    fi
fi

%post
chkconfig --add celeryd-services
chkconfig --add celeryd-edextract
chkconfig --add celeryd-edmigrate
chkconfig --add edmigrate-conductor
chkconfig --add repmgrd
chkconfig --add repmgrd-watcher
chkconfig --level 2345 celeryd-services off
chkconfig --level 2345 celeryd-edextract off
chkconfig --level 2345 celeryd-edmigrate off
chkconfig --level 2345 edmigrate-conductor off
chkconfig --level 2345 repmgrd off
chkconfig --level 2345 repmgrd-watcher off

%preun
chkconfig --del celeryd-services
chkconfig --del celeryd-edextract
chkconfig --del celeryd-edmigrate
chkconfig --del edmigrate-conductor
chkconfig --del repmgrd
chkconfig --del repmgrd-watcher

%postun


%changelog

