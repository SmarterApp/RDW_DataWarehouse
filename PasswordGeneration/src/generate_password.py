'''
Module to generate user passwords
Password pattern is defined in:
https://rally1.rallydev.com/#/9135758382d/detail/userstory/10519211036
'''

import argparse
import random
import os
import datetime

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
WORD_LIST = os.path.join(__location__, '..', 'word_lists', 'linuxwords.txt')
DEFAULT_OUTPUT_FILE = os.path.join(__location__, '..', 'passwords.txt')
SPECIAL_CHARS = '^!\$%&/()=?{[]}+~#-_.:,;<>\\'
MIN_LENGTH = 8


def generate_password(number, output_file):
    '''
    Method to generate given number of passwords. Write them into output_file
    '''
    # cast to integer
    count = int(number)
    # do check number
    if count <= 0:
        print("The number should be greater than 0")
        raise ValueError

    # get list of word (linux words, need to limit to 3 <= length <= 7)
    words_list = read_words()
    if len(words_list) == 0:
        print("Empty word list, please check", WORD_LIST)
        raise ValueError

    # loop count times, passwords are generated in a list
    generated_password_list = [generate_sigle_password(words_list) for _i in range(count)]
    # write password list into file
    write_into_file(generated_password_list, output_file)


def read_words():
    '''
    Read all words in WORD_LIST, return as a list
    '''
    word_list = []
    source_file_name = WORD_LIST
    try:
        source_file = open(source_file_name, 'r')
        lines = source_file.readlines()
        for line in lines:
            word_list.append(line.strip())
        source_file.close()
    except FileNotFoundError as err:
        print("No file", err)
    return word_list


def generate_sigle_password(words_list):
    '''
    Generate one single password as the pattern defined
    '''
    # randomly pick two words in words_list
    # words start with an upper case character and the remaining characters are lower case
    first_word = random.choice(words_list).title()
    second_word = random.choice(words_list).title()
    # generate one digit
    digit = generate_one_digit()
    # generate one special character
    special_char = generate_one_special_character()
    # group as a list
    four_parts = [digit, special_char, first_word, second_word]
    # shuffle the four parts
    random.shuffle(four_parts)
    # password pattern is:
    # any order of one word, one word, one digit and one special character
    password = ''
    for component in four_parts:
        password += component
    assert(len(password) >= MIN_LENGTH)
    return password


def generate_one_digit():
    '''
    Generate one digit between 1 and 10 (1<= x <10)
    '''
    return str(random.choice(range(1, 10)))


def generate_one_special_character():
    '''
    Randomly return a special character defined in SPECIAL_CHARS
    '''
    return SPECIAL_CHARS[random.choice(range(0, len(SPECIAL_CHARS)))]


def write_into_file(generated_password, output_file):
    '''
    Write the given generated_password, which is a list into output_file
    Each item in generated_password is written as one line in output_file
    '''
    file = open(output_file, 'w')
    file.write("\n".join(generated_password))


if __name__ == '__main__':
    print("Password Generation Starts", datetime.datetime.now())
    # specify number of password to be generated, and output file
    parser = argparse.ArgumentParser(description='Generate user password.')
    parser.add_argument("-n", "--number", default="500", help="number of password to be generated")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_FILE, help="output file")
    args = parser.parse_args()
    number = args.number
    output_file = args.output
    generate_password(number, output_file)
    print("Password Generation Done ", datetime.datetime.now())
