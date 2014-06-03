Name:		edsftp%(echo ${SFTP_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	Edware's SFTP Box
Group:		SFTP
License:	Proprietary software
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Vendor: Amplify Insight Edware Team <edwaredev@wgen.net>
Url: https://github.wgenhq.net/Ed-Ware-SBAC/edware

BuildRequires:	python3
BuildRequires:	python3-libs
AutoReqProv: no

%define _unpackaged_files_terminate_build 0

%description
EdWare SFTP
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})


%prep
rm -rf virtualenv/edsftp
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/edsftp %{buildroot}/opt/edware
mkdir -p %{buildroot}/opt/edware/conf
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/edsftp/config/linux/etc/rc.d/init.d/edsftp-watcher %{buildroot}/etc/rc.d/init.d/

%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv/edsftp
source virtualenv/edsftp/bin/activate

cd ${WORKSPACE}/config
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edcore
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edauth
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edapi
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edsftp
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/smarter_common
python setup.py clean --all
python setup.py install
cd -

deactivate
find virtualenv/edsftp/bin -type f -exec sed -i 's/\/var\/lib\/jenkins\/rpmbuild\/BUILD/\/opt/g' {} \;

%install
mkdir -p %{buildroot}/opt/virtualenv
cp -r virtualenv/edsftp %{buildroot}/opt/virtualenv

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,-)
/opt/virtualenv/edsftp/include/*
/opt/virtualenv/edsftp/lib/*
/opt/virtualenv/edsftp/lib64
/opt/virtualenv/edsftp/bin/activate
/opt/virtualenv/edsftp/bin/activate.csh
/opt/virtualenv/edsftp/bin/activate.fish
/opt/virtualenv/edsftp/bin/activate_this.py
%attr(755,root,root) /opt/virtualenv/edsftp/bin/easy_install
%attr(755,root,root) /opt/virtualenv/edsftp/bin/easy_install-3.3
%attr(755,root,root) /opt/virtualenv/edsftp/bin/sftp_driver.py
%attr(755,root,root) /opt/virtualenv/edsftp/bin/pip
%attr(755,root,root) /opt/virtualenv/edsftp/bin/pip-3.3
%attr(755,root,root) /opt/virtualenv/edsftp/bin/python3.3
/opt/virtualenv/edsftp/bin/python
/opt/virtualenv/edsftp/bin/python3
%attr(755,root,root) /etc/rc.d/init.d/edsftp-watcher

%pre
EDWARE_ROOT=/opt/edware
if [ ! -d $EDWARE_ROOT/run ]; then
    mkdir -p $EDWARE_ROOT/run
fi

if [ ! -d $EDWARE_ROOT/ssh ]; then
    mkdir -p $EDWARE_ROOT/ssh
fi

if [ ! -d $EDWARE_ROOT/ssh/.ssh ]; then
    mkdir -p $EDWARE_ROOT/ssh/.ssh
fi

%post
chkconfig --add edsftp-watcher
chkconfig --level 2345 edsftp-watcher off

%preun
chkconfig --del edsftp-watcher

%postun

%changelog
