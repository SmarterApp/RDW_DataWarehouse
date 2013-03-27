import subprocess
import os
import configparser
import shutil
import argparse


def main(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    assets_dir = config.get('default', 'assets.directory')
    smarter_dir = config.get('default', 'smarter.directory')
    run_npm = config.get('default', 'run.npm.update').lower()

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

    # Run cake watch - builds and watches
    if os.access(less_dir, os.W_OK):
        try:
            current_dir = os.getcwd()
            os.chdir(assets_dir)
            if run_npm == 'true':
                # Run npm update
                command_opts = ['npm', 'update']
                rtn_code = subprocess.call(command_opts)
                if rtn_code != 0:
                    logger.warning('npm install command failed')
            # Run cake
            command_opts = ['cake', 'build']
            p = subprocess.call(command_opts)
        finally:
            # Change the directory back to original
            os.chdir(current_dir)

    # Copy the entire assets into smarter, delete the dir first if it already exists
    target_dir = os.path.join(smarter_dir, 'assets')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree(assets_dir, target_dir)


if __name__ == '__main__':
    this_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(this_file)
    
    parser = argparse.ArgumentParser(description='Compile Assets and Copy Asssets into Smarter')
    parser.add_argument('--config', default=os.path.join(current_dir, 'compile_assets.ini'), help='Set the path to configuration ini file (defaults to compile_assets.ini')
    args = parser.parse_args()

    main(args.config)
