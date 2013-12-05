Name:		udl2%(echo ${SMARTER_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	Edware's Universal Data Loader
Group:		ETL pipeline
License:	Proprietary software
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Vendor: Amplify Insight Edware Team <edwaredev@wgen.net>
Url: https://github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0/

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

%install
cp -r virtualenv %{buildroot}/opt


%clean

%files
%defattr(644,root,root,-)
/opt/edware/conf/celeryd-udl2.conf
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
   usermod -G fuse celery
fi
if [ ! -d /opt/edware/log ]; then
    mkdir -p /opt/edware/log
fi

%post
chkconfig --add celeryd

%preun
chkconfig --del celeryd

%postun
userdel -rf celery > /dev/null 2>&1

%changelog

