from __future__ import absolute_import
__author__ = 'abrien'
from simple_file_validator.csv_validator import CsvValidator

def main():
    validator = CsvValidator()

    dir_path = '.'
    file_name = 'test_csv.csv'
    batch_sid = 1

    error_codes = validator.execute(dir_path, file_name, batch_sid)

    for error_code in error_codes:
        print(error_code)



if __name__ == "__main__":
    main()
