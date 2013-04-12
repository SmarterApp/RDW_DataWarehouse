'''
Reads a yaml file and generate an ini file according to an environment parameter.
@author:     aoren

@copyright:  2013 Wireless Generation. All rights reserved.

@contact:    edwaredevs@wgen.net
@deffield    updated: Updated
'''
import argparse
import yaml
from smarter.reports.exceptions.parameter_exception import InvalidParameterException

__all__ = []
__version__ = 0.1
__date__ = '2013-02-02'
__updated__ = '2013-02-02'

DBDRIVER = "postgresql+pypostgresql"
DEBUG = 0
VERBOSE = False


def flatten_yaml(a_dict, result, path=""):
    '''
    This method runs recursively and traversing the dictionary to flatten it and load the result into the result object.
    '''
    for k in a_dict:
        if type(a_dict[k]) != dict:
            value = "" if a_dict[k] is None else str(a_dict[k])
            result[path + k] = value
        else:
            # if it's a root, find (or add) a root dict and flatten its sub-tree under it
            group_dict = result.get(k, {})
            if k.startswith('[') and k.endswith(']'):
                # run recursively, but don't add this level to the path, as it is the root (group) level.
                result[k] = flatten_yaml(a_dict[k], group_dict, path)
            else:
                # run recursively adding the current level to the path.
                result = flatten_yaml(a_dict[k], result, path + k + ".")
    return result


def generate_ini(env, input_file='settings.yaml'):
    '''
    This tool is a standalone tool that convert a yaml file into its equivalent ini file.
    '''
    try:
        with open(input_file, 'r') as f:
            settings = f.read()
    except:
        raise InvalidParameterException(str.format("could not find or open file {0} for read", input_file))

    # use PyYaml to load the file's content
    settings = yaml.load(settings)

    # if the environment is in the yaml file, we use it. otherwise, we just use the common part.
    if env in settings:
        env_settings = settings[env]
    common_settings = settings['common']

    # first we load the common section into the yaml_object
    yaml_object = flatten_yaml(common_settings, {}, "")
    # if we have environment specific data, we use it to add/override to the common section
    if env_settings:
        yaml_object = flatten_yaml(env_settings, yaml_object, "")

    result = ""
    # we read each group and write it to the result string with its content.
    for group in yaml_object:
        result = result + group + "\n"
        group_settings = yaml_object[group]
        # we add all settings with their values.
        result = result + ''.join([setting + " = " + group_settings[setting] + "\n" for setting in group_settings])

    # we presume that the result file has the environment name.
    output_file = env + ".ini"
    try:
        # we overwrite the entire file's content
        with open(output_file, 'w') as f:
            f.write(result)
        # we pring the result (consider removing this one)
        print(result)
    except:
        raise IOError(str.format('could not open file {0} for write', output_file))

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a YAML file into an INI file.')
    parser.add_argument("-e", "--env", default='development', help="set environment name.")
    parser.add_argument("-i", "--input", default="settings.yaml", help="set input yaml file name default[settings.yaml]")
    args = parser.parse_args()

    if args.env is None:
        print("Please specifiy --env option")
        exit(-1)
    try:
        generate_ini(args.env, args.input)
    except Exception as ipe:
        print(ipe)
