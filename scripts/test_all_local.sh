#!/bin/bash

set -e # Exit on errors

pep8 edcore/ --ignore=E501
pep8 edschema/ --ignore=E501
pep8 edudl2/ --ignore=E501
pep8 edextract/ --ignore=E501
pep8 edapi/ --ignore=E501
pep8 edauth/ --ignore=E501
pep8 edmigrate/ --ignore=E501
pep8 edworker/ --ignore=E501
pep8 edsftp/ --ignore=E501
pep8 services/ --ignore=E501
pep8 smarter/ --ignore=E501

cd edschema
nosetests
cd ..

cd edcore
nosetests
cd ..

cd edudl2
nosetests edudl2/tests/unit_tests/*
cd ..

cd smarter
nosetests
cd ..

cd edmigrate
nosetests -vs
cd ..

cd edworker
nosetests -vs
cd ..

cd edapi
nosetests -vs
cd ..

cd edsftp
nosetests -vs
cd ..

cd edextract
nosetests -vs
cd ..

cd services
nosetests -vs
cd ..

cd edauth
nosetests -vs
cd ..
