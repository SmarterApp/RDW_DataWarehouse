'''
Created on Aug 25, 2014

@author: tosako
'''
import os
import io

IGNORE_ROOT_DIRS = ['scripts', 'resource', 'spike', 'sys', 'data_gen', 'pdfmaker', 'poc']
IGNORE_DIRS = ['node_modules', '3p', 'build', 'js', 'docs']
IGNORE_EXT = ['.gpg', '.pyc', '.gz', '.png', 'md', '.txt', '.out', '.eml', '.csv', '.jar', '.egg', '.gpz', '.asc', '.ico', '.json', 'gif', '.done', '.in']
IGNORE_FILES = ['random_seed', 'id_rsa', 'id_rsa.pub']


def add_license_style1(file, license, comment='#', offset_line=0):
    l = io.StringIO(license)
    lines = []
    with open(file, 'r+', encoding='utf8') as f:
        for idx in range(offset_line):
            lines.append(f.readline())
        content = f.read()
        f.seek(0, 0)
        for line in lines:
            f.write(line)
        for line in l:
            f.write(comment + ' ' + line)
        f.write(os.linesep)
        f.write(content)


def add_license_style2(file, license, start_comment='###', end_comment='###', offset_line=0):
    lines = []
    with open(file, 'r+', encoding='utf8') as f:
        for idx in range(offset_line):
            lines.append(f.readline())
        content = f.read()
        f.seek(0, 0)
        for line in lines:
            f.write(line)
        f.write(start_comment + os.linesep)
        f.write(license)
        f.write(os.linesep)
        f.write(end_comment + os.linesep)
        f.write(os.linesep)
        f.write(content)


def add_license_to_python(file, license):
    add_license_style1(file, license)


def add_license_to_ldif(file, license):
    add_license_style1(file, license)


def add_license_to_sql(file, license):
    add_license_style1(file, license, comment='--')


def add_license_to_coffee(file, license):
    add_license_style2(file, license)


def add_license_to_xml(file, license):
    offset = 0
    with open(file, 'r', encoding='utf8') as f:
        data = f.read(5)
        if data == '<?xml':
            offset = 1
    add_license_style2(file, license, start_comment='<!--', end_comment='-->', offset_line=offset)


def add_license_to_html(file, license):
    offset = 0
    with open(file, 'r', encoding='utf8') as f:
        data = f.readline()
        if data.lower().startswith('<!DOCTYPE html>'.lower()):
            offset = 1
        elif data.lower().startswith('<html'.lower()):
            offset = 1
    add_license_style2(file, license, start_comment='<!--', end_comment='-->', offset_line=offset)


def add_license_to_js(file, license):
    add_license_style2(file, license, start_comment='/*', end_comment='*/')


def add_license_to_less(file, license):
    add_license_style2(file, license, start_comment='/*', end_comment='*/')


def add_license_to_css(file, license):
    add_license_style2(file, license, start_comment='/*', end_comment='*/')


def add_license_to_yaml(file, license):
    add_license_style1(file, license)


def add_license_to_spec(file, license):
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        l = io.StringIO(content)
        for line in l:
            if line.startswith('License:'):
                f.write('License: Apache License, Version 2.0' + os.linesep)
            else:
                f.write(line)
    add_license_style1(file, license)


def add_license_to_shell(file, license):
    offset = 0
    with open(file, 'r') as f:
        data = f.read(2)
        if data == '#!':
            offset = 1
    add_license_style1(file, license, offset_line=offset)


def add_license(file, license, license_func=None):
    basename = os.path.basename(file)
    if '.' in basename:
        ext = basename.split('.')[-1]
        func = EXT_LICENSE.get('.' + ext, license_func)
        if func is not None:
            try:
                func(file, license)
            except:
                print('error: ' + file)
                raise
        else:
            print('no license: ' + file)
    else:
        func = LICENSE.get(basename, license_func)
        if func is not None:
            func(file, license)
        else:
            print('no license: ' + file)


def find_files_for_license(top, license, license_func=None):
    if not os.path.islink(top):
        for l in os.listdir(top):
            if not l.startswith('.'):
                path = os.path.join(top, l)
                if os.path.isdir(path):
                    func = LICENSE_DIR.get(l)
                    if func is not None:
                        find_files_for_license(path, license, license_func=func)
                    elif not l in IGNORE_DIRS and not l.endswith('.egg-info') and not l.startswith('__') and not l.startswith('selenium-'):
                        find_files_for_license(path, license, license_func=license_func)
                elif os.path.isfile(path):
                    if not l.endswith(tuple(IGNORE_EXT)) and l not in IGNORE_FILES:
                        add_license(path, license, license_func=license_func)


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    parent = os.path.abspath(os.path.join(here, '..'))
    license_file = os.path.join(here, 'apache_v2.txt')
    with open(license_file) as f:
        license = f.read()
    for d in [os.path.join(parent, d) for d in os.listdir(parent) if os.path.isdir(os.path.join(parent, d)) and not d.startswith(".") and d not in IGNORE_ROOT_DIRS]:
        find_files_for_license(d, license)


EXT_LICENSE = {'.py': add_license_to_python,
               '.coffee': add_license_to_coffee,
               '.sh': add_license_to_shell,
               '.ldif': add_license_to_ldif,
               '.sql': add_license_to_sql,
               '.xml': add_license_to_xml,
               '.xsd': add_license_to_xml,
               '.html': add_license_to_html,
               '.js': add_license_to_js,
               '.wsgi': add_license_style1,
               '.ini': add_license_style1,
               '.cfg': add_license_style1,
               '.conf': add_license_style1,
               '.spec': add_license_to_spec,
               '.less': add_license_to_less,
               '.css': add_license_to_css,
               '.yaml': add_license_to_yaml,
               '.pt': add_license_to_html}
LICENSE = {'Cakefile': add_license_style1,
           'wsgi_swi_template': add_license_style1,
           'wsgi_frs_template': add_license_style1}
LICENSE_DIR = {'init.d': add_license_to_shell}

if __name__ == '__main__':
    main()
