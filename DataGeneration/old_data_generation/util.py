import random
from constants import ADD_SUFFIX
import datetime


def generate_email_address(first_name, last_name, domain):
    domain = '@' + domain.replace(' ', '') + '.edu'
    address = first_name + '.' + last_name
    return (address + domain).lower()


def generate_address(word_list):
    address = str(random.randint(1, 1000))
    street = random.choice(word_list)
    full_address = (address + " " + street + " " + random.choice(ADD_SUFFIX)).title()
    return full_address


def generate_dob(grade):

    aprox_age = grade + 6
    current_year = int(datetime.datetime.now().year)

    birth_year = current_year - aprox_age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)

    dob = datetime.date(birth_year, birth_month, birth_day).strftime("%Y%m%d")

    return dob


def generate_start_date(grade):
    today = datetime.datetime.now()
    current_year = int(today.year)
    current_month = int(today.month)

    start_year = current_year - grade
    if(grade == 0 and current_month <= 9):
        start_year = current_year - 1
    # generate the first day of school
    start_month = 9
    start_day = random.randint(1, 8)

    # Need to return a string (not a date object), but using the library to ensure formatint (YYYYMMDD)
    return datetime.date(start_year, start_month, start_day).strftime('%Y%m%d')
