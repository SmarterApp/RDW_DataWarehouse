#!/bin/bash

# list of dependencies
BREW_DEPS=(libxmlsec1 wkhtmltopdf rabbitmq)
PIP_DEPS=(nose coverage nose-cov)


# check if a user is using python virtualenv
if [ -z ${VIRTUAL_ENV:=""} ]; then
    echo "Please activate your virtualenv for python first"
    exit 1
fi

# find absolute path of this script
FILE_PATH=$(cd "$(dirname "$0")";pwd)

# find assets absolute path
ASSERTS=$(cd "${FILE_PATH}/../assets";pwd)

# find smarter absolute path
SMARTER=$(cd "${FILE_PATH}/../smarter";pwd)

# install smarter module
cd ${SMARTER}
python setup-developer.py develop

for DEP in ${BREW_DEPS[@]}
do
    brew install ${DEP} >/dev/null 2>&1
done

for DEP in ${PIP_DEPS[@]}
do
    pip install ${DEP} >/dev/null 2>&1
done


npm update

cd ${ASSERTS}
node_modules/coffee-script/bin/cake -m DEV -a ${ASSERTS} -s ${SMARTER} setup
