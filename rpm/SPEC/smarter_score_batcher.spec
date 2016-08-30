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

Name:		smarter_score_batcher%(echo ${SMARTER_ENV_NAME:=""})
Version:	%(echo ${RPM_VERSION:="X.X"})
Release:	%(echo ${BUILD_NUMBER:="X"})%{?dist}
Summary:	SMARTER EdWare Reporting Web Application

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
# disable the default cleanup of build root
%define __spec_install_pre %{___build_pre}

%description
EdWare smarter score batcher
commit: %(echo ${GIT_COMMIT:="UNKNOWN"})

%prep
rm -rf virtualenv/smarter_score_batcher
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter_score_batcher %{buildroot}/opt/edware
cp -r ${WORKSPACE}/smarter_score_batcher/resources %{buildroot}/opt/edware
cp -r ${WORKSPACE}/scripts %{buildroot}/opt/edware
mkdir -p %{buildroot}/opt/edware/conf
mkdir -p %{buildroot}/etc/rc.d/init.d
cp ${WORKSPACE}/config/generate_ini.py %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/config/settings.yaml %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/smarter_score_batcher/config/linux/opt/edware/conf/celeryd-smarter_score_batcher.conf %{buildroot}/opt/edware/conf/
cp ${WORKSPACE}/smarter_score_batcher/config/linux/etc/rc.d/init.d/celeryd-smarter_score_batcher %{buildroot}/etc/rc.d/init.d/
cp ${WORKSPACE}/smarter_score_batcher/config/linux/etc/rc.d/init.d/file-monitor-smarter_score_batcher %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/opt/edware/item_level
mkdir -p %{buildroot}/opt/edware/raw_data
mkdir -p %{buildroot}/opt/edware/tsb

%build
export LANG=en_US.UTF-8
virtualenv-3.3 --distribute virtualenv/smarter_score_batcher
source virtualenv/smarter_score_batcher/bin/activate

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
cd ${WORKSPACE}/edschema
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
cd ${WORKSPACE}/edworker
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/smarter_common
python setup.py clean --all
python setup.py install
cd -
cd ${WORKSPACE}/smarter_score_batcher
python setup.py clean --all
python setup.py install
cd -

deactivate

%install
mkdir -p %{buildroot}/opt/virtualenv
cp -r virtualenv/smarter_score_batcher %{buildroot}/opt/virtualenv
find %{buildroot}/opt/virtualenv/smarter_score_batcher/bin -type f -exec sed -i -r 's/(\/[^\/]*)*\/rpmbuild\/BUILD/\/opt/g' {} \;


%clean


%files
%defattr(644,root,root,755)
/opt/edware/smarter_score_batcher/smarter_score_batcher.wsgi
/opt/edware/resources/*
/opt/edware/conf/generate_ini.py
/opt/edware/conf/settings.yaml
/opt/edware/conf/celeryd-smarter_score_batcher.conf
/opt/virtualenv/smarter_score_batcher/include/*
/opt/virtualenv/smarter_score_batcher/lib/*
/opt/virtualenv/smarter_score_batcher/lib64
/opt/virtualenv/smarter_score_batcher/bin/activate
/opt/virtualenv/smarter_score_batcher/bin/activate.csh
/opt/virtualenv/smarter_score_batcher/bin/activate.fish
/opt/virtualenv/smarter_score_batcher/bin/activate_this.py
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/bfg2pyramid
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/easy_install
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/easy_install-3.3
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/mako-render
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pcreate
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pip
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pip3
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/prequest
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/proutes
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pserve
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pshell
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/ptweens
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pviews
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/pygmentize
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/python3.3
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celery
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celery
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celerybeat
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celeryctl
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celeryd
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celeryd-multi
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/celeryev
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/python
%attr(755,root,root) /opt/virtualenv/smarter_score_batcher/bin/python3
%attr(755,root,root) /etc/rc.d/init.d/celeryd-smarter_score_batcher
%attr(755,root,root) /etc/rc.d/init.d/file-monitor-smarter_score_batcher

%dir
%attr(755, celery, celery) /opt/edware/item_level
%attr(755, celery, celery) /opt/edware/raw_data
%attr(755, celery, celery) /opt/edware/tsb


%pre
id celery > /dev/null 2>&1
if [ $? != 0 ]; then
   useradd celery
   egrep -i "^fuse:" /etc/group > /dev/null 2>&1
   RET=$?
   if [ ${RET} == 0 ]; then
      usermod -G fuse celery
   fi
fi
if [ ! -d /opt/edware/log ]; then
    mkdir -p /opt/edware/log
fi
if [ ! -d /var/log/celery-smarter_score_batcher ]; then
    mkdir -p /var/log/celery-smarter_score_batcher
    chown celery.celery /var/log/celery-smarter_score_batcher
fi
# if [ ! -d /opt/edware/resources ]; then
#     mkdir -p /opt/edware/resources
# fi
# chown -R celery.celery /opt/edware/resources

%post
chkconfig --add celeryd-smarter_score_batcher
chkconfig --level 2345 celeryd-smarter_score_batcher off
chkconfig --add file-monitor-smarter_score_batcher
chkconfig --level 2345 file-monitor-smarter_score_batcher off

%preun
chkconfig --del celeryd-smarter_score_batcher
chkconfig --del file-monitor-smarter_score_batcher

%postun


%changelog
