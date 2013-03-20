'''
Created on Mar 20, 2013

@author: dip
'''
import json


def get_overall_asmt_interval(result):
    '''
    Given a dictionary, return overall assessment interval
    Logic is to interval is the difference of score and min score range
    '''
    return result['asmt_score'] - result['asmt_score_range_min']


def rearrange_cut_points(result):
    '''
    Given a dictionary, return a formatted results for assessment cutpoints and colors
    '''

    result['cut_point_intervals'] = []

    custom_metadata = result['asmt_custom_metadata']
    custom = None if not custom_metadata else json.loads(custom_metadata)
    # once we use the data, we clean it from the result
    del(result['asmt_custom_metadata'])

    # go over the 4 cut points
    for i in range(1, 5):
        # we only take cutpoints with values > 0
        cut_point_interval = result['asmt_cut_point_{0}'.format(i)]
        # if it's the forth interval, we would have a value anyway.
        if i == 4 or (cut_point_interval and cut_point_interval > 0):
            cut_point_interval_object = {'name': str(result['asmt_cut_point_name_{0}'.format(i)]),
                                         'interval': str(cut_point_interval)}

            # the value of the 4th interval is the assessment max score
            if (i == 4):
                cut_point_interval_object['interval'] = str(result['asmt_score_max'])
            # once we use the data, we clean it from the result
            del(result['asmt_cut_point_name_{0}'.format(i)])
            del(result['asmt_cut_point_{0}'.format(i)])
            # connect the custom metadata content to the cut_point_interval object
            if custom is not None:
                result['cut_point_intervals'].append(dict(list(cut_point_interval_object.items()) + list(custom[i - 1].items())))
            else:
                result['cut_point_intervals'].append(cut_point_interval_object)

    # remove unnecessary cut point name
    if 'asmt_cut_point_name_5' in result:
        del(result['asmt_cut_point_name_5'])
    return result
