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

Name:		hpz%(echo ${HPZ_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	HTTP Pickup Zone

Group:		WSGI Web Application
License: Amplify Education, Inc and ASL 2.0
URL:		http://www.amplify.com
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python3
BuildRequires:	python3-libs
Requires:	xmlsec1 python3-mod_wsgi xmlsec1-openssl xmlsec1-openssl-devel postgresql92-devel python3-libs
AutoReqProv: no

# force python3 to be passed to brp-python-bytecompile
BuildRequires: python3-devel
%global __python %{__python3}

%define _unpackaged_files_terminate_build 0

%description
HPZ hpz
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})


%prep
rm -rf virtualenv/hpz
rm -rf %{buildroot}

# Instead of building from ${WORKSPACE}/hpz this tricks python setup to include the assets folder in the egg
# (not quite sure why that's a good idea but leaving it in)
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/hpz %{buildroot}/opt/edware
touch %{buildroot}/opt/edware/hpz/assets/__init__.py

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

%install
mkdir -p %{buildroot}/opt/virtualenv
cp -r virtualenv/hpz %{buildroot}/opt/virtualenv
find %{buildroot}/opt/virtualenv/hpz/bin -type f -exec sed -i -r 's/(\/[^\/]*)*\/rpmbuild\/BUILD/\/opt/g' {} \;

mkdir -p %{buildroot}/opt/edware/hpz/scripts
cp ${WORKSPACE}/hpz/*.wsgi %{buildroot}/opt/edware/hpz/
cp ${WORKSPACE}/hpz/scripts/* %{buildroot}/opt/edware/hpz/scripts/
mkdir -p %{buildroot}/opt/edware/conf
cp ${WORKSPACE}/config/generate_ini.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/hpz/settings.yaml %{buildroot}/opt/edware/conf/

%clean

%files
%defattr(644,root,root,755)
/opt/edware/hpz/frs.wsgi
/opt/edware/hpz/swi.wsgi
/opt/edware/hpz/scripts/pickup_zone_cleanup.py
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
%attr(755,root,root) /opt/virtualenv/hpz/bin/pip3
%attr(755,root,root) /opt/virtualenv/hpz/bin/prequest
%attr(755,root,root) /opt/virtualenv/hpz/bin/proutes
%attr(755,root,root) /opt/virtualenv/hpz/bin/pserve
%attr(755,root,root) /opt/virtualenv/hpz/bin/pshell
%attr(755,root,root) /opt/virtualenv/hpz/bin/ptweens
%attr(755,root,root) /opt/virtualenv/hpz/bin/pviews
%attr(755,root,root) /opt/virtualenv/hpz/bin/pygmentize
%attr(755,root,root) /opt/virtualenv/hpz/bin/python3.3
%attr(755,root,root) /opt/virtualenv/hpz/bin/python
%attr(755,root,root) /opt/virtualenv/hpz/bin/python3


%pre
if [ ! -d /opt/edware/log ]; then
    mkdir -p /opt/edware/log
fi

%post

%preun

%postun


%changelog

