#!/usr/bin/env python
import subprocess
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import argparse


if __name__ == '__main__':
    print("initialzie udl2 database\n")
    db_host = input("please type in host name for postgres server\n")
    db_superuser = input("please type in postgres superuser name you want to connect\n")
    print("now run createuser -W -s -e -E -d udl2 -P -h %s -U %s -W \n" % (db_host, db_superuser))
    subprocess.call("createuser -W -s -e -E -d udl2 -P -h %s -U %s -W " % (db_host, db_superuser), shell=True)
    print("now create udl2 db for udl2 system")
    print("now run createdb -e -E utf-8 -O udl2 -h %s -U %s -W udl2" % (db_host, db_superuser))
    subprocess.call("createdb -e -E utf-8 -O udl2 -h %s -U %s -W udl2" % (db_host, db_superuser) , shell=True)