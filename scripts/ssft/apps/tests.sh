#!/usr/bin/env bash

__dependencies(){
    packages=( tests )
    setup_virtualenv
}

__db(){
    echo "No DB"
}

__ini(){
    echo "No ini"
}