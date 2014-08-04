Name:		smarter_score_batcher%(echo ${SMARTER_ENV_NAME:=""})
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
EdWare smarter score batcher
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})

%prep
rm -rf virtualenv/smarter_score_batcher
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter_score_batcher %{buildroot}/opt/edware
cp -r ${WORKSPACE}/scripts %{buildroot}/opt/edware
mkdir -p %{buildroot}/opt/edware/conf
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/config/generate_ini.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/config/settings.yaml %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/services/config/linux/opt/edware/conf/celeryd-smarter_score_batcher.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/services/config/linux/etc/rc.d/init.d/celeryd-smarter_score_batcher %{buildroot}/etc/rc.d/init.d/

%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv/smarter
source virtualenv/smarter/bin/activate

cd %{buildroot}/opt/edware/scripts
BUILDROOT=%{buildroot}
# WORKSPACE_PATH=${BUILDROOT//\//\\\/}

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
cd ${WORKSPACE}/edworker
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/edapi
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/smarter_common
python setup.py clean --all
python setup.py install
cd -
cd %{buildroot}/opt/edware/smarter_score_batcher
python setup.py clean --all
python setup.py install
cd -

deactivate
echo -e "/opt/edware/smarter_score_batcher\n." > virtualenv/smarter/lib/python3.3/site-packages/smarter-score-batcher.egg-link
find virtualenv/smarter/bin -type f -exec sed -i 's/\/var\/lib\/jenkins\/rpmbuild\/BUILD/\/opt/g' {} \;

%install
mkdir -p %{buildroot}/opt/virtualenv
cp -r virtualenv/smarter %{buildroot}/opt/virtualenv


%clean


%files
%defattr(644,root,root,-)
/opt/edware/smarter_score_batcher/smarter_score_batcher.wsgi
/opt/edware/conf/generate_ini.py
/opt/edware/conf/settings.yaml
/opt/edware/conf/celeryd-smarter_score_batcher.conf
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
%attr(755,root,root) /opt/virtualenv/smarter/bin/pip-3.3
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
/opt/virtualenv/smarter/bin/python
/opt/virtualenv/smarter/bin/python3
%attr(755,root,root) /etc/rc.d/init.d/celeryd-smarter_score_batcher

%pre
id celery > /dev/null 2>&1
if [ $? != 0 ]; then
   useradd celery
   usermod -G fuse celery
fi
if [ ! -d /opt/edware/log ]; then
    mkdir -p /opt/edware/log
fi
if [ ! -d /var/log/celery-smarter_score_batcher ]; then
    mkdir -p /var/log/celery-smarter_score_batcher
    chown celery.celery /var/log/celery-smarter_score_batcher
fi

%post
chkconfig --add celeryd-smarter_score_batcher
chkconfig --level 2345 celeryd-smarter_score_batcher off

%preun
chkconfig --del celeryd-smarter_score_batcher

%postun


%changelog
