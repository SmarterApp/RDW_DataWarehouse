Name:		hpz%(echo ${HPZ_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	HTTP Pickup Zone

Group:		WSGI Web Application
License:	Proprietary software
URL:		http://www.amplify.com
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python3
BuildRequires:	python3-libs
Requires:	xmlsec1 python3-mod_wsgi xmlsec1-openssl xmlsec1-openssl-devel fuse-encfs
AutoReqProv: no

%define _unpackaged_files_terminate_build 0

%description
HPZ hpz
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})


%prep
rm -rf virtualenv/hpz
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/hpz %{buildroot}/opt/edware
mkdir -p %{buildroot}/opt/edware/conf
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/config/generate_ini.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/hpz/settings.yaml %{buildroot}/opt/edware/conf/

%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv/hpz
source virtualenv/hpz/bin/activate


cd ${WORKSPACE}/config
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edcore
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edschema
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edauth
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/smarter_common
python setup.py clean --all
python setup.py install
cd -
cd %{buildroot}/opt/edware/hpz
python setup.py clean --all
python setup.py install
cd -

deactivate
echo -e "/opt/edware/hpz\n." > virtualenv/hpz/lib/python3.3/site-packages/hpz.egg-link
find virtualenv/hpz/bin -type f -exec sed -i 's/\/var\/lib\/jenkins\/rpmbuild\/BUILD/\/opt/g' {} \;

%install
mkdir -p %{buildroot}/opt/virtualenv
cp -r virtualenv/hpz %{buildroot}/opt/virtualenv


%clean


%files
%defattr(644,root,root,-)
/opt/edware/hpz/frs.wsgi
/opt/edware/hpz/swi.wsgi
/opt/edware/conf/generate_ini.py
/opt/edware/conf/settings.yaml
/opt/virtualenv/hpz/include/*
/opt/virtualenv/hpz/lib/*
/opt/virtualenv/hpz/lib64
/opt/virtualenv/hpz/bin/activate
/opt/virtualenv/hpz/bin/activate.csh
/opt/virtualenv/hpz/bin/activate.fish
/opt/virtualenv/hpz/bin/activate_this.py
%attr(755,root,root) /opt/virtualenv/hpz/bin/bfg2pyramid
%attr(755,root,root) /opt/virtualenv/hpz/bin/easy_install
%attr(755,root,root) /opt/virtualenv/hpz/bin/easy_install-3.3
%attr(755,root,root) /opt/virtualenv/hpz/bin/mako-render
%attr(755,root,root) /opt/virtualenv/hpz/bin/pcreate
%attr(755,root,root) /opt/virtualenv/hpz/bin/pip
%attr(755,root,root) /opt/virtualenv/hpz/bin/pip-3.3
%attr(755,root,root) /opt/virtualenv/hpz/bin/prequest
%attr(755,root,root) /opt/virtualenv/hpz/bin/proutes
%attr(755,root,root) /opt/virtualenv/hpz/bin/pserve
%attr(755,root,root) /opt/virtualenv/hpz/bin/pshell
%attr(755,root,root) /opt/virtualenv/hpz/bin/ptweens
%attr(755,root,root) /opt/virtualenv/hpz/bin/pviews
%attr(755,root,root) /opt/virtualenv/hpz/bin/pygmentize
%attr(755,root,root) /opt/virtualenv/hpz/bin/python3.3
/opt/virtualenv/hpz/bin/python
/opt/virtualenv/hpz/bin/python3


%pre
if [ ! -d /opt/edware/log ]; then
    mkdir -p /opt/edware/log
fi
if [ ! -d /opt/edware/hpz/uploads ]; then
    mkdir -p /opt/edware/hpz/uploads
    chown -R apache.apache /opt/edware/hpz/uploads
fi

%post

%preun

%postun


%changelog

