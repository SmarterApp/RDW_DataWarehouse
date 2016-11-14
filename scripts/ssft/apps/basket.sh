#!/usr/bin/env bash

__dependencies(){
    packages=(
            config
            data_gen
            edapi
            edauth
            edcore
            edextract
            edmigrate
            edschema
            edsftp
            edudl2
            edworker
            hpz
            hpz_client
            services
            smarter
            smarter_common
            smarter_score_batcher
    )
    setup_virtualenv
    echo "Setting up unit tests dependencies"

    pip_3_3 install --upgrade nose
    pip_3_3 install --upgrade coverage
    pip_3_3 install --upgrade pep8
    pip_3_3 install --upgrade nose-cov
    pip_3_3 install --upgrade nose-htmloutput
    pip_3_3 install --upgrade nose-allure-plugin

    echo "Finished setting up unit tests dependencies"
}

__db(){
    echo "No DB"
}

__ini(){
    echo "No ini"
}