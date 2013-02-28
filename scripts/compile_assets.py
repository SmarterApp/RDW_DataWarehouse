import subprocess
import os
import configparser
import shutil
import sys


def main():
    this_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(this_file)

    config = configparser.ConfigParser()
    config.read(os.path.join(current_dir, 'compile_assets.ini'))
    assets_dir = config.get('default', 'assets.directory')
    smarter_dir = config.get('default', 'smarter.directory')

    css_dir = os.path.join(assets_dir, "css")
    less_dir = os.path.join(assets_dir, "less")

    # We're assuming we only have one less file to compile
    less_file = os.path.join(less_dir, 'style.less')
    css_file = os.path.join(css_dir, 'style.css')

    # delete all css file before lessc generates css files from less files
    css_filelist = [f for f in os.listdir(css_dir) if f.endswith('.css')]
    for f in css_filelist:
        target_file = os.path.join(css_dir, f)
        if os.access(target_file, os.W_OK):
            os.unlink(target_file)

    # Run lessc to compile less files
    if os.access(less_dir, os.W_OK):
        command_opts = ['lessc', '-x', less_file, css_file]
        rtn_code = subprocess.call(command_opts)
        if rtn_code != 0:
            print('Error happened in lessc call')

    # Copy the entire assets into smarter, delete the dir first if it already exists
    target_dir = os.path.join(smarter_dir, 'assets')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree(assets_dir, target_dir)


if __name__ == '__main__':
    sys.exit(main())
