Name:		udl2%(echo ${UDL2_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	Edware's Universal Data Loader
Group:		ETL pipeline
License:	Proprietary software
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Vendor: Amplify Insight Edware Team <edwaredev@wgen.net>
Url: https://github.wgenhq.net/Ed-Ware-SBAC/edware

BuildRequires:	python3
BuildRequires:	python3-libs
AutoReqProv: no

%define _unpackaged_files_terminate_build 0

%description
EdWare UDL2
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})


%prep
rm -rf virtualenv
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/udl2 %{buildroot}/opt/edware
cp -r ${WORKSPACE}/edschema %{buildroot}/opt/edware
mkdir -p %{buildroot}/opt/edware/conf
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/udl2/conf/linux/opt/edware/conf/celeryd-udl2.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/udl2/conf/udl2_conf.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/udl2/conf/linux/etc/rc.d/init.d/celeryd-udl2 %{buildroot}/etc/rc.d/init.d/

%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv
source virtualenv/bin/activate

cd ${WORKSPACE}/edschema
python setup.py install
cd -
cd ${WORKSPACE}/udl2
python setup.py install
cd -

deactivate
find virtualenv/bin -type f -exec sed -i 's/\/var\/lib\/jenkins\/rpmbuild\/BUILD/\/opt/g' {} \;

%install
cp -r virtualenv %{buildroot}/opt

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,-)
/opt/edware/conf/celeryd-udl2.conf
/opt/edware/conf/udl2_conf.py
/opt/virtualenv/include/*
/opt/virtualenv/lib/*
/opt/virtualenv/lib64
/opt/virtualenv/bin/activate
/opt/virtualenv/bin/activate.csh
/opt/virtualenv/bin/activate.fish
/opt/virtualenv/bin/activate_this.py
%attr(755,root,root) /opt/virtualenv/bin/easy_install
%attr(755,root,root) /opt/virtualenv/bin/easy_install-3.3
%attr(755,root,root) /opt/virtualenv/bin/initialize_udl2_database.sh
%attr(755,root,root) /opt/virtualenv/bin/teardown_udl2_database.sh
%attr(755,root,root) /opt/virtualenv/bin/initialize_udl2_system.sh
%attr(755,root,root) /opt/virtualenv/bin/initialize_udl2_database_user.sh
%attr(755,root,root) /opt/virtualenv/bin/initialize_udl2_directories.sh
%attr(755,root,root) /opt/virtualenv/bin/initialize_udl2_database_user.sh
%attr(755,root,root) /opt/virtualenv/bin/start_rabbitmq.sh
%attr(755,root,root) /opt/virtualenv/bin/driver.py
%attr(755,root,root) /opt/virtualenv/bin/add_tenant.sh
%attr(755,root,root) /opt/virtualenv/bin/start_rabbitmq.py
%attr(755,root,root) /opt/virtualenv/bin/pip
%attr(755,root,root) /opt/virtualenv/bin/pip-3.3
%attr(755,root,root) /opt/virtualenv/bin/python3.3
%attr(755,root,root) /opt/virtualenv/bin/celery
%attr(755,root,root) /opt/virtualenv/bin/celerybeat
%attr(755,root,root) /opt/virtualenv/bin/celeryctl
%attr(755,root,root) /opt/virtualenv/bin/celeryd
%attr(755,root,root) /opt/virtualenv/bin/celeryd-multi
%attr(755,root,root) /opt/virtualenv/bin/celeryev
/opt/virtualenv/bin/python
/opt/virtualenv/bin/python3
%attr(755,root,root) /etc/rc.d/init.d/celeryd-udl2

%pre
id celery > /dev/null 2>&1
if [ $? != 0 ]; then
   useradd celery
   useradd udl2
fi
UDL2_ROOT=/opt/edware
UDL2_ZONES=$UDL2_ROOT/zones

if [ ! -d $UDL2_ROOT/log ]; then
    mkdir -p $UDL2_ROOT/log
fi

if [ ! -d $UDL2_ZONES ]; then
    mkdir -p $UDL2_ZONES
fi

if [ ! -d $UDL2_ZONES/landing ]; then
    mkdir -p $UDL2_ZONES/landing
fi

if [ ! -d $UDL2_ZONES/landing/arrivals ]; then
    mkdir -p $UDL2_ZONES/landing/arrivals
fi

if [ ! -d $UDL2_ZONES/landing/work ]; then
    mkdir -p $UDL2_ZONES/landing/work
fi

if [ ! -d $UDL2_ZONES/landing/history ]; then
    mkdir -p $UDL2_ZONES/landing/history
fi
sudo chown -R udl2.udl2 $UDL2_ROOT

%post
chkconfig --add celeryd-udl2

%postun
userdel -rf celery > /dev/null 2>&1
userdel -rf udl2 > /dev/null 2>&1

%preun
chkconfig --del celeryd-udl2

%changelog

