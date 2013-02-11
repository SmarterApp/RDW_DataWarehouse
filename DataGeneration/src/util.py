import random
from constants import ADD_SUFFIX
import datetime

def generate_email_address(first_name, last_name, domain):
    address = first_init + '.' + last_name
    return address + '@' + domain

def generate_address(name_list):
    address = random.randint(1, 1000)
    street = random.choice(name_list)
    full_address = address + " " + street + " " + random.choice(ADD_SUFFIX)

    return full_address

def generate_address_from_list(count, words_list):
    '''
    input: count: total number of addresses
           words_list: a word list used for generate address
    output: list of addresses
    each address is created as: a number, a random word selected from input words_list, and a suffix
    '''
    adds = []
    if(count > 0):
        no = random.sample(range(1, count * 10), count)
        road_name = []
        if(count < len(words_list)):
            road_name = random.sample(words_list, count)
        else:
            road_name.extend(words_list)
        adds = [str(no[i]) + " " + str(road_name[i % len(road_name)]) + " " + random.choice(ADD_SUFFIX) for i in range(count)]
    return adds

def generate_dob(grade):

    aprox_age = grade + 6
    current_year = int(datetime.datetime.now().year)

    birth_year = current_year - aprox_age
    birth_month = random.randint(1,12)
    birth_day = random.random(1,28)

    dob = datetime.datetime(birth_year, birth_month, birth_day)

    return dob


def generate_city():
    pass

def generate_zip():
    pass