#!/bin/bash
. /opt/virtualenv/bin/activate
python -m filerouter.filerouter -b -g /opt/edware/home  -j /sftp/opt/edware/home
