import unittest
import generate_password
import os
import re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
FILES_FOR_TEST_PATH = os.path.join(__location__, 'files_for_test')


class TestGeneratePassword(unittest.TestCase):

    def test_generate_password_negative_number(self):
        self.assertRaises(ValueError, generate_password.generate_password, -10, '/output')

    def test_generate_password_greater_than_half_of_words_list(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'word_list_10.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 8, '/output')

    def test_generate_password_invalid_words_list_file(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'non_existing_file.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 100, '/output')

    def test_generate_password_empty_words_list(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'empty_word_list.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 200, '/output')

    def test_generate_password_one_word_in_words_list(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'one_word_list.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 200, '/output')
        
    def test_generate_password_three_passwords(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'word_list_10.txt')
        number = '3'
        output_file = os.path.join(FILES_FOR_TEST_PATH, 'output_3.txt')
        generate_password.generate_password(number, output_file)
        # verify
        expected_file = open(output_file, 'r')
        lines = expected_file.readlines()
        self.assertEqual(len(lines), int(number))
        for line in lines:
            self.assertTrue(len(line) >= generate_password.MIN_LENGTH)
        expected_file.close()
        os.remove(output_file)

    def test_generate_sigle_password_long_list(self):
        first_word = 'abcd'
        second_word = 'deffgz'
        actual_password = generate_password.generate_single_password(first_word, second_word)
        # verify that the actual password contains only one digit, one special character
        actual_special_chars = re.findall(r'\W{1}|[_]{1}', actual_password)
        self.assertTrue(len(actual_special_chars), 1)
        self.assertTrue(actual_special_chars[0] in generate_password.SPECIAL_CHARS)
        one_digit_expression = '[1-9]{1}'
        actual_digit = re.findall(one_digit_expression, actual_password)
        self.assertTrue(len(actual_digit), 1)
        # verify that two words are either first_word, or second_word
        actual_password_copy = actual_password
        rest_password = actual_password_copy.replace(str(actual_special_chars[0]), '').replace(str(actual_digit[0]), '')
        self.assertTrue(rest_password in [first_word.title() + second_word.title(), second_word.title() + first_word.title()])
        self.assertEqual(len(actual_password), len(first_word) + len(second_word) + 2)

    def test_generate_one_special_character(self):
        special_char = generate_password.generate_one_special_character()
        self.assertTrue(special_char in generate_password.SPECIAL_CHARS)
