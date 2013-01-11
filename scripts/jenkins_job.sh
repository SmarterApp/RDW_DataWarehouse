#!/bin/bash

export PROJ=edware
export EDWARE_GITHUB_URI=ssh://git@github.wgenhq.net/Ed-Ware-SBAC/edware

if [ ! -d $HOME/prjs/$PROJ ]; then
    mkdir -p $HOME/prjs/
    cd $HOME/prjs
    git clone $EDWARE_GITHUB_URI
fi

if [ -d $HOME/prjs/$PROJ ]; then

    cd $HOME/prjs/$PROJ
    git pull $EDWARE_GITHUB_URI

# run the py.test --pep8

# run rhino jslint

fi

