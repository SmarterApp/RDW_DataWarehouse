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
EdWare smarter 
commit: ${GIT_COMMIT:="UNKNOWN"}


%prep
rm -rf virtualenv
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter %{buildroot}/opt/edware
cp -r ${WORKSPACE}/scripts %{buildroot}/opt/edware
cp -r ${WORKSPACE}/assets %{buildroot}/opt/edware/assets
touch %{buildroot}/opt/edware/assets/__init__.py




%build
export LANG=en_US.UTF-8
/opt/python3/bin/virtualenv-3.3 --distribute virtualenv
source virtualenv/bin/activate

cd %{buildroot}/opt/edware/scripts
BUILDROOT=%{buildroot}
WORKSPACE_PATH=${BUILDROOT//\//\\\/}
sed -i.bak "s/assets.directory = \/path\/assets/assets.directory = ${WORKSPACE_PATH}\/opt\/edware\/assets/g" compile_assets.ini
sed -i.bak "s/smarter.directory = \/path\/smarter/smarter.directory = ${WORKSPACE_PATH}\/opt\/edware\/smarter/g" compile_assets.ini

python compile_assets.py
cd -

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
rm -rf assets
mv ../assets .
python setup.py install
cd -

deactivate
#/opt/python3/bin/virtualenv-3.3 --relocatable virtualenv
echo -e "/opt/edware/smarter\n." > virtualenv/lib/python3.3/site-packages/smarter.egg-link
sed -i 's/\/home\/jenkins\/rpmbuild\/BUILD/\/opt/g' virtualenv/bin/activate
sed -i 's/\/home\/jenkins\/rpmbuild\/BUILD/\/opt/g' virtualenv/bin/pip
sed -i 's/\/home\/jenkins\/rpmbuild\/BUILD/\/opt/g' virtualenv/bin/pserve
sed -i 's/\/home\/jenkins\/rpmbuild\/BUILD/\/opt/g' virtualenv/bin/pcreate


%install
cp -r virtualenv %{buildroot}/opt
#rm -rf %{buildroot}/opt/edware/smarter/assets
#cp -r %{buildroot}/opt/edware/assets %{buildroot}/opt/edware/smarter


%clean


%files
%defattr(644,root,root,-)
#/opt/edware/smarter/*
/opt/virtualenv/include/*
/opt/virtualenv/lib/*
/opt/virtualenv/lib64
/opt/virtualenv/bin/activate
/opt/virtualenv/bin/activate.csh
/opt/virtualenv/bin/activate.fish
/opt/virtualenv/bin/activate_this.py
%attr(755,root,root) /opt/virtualenv/bin/bfg2pyramid
%attr(755,root,root) /opt/virtualenv/bin/easy_install
%attr(755,root,root) /opt/virtualenv/bin/easy_install-3.3
%attr(755,root,root) /opt/virtualenv/bin/initialize_smarter_db
%attr(755,root,root) /opt/virtualenv/bin/mako-render
%attr(755,root,root) /opt/virtualenv/bin/pcreate
%attr(755,root,root) /opt/virtualenv/bin/pip
%attr(755,root,root) /opt/virtualenv/bin/pip-3.3
%attr(755,root,root) /opt/virtualenv/bin/prequest
%attr(755,root,root) /opt/virtualenv/bin/proutes
%attr(755,root,root) /opt/virtualenv/bin/pserve
%attr(755,root,root) /opt/virtualenv/bin/pshell
%attr(755,root,root) /opt/virtualenv/bin/ptweens
%attr(755,root,root) /opt/virtualenv/bin/pviews
%attr(755,root,root) /opt/virtualenv/bin/pygmentize
%attr(755,root,root) /opt/virtualenv/bin/python3.3
/opt/virtualenv/bin/python
/opt/virtualenv/bin/python3


%pre
/etc/init.d/httpd stop
if [ ! -d /opt/edware/conf ]; then
    mkdir -p /opt/edware/conf
fi

%post
/etc/init.d/httpd start

%preun
/etc/init.d/httpd stop

%postun
/etc/init.d/httpd start



%changelog

