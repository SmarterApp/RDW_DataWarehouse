Name:		smarter
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	SMARTER EdWare Reporting Web Application

Group:		WSGI Web Application
License:	Proprietary software
URL:		http://www.amplify.com
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python3
BuildRequires:	python3-libs
Requires:	xmlsec1 python3-mod_wsgi
AutoReqProv: no

%define _unpackaged_files_terminate_build 0

%description
building EdWare smarter rpm


%prep
rm -rf virtualenv
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter %{buildroot}/opt/edware
cp -r ${WORKSPACE}/scripts %{buildroot}/opt/edware
cp -r ${WORKSPACE}/assets %{buildroot}/opt/edware/assets




%build
umask 0002
export LANG=en_US.UTF-8
/opt/python3/bin/virtualenv-3.3 --distribute virtualenv
source virtualenv/bin/activate
cd ${WORKSPACE}/edschema
python setup.py install
cd -
cd ${WORKSPACE}/edauth
python setup.py install
cd -
cd ${WORKSPACE}/edapi
python setup.py install
cd -
cd %{buildroot}/opt/edware/smarter
python setup.py develop
cd -

cd %{buildroot}/opt/edware/scripts
BUILDROOT=%{buildroot}
WORKSPACE_PATH=${BUILDROOT//\//\\\/}
sed -i.bak "s/assets.directory = \/path\/assets/assets.directory = ${WORKSPACE_PATH}\/opt\/edware\/assets/g" compile_assets.ini
sed -i.bak "s/smarter.directory = \/path\/smarter/smarter.directory = ${WORKSPACE_PATH}\/opt\/edware\/smarter/g" compile_assets.ini
python compile_assets.py
cd -
deactivate
echo -e "/opt/edware/smarter\n." > virtualenv/lib/python3.3/site-packages/smarter.egg-link


%install
cp -r virtualenv %{buildroot}/opt
rm -rf %{buildroot}/opt/edware/smarter/assets
cp -r %{buildroot}/opt/edware/assets %{buildroot}/opt/edware/smarter


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/opt/edware/smarter/*
/opt/virtualenv/*

%pre
/etc/init.d/httpd stop

%post
/etc/init.d/httpd start

%preun
/etc/init.d/httpd stop

%postun
/etc/init.d/httpd start



%changelog

