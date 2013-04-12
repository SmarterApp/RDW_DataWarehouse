'''
Module to generate user passwords
Password pattern is defined in:
https://rally1.rallydev.com/#/9135758382d/detail/userstory/10519211036
'''

import argparse
import random
import os
import datetime
import math

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
WORD_LIST = os.path.join(__location__, '..', 'word_lists', 'linuxwords.txt')
DEFAULT_OUTPUT_FILE = os.path.join(__location__, '..', 'passwords.txt')
SPECIAL_CHARS = '^!\$%&/=?+~#-\\_:;<>'
MIN_LENGTH = 10


def generate_password(number, output_file):
    '''
    Method to generate given number of passwords. Write them into output_file
    '''
    # cast to integer
    count = int(number)

    # the number should be greater than 0
    if count <= 0:
        print("The number should be greater than 0")
        raise ValueError

    # get list of word
    words_list = read_words()
    # the words list should not be empty
    if len(words_list) == 0:
        print("Empty word list, please check", WORD_LIST)
        raise ValueError

    # the input number should be less than half length of the words_list
    half_number_of_words = math.ceil(len(words_list) / 2)
    if count >= half_number_of_words:
        print("The input number", number, "is too big, it should be less than half number of words in", WORD_LIST)
        raise ValueError

    # get two word lists from words_list
    # words in first_word_list are unique words selected from the first half of word_list
    # words in second_word_list are unique words selected from the second half of word_list
    first_word_list = random.sample(words_list[0: half_number_of_words], count)
    second_word_list = random.sample(words_list[half_number_of_words:-1], count)

    # generate single password count  number of times
    # make words selected from first_word_list and second_word_list
    # start with an upper case character and lower case for remaining characters
    generated_password = [generate_single_password(first_word_list[i], second_word_list[i]) for i in range(count)]

    # write into output file
    write_into_file(generated_password, output_file)


def read_words():
    '''
    Read all words in WORD_LIST, return as a list
    '''
    word_list = []
    file_name = WORD_LIST
    try:
        target_file = open(file_name, 'r')
        lines = target_file.readlines()
        for line in lines:
            word_list.append(line.strip())
        target_file.close()
    except FileNotFoundError as err:
        print("No file", err)
    return word_list


def generate_single_password(first_word, second_word):
    '''
    Generate one single password as the pattern defined
    '''
    # generate one digit
    digit = generate_one_digit()
    # generate one special character
    special_char = generate_one_special_character()
    # group as a list
    four_parts = [digit, special_char, first_word.title(), second_word.title()]
    # shuffle the four parts
    random.shuffle(four_parts)
    # password pattern is:
    # any order of one word, one word, one digit and one special character
    password = ''
    for component in four_parts:
        password += component
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
    file.close()


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    # input arguments: number of password to be generated, and output file
    parser = argparse.ArgumentParser(description='Generate user passwords.')
    parser.add_argument("-n", "--number", default="500", help="number of password to be generated")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_FILE, help="output file")
    args = parser.parse_args()
    number = args.number
    output_file = args.output
    generate_password(number, output_file)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print(number, "password(s) are generated in", spend_time)
