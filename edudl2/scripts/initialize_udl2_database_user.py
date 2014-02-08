#!/usr/bin/env python
import subprocess
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import sys


if __name__ == '__main__':
    print("initialzie udl2 database\n")
    db_host = input("please type in host name for postgres server\n")
    db_superuser = input("please type in postgres superuser name you want to connect\n")
    print("now run createuser -W -s -e -E -d udl2 -P -h %s -U %s -W \n" % (db_host, db_superuser))
    subprocess.call("createuser -W -s -e -E -d udl2 -P -h %s -U %s -W " % (db_host, db_superuser), shell=True)

    print("now create udl2 db for udl2 system")
    print("now run createdb -e -E utf-8 -O udl2 -h {db_host} -U {db_superuser} -W udl2".format(db_host=db_host,
                                                                                               db_superuser=db_superuser))

    subprocess.call("createdb -e -E utf-8 -O udl2 -h {db_host} -U {db_superuser} -W udl2".format(db_host=db_host,
                                                                                                 db_superuser=db_superuser),
                    shell=True)

    print("now create edware data warehousing database on local for testing if needed")
    create_star_schema = input("create edware star schema (Y/n)")
    if create_star_schema.upper()[0:1] == 'Y':
        print("initialize local edware database\n")
        db_host = input("please type in host name for postgres server\n")
        db_superuser = input("please type in postgres superuser name you want to connect\n")
        print("now run createuser -W -s -e -E -d edware -P -h {db_host} -U {db_superuser} -W \n".format(db_host=db_host,
                                                                                                        db_superuser=db_superuser))
        subprocess.call("createuser -W -s -e -E -d edware -P -h {db_host} -U {db_superuser} -W ".format(db_host=db_host,
                                                                                                        db_superuser=db_superuser), shell=True)
        print("now create edware db for udl2 system")
        print("now run createdb -e -E utf-8 -O edware -h {db_host} -U {db_superuser} -W edware".format(db_host=db_host,
                                                                                                       db_superuser=db_superuser))
        subprocess.call("createdb -e -E utf-8 -O edware -h {db_host} -U {db_superuser} -W edware".format(db_host=db_host,
                                                                                                         db_superuser=db_superuser), shell=True)
