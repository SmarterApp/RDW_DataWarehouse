'''
Created on Apr 4, 2013

@author: swimberly
'''

import re
import argparse


def verify_password_file(filename):
    '''
    Method that loops through a file of passwords and checks each one for correctness
    @param filename: the name of the password file
    '''

    all_clear = True

    with open(filename, 'r') as f:
        for line in f.readlines():
            if not check_password(line):
                all_clear = False
    return all_clear


def check_password(password):
    '''
    check a single password against rules defined by the story
    @param password: the password string to check
    @raise AssertionError: Newline count too large (this would be very strange)
    '''

    # Remove newline chars from password
    passwd = password.splitlines()
    assert len(passwd) == 1
    passwd = passwd[0]
    empty_str = passwd

    regex = r'\d{1}|\W{1}|[_]{1}|([A-Z]{1}[a-z]*)'
    special_chars = re.findall(r'\W{1}|[_]{1}', passwd)
    digit_chars = re.findall(r'\d{1}', passwd)
    words = re.findall(r'[A-Z]{1}[a-z]*', passwd)
    white_space = re.findall(r'\s', passwd)

    try:
        assert len(special_chars) == 1
        empty_str = empty_str.replace(special_chars[0], '', 1)
        assert len(digit_chars) == 1
        empty_str = empty_str.replace(digit_chars[0], '', 1)
        assert len(words) == 2
        assert not white_space

        for word in words:
            assert len(word) >= 4 and len(word) <= 8
            empty_str = empty_str.replace(word, '', 1)

        assert re.match(regex, password)

        # Check that no other characters appear in the string
        assert empty_str == ''

    except AssertionError:
        print("Invalid password: %s" % password)
        return False

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Functional Test for Password Generator')
    parser.add_argument('filename', help='The name of the password file to check')
    args = parser.parse_args()
    if verify_password_file(args.filename):
        print("All passwords are valid")
