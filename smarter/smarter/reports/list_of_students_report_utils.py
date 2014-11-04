'''
Created on Oct 21, 2014

@author: tosako
'''


def get_group_filters(results):
    # TODO: use list comprehension, format grouping information for filters
    all_groups = set()
    for result in results:
        for i in range(1, 11):
            if result['group_{i}_id'.format(i=i)]:
                all_groups.add((result['group_{i}_id'.format(i=i)], result['group_{i}_text'.format(i=i)]))

    options = [{"value": k, "label": v} for k, v in all_groups]
    filters = sorted(options, key=lambda k: k['label'])
    return filters


def __reverse_map(map_object):
    '''
    reverse map for FE
    '''
    return {v: k for k, v in map_object.items()}
