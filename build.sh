#!/bin/bash
# parameters $1 is build number
# This build script is for the sole purpose of assisting the build server 
# (CentOS Linux) in continuous integration and not for individual developer use.

export WORKSPACE=`pwd`
export RPM_VERSION="0.8"
export BUILD_NUMBER=$1
dist=$(python -c "import platform;print(platform.dist()[0])")
if [ "$dist" != "centos" ]; then
  echo "This script is intended to run on CentOS only"
  exit -1
fi

error() {
  local parent_lineno="$1"
  local message="$2"
  local code="${3:-1}"
  if [[ -n "$message" ]] ; then
    echo "Error on or near line ${parent_lineno}: ${message}; exiting with status ${code}"
  else
    echo "Error on or near line ${parent_lineno}; exiting with status ${code}"
  fi
  exit "${code}"
}

#build individual packages for use in unit testing
trap 'error ${LINENO}' ERR
virtualenv venv
source venv/bin/activate
for p in config edcore edschema edauth edapi edworker services edextract edmigrate smarter_common smarter_score_batcher edudl2 edsftp hpz hpz_client smarter; do 
  cd $p; 
  python setup.py clean --all; 
  python setup.py develop;
  cd ..; 
done

#turn off error trapping during unit testing because we expect some tests to 
#  fail and want the build script to continue
trap '' ERR

for p in config edcore edschema edauth edapi edworker services edextract edmigrate smarter_common smarter_score_batcher edudl2 edsftp hpz hpz_client smarter; do 
  cd $p; 
  python -m unittest discover;
  cd ..; 
done
deactivate

#turn on error trapping for rpm building
trap 'error ${LINENO}' ERR
#build RPMs
rpmbuild -bb rpm/SPEC/edsftp.spec
rpmbuild -bb rpm/SPEC/edudl2.spec
rpmbuild -bb rpm/SPEC/hpz.spec
rpmbuild -bb rpm/SPEC/smarter_score_batcher.spec
rpmbuild -bb rpm/SPEC/smarter.spec
