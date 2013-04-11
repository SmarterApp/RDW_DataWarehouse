'''
Reads a yaml file and generate an ini file according to an environment parameter.
@author:     aoren

@copyright:  2013 Wireless Generation. All rights reserved.

@contact:    edwaredevs@wgen.net
@deffield    updated: Updated
'''
import argparse
import yaml

__all__ = []
__version__ = 0.1
__date__ = '2013-02-02'
__updated__ = '2013-02-02'

DBDRIVER = "postgresql+pypostgresql"
DEBUG = 0
VERBOSE = False


def flatten_yaml(aDict, result, path=""):
    for k in aDict:
        if type(aDict[k]) != dict:
            result = result + path + k + " = " + str(aDict[k]) + "\n"
        else:
            if k.startswith('[') and k.endswith(']'):
                result = result + k + "\n"
                result = flatten_yaml(aDict[k], result, path)
            else:
                result = flatten_yaml(aDict[k], result, path + k + ".")

    return result


def generate_ini(env, output_file):
    with open('settings.yaml', 'r') as f:
        settings = f.read()

    settings = yaml.load(settings)

    env_settings = settings[env]
    common_settings = settings['common']

    result = flatten_yaml(env_settings, "", "")
    result = flatten_yaml(common_settings, result, "")

    try:
        with open(output_file, 'w') as f:
            f.write(result)
        print(result)
    except:
        print(str.format('could not open file {0} for write', output_file))

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create New Schema for EdWare')
    parser.add_argument("-e", "--env", default='dev', help="set environment name.")
    parser.add_argument("-o", "--output", default="development.ini", help="set output file name default[development.ini]")
    args = parser.parse_args()

#    if __env is None:
#        print("Please specifiy --env option")
#        exit(-1)
    generate_ini(args.env, args.output)
