import math
import random

def extract_value_from_normal_distribution(avg, min, max):
    pass

def generate_name_from_lists(list_1, list_2, max_name_length=None):
    return None

def generate_names_from_lists(count, list1, list2, name_length=None):
    '''
    Generate total 'count' number of random combination of names from input lists
    '''

    # TODO: Add comments to this function. Difficult to follow.
    names = []
    if(count > 0):
        base = math.ceil(math.sqrt(count))
        if(base < len(list1) and base < len(list2)):
            names1 = random.sample(list1, base)
            names2 = random.sample(list2, base)
        elif(base < len(list1) * len(list2)):
            if(len(list1) < len(list2)):
                names1 = list1
                names2 = random.sample(list2, math.ceil(count / len(list1)))
            else:
                names2 = list2
                names1 = random.sample(list1, math.ceil(count / len(list2)))
        else:
            print("not enough...", base, " ", len(list1), " ", len(list2))
            raise ValueError

        if(name_length is not None):
            names = [(str(name1) + " " + str(name2))[0: name_length] for name1 in names1 for name2 in names2]
        else:
            names = [str(name1) + " " + str(name2) for name1 in names1 for name2 in names2]

    new_list = []
    new_list.extend(names[0:count])
    return new_list
