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


def flatten_yaml(a_dict, result, path=""):
    '''
    This method runs recursively and traversing the dictionary to flatten it and load the result into the result object.
    '''
    for key in a_dict:
        if type(a_dict[key]) != dict:
            value = "" if a_dict[key] is None else str(a_dict[key])
            result[path + key] = value
        else:
            # if it's a root, find (or add) a root dict and flatten its sub-tree under it
            group_dict = result.get(key, {})
            if key.startswith('[') and key.endswith(']'):
                # run recursively, but don't add this level to the path, as it is the root (group) level.
                result[key] = flatten_yaml(a_dict[key], group_dict, path)
            else:
                # run recursively adding the current level to the path.
                result = flatten_yaml(a_dict[key], result, path + key + ".")
    return result


def generate_ini(env, input_file='settings.yaml', output_file=None, project_name=None):
    '''
    This tool is a standalone tool that convert a yaml file into its equivalent ini file.
    '''
    try:
        with open(input_file, 'r') as f:
            settings = f.read()
    except:
        raise IOError(str.format("could not find or open file {0} for read", input_file))

    # check for host class
    hostclass = None
    if '.' in env:
        hostclass = env
        env = env.split('.')[0]

    # use PyYaml to load the file's content
    settings = yaml.load(settings)

    # if the environment is in the yaml file, we use it. otherwise, we just use the common part.
    env_settings = False
    if env in settings:
        env_settings = settings[env]
    else:
        print(str.format("could not find environment {0} in the yaml file", env))

    if 'common' not in settings:
        raise ValueError("could not find the common section in the yaml file")

    # check for host class config
    hc_settings = False
    if hostclass is not None and hostclass in settings:
        hc_settings = settings[hostclass]
    elif hostclass is not None:
        print(str.format("could not find host class environment {0} in the yaml file", hostclass))

    common_settings = settings['common']

    # first we load the common section into the yaml_object
    yaml_object = flatten_yaml(common_settings, {}, "")
    # if we have environment specific data, we use it to add/override to the common section
    if env_settings:
        yaml_object = flatten_yaml(env_settings, yaml_object, "")
    # if we have host class specific data, we use it to add/override to the environment section
    if hc_settings:
        yaml_object = flatten_yaml(hc_settings, yaml_object, "")

    # update project name in yaml settings
    if project_name is not None:
        yaml_object['[app:main]']['use'] = 'egg:' + project_name

    result = ""
    # we read each group and write it to the result string with its content.
    # output in alphabetic order
    for group in sorted(yaml_object.keys()):
        result = result + group + "\n"
        group_settings = yaml_object[group]
        # we add all settings with their values.
        result = result + ''.join([setting + " = " + group_settings[setting] + "\n" for setting in sorted(group_settings.keys())])

    if not output_file:
        # we presume that the result file has the environment name.
        output_file = env + ".ini"
    try:
        # we overwrite the entire file's content
        with open(output_file, 'w') as f:
            f.write(result)
        # we print the result (consider removing this one)
        print(result)
    except:
        raise IOError(str.format('could not open file {0} for write', output_file))

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a YAML file into an INI file.')
    parser.add_argument("-e", "--env", default='development', help="set environment name.")
    parser.add_argument("-i", "--input", default="settings.yaml", help="set input yaml file name default[settings.yaml]")
    parser.add_argument("-o", "--output", help="set output ini file name. Default is development.ini")
    parser.add_argument("-p", "--project", default="smarter", choices=['smarter', 'smarter_score_batcher'], help="the project name. Default is smarter.")
    args = parser.parse_args()

    if args.env is None:
        print("Please specifiy --env option")
        exit(-1)
    try:
        generate_ini(args.env, args.input, args.output, args.project)
    except Exception as ipe:
        print(ipe)
