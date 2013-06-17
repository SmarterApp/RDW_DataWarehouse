#!/bin/sh

if [ "`uname`" == "Darwin" ]; then
    sudo killall -9 python3.3 || sudo killall -9 python3
else 
    sudo killall -9 celery;
fi
