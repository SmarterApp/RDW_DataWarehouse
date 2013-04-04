import unittest
import generate_password
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
FILES_FOR_TEST_PATH = os.path.join(__location__, 'files_for_test')


class TestGeneratePassword(unittest.TestCase):

    def test_generate_password_invalid_number(self):
        self.assertRaises(ValueError, generate_password.generate_password, -1, '/output')

    def test_generate_password_invalid_words_list_file(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'non_existing_file.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 100, '/output')

    def test_generate_password_empty_words_list(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'empty_word_list.txt')
        self.assertRaises(ValueError, generate_password.generate_password, 200, '/output')

    def test_generate_password_three(self):
        generate_password.WORD_LIST = os.path.join(FILES_FOR_TEST_PATH, 'word_list_10.txt')
        number = '3'
        output_file = os.path.join(FILES_FOR_TEST_PATH, 'output_1.txt')
        generate_password.generate_password(number, output_file)
        # check
        expected_file = open(output_file, 'r')
        lines = expected_file.readlines()
        self.assertEqual(len(lines), int(number))
        for line in lines:
            self.assertTrue(len(line) >= 8)
        expected_file.close()
        os.remove(output_file)

    def test_generate_sigle_password_long_list(self):
        words_list = ['oneword', 'zfgadfs', 'qdfafggt', 'lqpzxc', 'addfl', 'polqsf']
        actual_password = generate_password.generate_sigle_password(words_list)
        # TODO: ASSERT, can do it in regular expression

    def test_generate_sigle_password_one_word_list(self):
        words_list = ['oneword']
        actual_password = generate_password.generate_sigle_password(words_list)
        self.assertEqual(len(actual_password), len(words_list[0]) * 2 + 2)

    def test_generate_one_special_character(self):
        special_char = generate_password.generate_one_special_character()
        self.assertTrue(special_char in generate_password.SPECIAL_CHARS)
