#!/bin/bash

export EDWARE=edware
export EDWARE_GITHUB_URI=ssh://git@github.wgenhq.net/Ed-Ware-SBAC/edware

if [ ! -d $HOME/workspace/repos/$EDWARE ]; then
    mkdir -p $HOME/workspace/repos
    cd $HOME/prjs/workspace/repos/$EDWARE
    git clone $EDWARE_GITHUB_URI
fi

if [ -d $HOME/workspace/repos/$EDWARE ]; then

    cd $HOME/workspace/repos/$EDWARE
    git pull $EDWARE_GITHUB_URI

# run the py.test --pep8
cd $HOME/workspace/repos/$EDWARE
find . -type f |grep ".py$" | xargs  py.test --pep8
# run rhino jslint

fi

