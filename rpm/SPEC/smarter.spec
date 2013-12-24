Name:		smarter%(echo ${SMARTER_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	SMARTER EdWare Reporting Web Application

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
EdWare smarter 
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})


%prep
rm -rf virtualenv
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter %{buildroot}/opt/edware
cp -r ${WORKSPACE}/scripts %{buildroot}/opt/edware
cp -r ${WORKSPACE}/assets %{buildroot}/opt/edware/assets
touch %{buildroot}/opt/edware/assets/__init__.py
mkdir -p %{buildroot}/opt/edware/conf
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/config/generate_ini.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/config/settings.yaml %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/config/comparing_populations_precache_filters.json %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/services/config/linux/opt/edware/conf/celeryd-services.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/services/config/linux/etc/rc.d/init.d/celeryd-services %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/edextract/config/linux/opt/edware/conf/celeryd-edextract.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/edextract/config/linux/etc/rc.d/init.d/celeryd-edextract %{buildroot}/etc/rc.d/init.d/


%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv
source virtualenv/bin/activate

cd %{buildroot}/opt/edware/scripts
BUILDROOT=%{buildroot}
WORKSPACE_PATH=${BUILDROOT//\//\\\/}
sed -i.bak "s/assets.directory = \/path\/assets/assets.directory = ${WORKSPACE_PATH}\/opt\/edware\/assets/g" compile_assets.ini
sed -i.bak "s/smarter.directory = \/path\/smarter/smarter.directory = ${WORKSPACE_PATH}\/opt\/edware\/smarter/g" compile_assets.ini

python compile_assets.py
cd -

cd ${WORKSPACE}/config
python setup.py install
cd -
cd ${WORKSPACE}/edcore
python setup.py install
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
cd ${WORKSPACE}/edworker
python setup.py install
cd -
cd ${WORKSPACE}/services
python setup.py install
cd -
cd ${WORKSPACE}/edextract
python setup.py install
cd -
cd %{buildroot}/opt/edware/smarter
rm -rf assets
mv ../assets .
python setup.py install
cd -

deactivate
echo -e "/opt/edware/smarter\n." > virtualenv/lib/python3.3/site-packages/smarter.egg-link
find virtualenv/bin -type f -exec sed -i 's/\/var\/lib\/jenkins\/rpmbuild\/BUILD/\/opt/g' {} \;

%install
cp -r virtualenv %{buildroot}/opt


%clean


%files
%defattr(644,root,root,-)
/opt/edware/smarter/smarter.wsgi
/opt/edware/conf/generate_ini.py
/opt/edware/conf/settings.yaml
/opt/edware/conf/comparing_populations_precache_filters.json
/opt/edware/conf/celeryd-services.conf
/opt/edware/conf/celeryd-edextract.conf
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
%attr(755,root,root) /opt/virtualenv/bin/celery
%attr(755,root,root) /opt/virtualenv/bin/celery
%attr(755,root,root) /opt/virtualenv/bin/celerybeat
%attr(755,root,root) /opt/virtualenv/bin/celeryctl
%attr(755,root,root) /opt/virtualenv/bin/celeryd
%attr(755,root,root) /opt/virtualenv/bin/celeryd-multi
%attr(755,root,root) /opt/virtualenv/bin/celeryev
/opt/virtualenv/bin/python
/opt/virtualenv/bin/python3
%attr(755,root,root) /etc/rc.d/init.d/celeryd-services
%attr(755,root,root) /etc/rc.d/init.d/celeryd-edextract


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


%post
chkconfig --add celeryd-services
chkconfig --add celeryd-edextract



%preun
chkconfig --del celeryd-services
chkconfig --del celeryd-edextract


%postun
userdel -rf celery > /dev/null 2>&1


%changelog

