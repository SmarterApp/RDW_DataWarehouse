#!/bin/sh

if [ "`uname`" == "Darwin" ]; then
    killall -9 python3.3 || sudo killall -9 python3
else 
    killall -9 celery;
fi
exit 0
