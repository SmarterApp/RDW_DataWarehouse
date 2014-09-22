'''
Created on Sep 22, 2014

@author: agrebneva
'''


def deep_merge(dict1, dict2):
    '''
    deep merge of nested dicts
    '''
    dict_merge = dict1.copy()
    dict1_keys = dict1.keys()
    for k, v in dict2.items():
        if k in dict1_keys:
            if isinstance(dict1[k], dict) and isinstance(v, dict):
                dict_merge[k] = deep_merge(dict1[k], v)
            elif isinstance(v, dict) != isinstance(dict1[k], dict):
                raise Exception("Dictionaries are not mergable")
            else:
                dict_merge[k] = v
        else:
            dict_merge[k] = v
    return dict_merge
