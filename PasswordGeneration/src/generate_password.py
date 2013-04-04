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

    # get two word lists from words_list
    first_word_list, second_word_list = get_two_words_lists(words_list, count)
    first_list_len = len(first_word_list)
    second_list_len = len(second_word_list)
    # open the output file
    generated_password = []
    for i in range(count):
        # get two actual words from list
        first_word = first_word_list[i % first_list_len].title()
        second_word = second_word_list[i % second_list_len].title()
        # generate one single password
        password = generate_sigle_password(first_word, second_word)
        generated_password.append(password)
    # write into file
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


def get_two_words_lists(words_list, count):
    '''
    Return two words lists.
    Each one has the given count of words from words_list
    '''
    first_list = []
    second_list = []
    total_number_of_words = len(words_list)
    half_number_of_words = total_number_of_words // 2
    # if count is smaller than half length of the words_list
    # select count number of words from the first half of words_list as first_list
    # select count number of words from the second half of words_list as second_list
    if(count < half_number_of_words):
        first_list = random.sample(words_list[0: half_number_of_words], count)
        second_list = random.sample(words_list[half_number_of_words:-1], count)
    # else if count is smaller than total length of words_list
    # randomly select count number of words for both first_list, and second_list
    elif count < total_number_of_words:
        first_list = random.sample(words_list, count)
        second_list = random.sample(words_list, count)
    # if count is greater than the length of words_list, raise exception.
    # We need more words in words_list
    else:
        first_list = words_list
        second_list = words_list
    return first_list, second_list


def generate_sigle_password(first_word, second_word):
    '''
    Generate one single password as the pattern defined
    '''
    # generate one digit
    digit = generate_one_digit()
    # generate one special character
    special_char = generate_one_special_character()

    four_parts = [digit, special_char, first_word, second_word]
    # shuffle the three characters
    random.shuffle(four_parts)
    # password pattern is:
    # one character, one word, one character, one word, one character
    # three characters are in four_parts which are shuffled already
    password = ''
    for component in four_parts:
        password += component
    assert(len(password) >= 8)
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
