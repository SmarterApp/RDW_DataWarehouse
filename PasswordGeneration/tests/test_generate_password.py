import unittest
import generate_password
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
FILES_FOR_TEST_PATH = os.path.join(__location__, 'files_for_test')


class TestGeneratePassword(unittest.TestCase):

    def test_generate_password_negtive_number(self):
        self.assertRaises(ValueError, generate_password.generate_password, -10, '/output')

    def test_generate_password_greater_than_max_number(self):
        self.assertRaises(ValueError, generate_password.generate_password, generate_password.MAX_NUMBER_OF_PASSWORD + 10, '/output')

    def test_generate_password_invalid_words_list_file(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'non_existing_file.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 100, '/output')

    def test_generate_password_empty_words_list(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'empty_word_list.txt')
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
        words_list = ['oneword', 'zfgadfs', 'qdfafggt', 'lqpzxc', 'addfl', 'polqsf']
        actual_password = generate_password.generate_sigle_password(words_list)

        # verify that the actual password contains only one digit, one special character
        actual_digit_index = -1
        actual_special_char_index = -1
        for i in range(len(actual_password)):
            if actual_password[i].isdigit() and actual_digit_index == -1:
                actual_digit_index = i
            elif actual_password[i] in generate_password.SPECIAL_CHARS and actual_special_char_index == -1:
                actual_special_char_index = i
        self.assertTrue(-1 < actual_digit_index < len(actual_password))
        self.assertTrue(-1 < actual_special_char_index < len(actual_password))
        # verify that two words are selected from words_list(not necessary to be different)
        actual_password_copy = actual_password
        rest_password = actual_password_copy.replace(str(actual_password[actual_digit_index]), '').replace(str(actual_password[actual_special_char_index]), '')
        self.assertTrue(rest_password in [word.title() + wor.title() for word in words_list for wor in words_list])

    def test_generate_sigle_password_one_word_list(self):
        words_list = ['oneword']
        actual_password = generate_password.generate_sigle_password(words_list)
        self.assertEqual(len(actual_password), len(words_list[0]) * 2 + 2)

    def test_generate_one_special_character(self):
        special_char = generate_password.generate_one_special_character()
        self.assertTrue(special_char in generate_password.SPECIAL_CHARS)
