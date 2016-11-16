#!/bin/bash
# parameters $1 is build number

export WORKSPACE=`pwd`
export RPM_VERSION="0.8"
export BUILD_NUMBER=$1

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

#build and run unit tests
trap 'error ${LINENO}' ERR
virtualenv venv
source venv/bin/activate
for p in config edcore edschema edauth edapi edworker services edextract edmigrate smarter_common smarter_score_batcher edudl2 edsftp hpz hpz_client smarter; do 
	cd $p; 
	python setup.py clean --all; 
	python setup.py develop;
	cd ..; 
done

trap '' ERR

for p in config edcore edschema edauth edapi edworker services edextract edmigrate smarter_common smarter_score_batcher edudl2 edsftp hpz hpz_client smarter; do 
	cd $p; 
	python -m unittest discover;
	cd ..; 
done
deactivate

trap 'error ${LINENO}' ERR
#build RPMs
rpmbuild -bb rpm/SPEC/edsftp.spec
rpmbuild -bb rpm/SPEC/edudl2.spec
rpmbuild -bb rpm/SPEC/hpz.spec
rpmbuild -bb rpm/SPEC/smarter_score_batcher.spec
rpmbuild -bb rpm/SPEC/smarter.spec
