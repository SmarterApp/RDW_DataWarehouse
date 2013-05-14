#!/usr/bin/env python
import subprocess
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import sys


if __name__ == '__main__':
    cleaned_argv = [ arg for arg in sys.argv[1:] if arg != '']
    subprocess.call("python -m udl2.database %s " % " ".join(cleaned_argv), shell=True)
