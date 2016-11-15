'''
Module to generate scores with percentage, cut
points, minimum score, maximum score and total number
'''
import random


def generate_overall_scores(percentages_or_counts, cut_points, min_score, max_score, total, is_percentage=True):
    '''
    Main function to generate given total number of scores in range(min_score, max_score)
    Generated scores satisfy given percentage distribution, and cut_points
    '''
    counts = []
    if is_percentage is True:
        counts = split_total_by_precentages(percentages_or_counts, total)
    else:
        counts = percentages_or_counts

    # generate random scores
    generated_random_numbers = generate_random_scores_by_percentage_between_cut_points(counts, cut_points, total)

    # calculate average, and standard deviation from generated_random_numbers
    actual_avg, actual_std = calculate_avg_std(generated_random_numbers)

    # generate normal distribution with actual avg and std
    gauss_numbers = gauss_list(actual_avg, actual_std, total)

    # merge generated_random_numbers and gauss_numbers
    gauss_and_random_lists = gauss_numbers + generated_random_numbers

    # select total number from gauss_and_random_lists
    sample_in_gauss_and_random_lists = sub_sample_list(gauss_and_random_lists, cut_points, counts, total)
    # ORIGINAL CODE FOLLOWS
    # sample_in_gauss_and_random_lists = random.sample(gauss_and_random_lists, total)

    # do adjustment for the list
    final_scores_list = adjust_list(sample_in_gauss_and_random_lists, counts, cut_points, total)

    return final_scores_list


def generate_random_scores_by_percentage_between_cut_points(count_for_level, cut_points, total):
    '''
    Generate random scores by percentages in each performance level (as defined by cut_points)

    INPUT:
    count_for_level = list of counts - one for each performance level
    cut_points = list of cut points - these help define the performance levels
    total = total number of scores to generate

    OUTPUT:

    Note:
    minimum score = cut_points[0]  (i.e. minimum score = first cut point)
    maximum score = cut_points[-1] (i.e. maximum score = last cut point)

    performance level 1 : runs from cut_points[0]   to cut_points[1]
    performance level n : runs from cut_points[n-1] to cut_points[n]

    '''
    assert len(count_for_level) == len(cut_points) - 1

    pl_count = len(count_for_level)
    last_pl = pl_count - 1
    all_scores = []

    # count_for_level = split_total_by_precentages(percentages, total)

    for i in range(pl_count):
        lo = cut_points[i]
        hi = cut_points[i + 1]
        if i != last_pl:  # do not include the higher cut point in the PL range
            hi -= 1  # unless it is the last PL

        pl_scores = generate_random_numbers(lo, hi, count_for_level[i])
        all_scores.extend(pl_scores)

    assert len(all_scores) >= total
    return all_scores


def split_total_by_precentages(percentages, total):
    '''
    Return a list of integer which add up to 'total' and are distributed in the list by 'percentages'

    If the sum of the resulting split is not equal to the required total (caused by rounding errors)
        calculate the difference, find the largest value and adjust it as necessary
    '''

    need = len(percentages)
    out_list = [0] * need

    for i in range(need):
        val = (percentages[i] * total) / 100  # calculate according to the percentage
        val = int(val)  # round the result DOWN to the nearest integer
        out_list[i] = val

    diff = total - sum(out_list)
    if diff:
        index_of_max = out_list.index(max(out_list))
        out_list[index_of_max] += diff

    return out_list


def generate_random_numbers(min_number, max_number, count):
    '''
    Generate count number of integer x, so that min_number <= x <= max_number
    '''

    if count < 1:
        return []

    assert(min_number > 0 and max_number > min_number)

    random_numbers = [random.randint(int(min_number), int(max_number)) for _i in range(int(count))]
    return random_numbers


def calculate_avg_std(generated_random_numbers):
    '''
    Given a list of numbers, calculate average, and standard deviation of it
    '''
    if(len(generated_random_numbers) < 1):
        return None, None
    else:
        actual_avg = sum(generated_random_numbers) / len(generated_random_numbers)
        temp = sum([(val - actual_avg) ** 2 for val in generated_random_numbers])
        actual_std = (temp / (len(generated_random_numbers))) ** 0.5

        return actual_avg, actual_std


def gauss_list(avg, std, num):
    """
    return list of random number with gauss distribution
    """
    result = [0] * num
    for i in range(num):
        result[i] = int(random.gauss(avg, std))
    return result


def sub_sample_list(score_list, cut_points, pl_counts, total):
    """ return a sub-sample of the 'score_list' so that there are only 'total' scores, but sample by perforamce levels
    """
    # pl_counts = split_total_by_precentages(percentages, total)
    outlist = []
    pl_count = len(cut_points) - 1
    last_pl = pl_count - 1

    for i in range(pl_count):
        lo = cut_points[i]
        hi = cut_points[i + 1]
        if i != last_pl:  # do not include the higher cut point in the PL range
            hi -= 1  # unless it is the last PL

        split_list = [x for x in score_list if lo <= x <= hi]
        sub_list = random.sample(split_list, pl_counts[i])
        outlist.extend(sub_list)

    return outlist


def adjust_list(total_list, required_numbers, cut_points, total):
    '''
    Make adjustment of input total_list
    First, split the total list into each level
    For each split list, call function add_or_delete(), return a split_adjust_list
    Return combination of all split_adjust_list
    '''
    assert len(required_numbers) == len(cut_points) - 1 and len(cut_points) >= 3

    pl_count = len(required_numbers)
    last_pl = pl_count - 1

    adjusted_list = []
    # required_numbers = split_total_by_precentages(percentages, total)

    for i in range(pl_count):
        required = required_numbers[i]
        if not required:
            continue

        lo = cut_points[i]
        hi = cut_points[i + 1]
        if i != last_pl:  # do not include the higher cut point in the PL range
            hi -= 1  # unless it is the last PL

        split_list = [x for x in total_list if lo <= x <= hi]

        if len(split_list) > 0:
            split_adjust = add_or_delete(split_list, required)
        else:
            print("WARNING: in adjust_list() : nothing in split_list : PL-lo=%d, PL-hi=%d, required=%d" % (lo, hi, required))
            split_adjust = generate_random_numbers(lo, hi, required)

        adjusted_list.extend(split_adjust)
    return adjusted_list


def add_or_delete(score_list, required_number):
    '''
    Given a list of scores, and required number of scores, delete or add new scores for the input score_list
    '''

    # need more scores
    if len(score_list) < required_number:
        need_num = int(required_number) - len(score_list)
        # if need_num is greater than score_list, double the score_list
        while need_num > len(score_list) and need_num > 0:
            score_list.extend(score_list)
            need_num = int(required_number) - len(score_list)
        # still need more numbers, but the need_num is less than length of score_list
        if need_num > 0:
            score_list.extend(random.sample(score_list, need_num))
    # score_list has more scores than required number
    else:
        if required_number > 0:
            score_list = random.sample(score_list, int(required_number))
        else:
            score_list = []

    return score_list


if __name__ == '__main__':
    # total number 10000
    TOTAL = 254565
    PERCENTAGE = [30, 34, 28, 8]
    CUT_POINTS = [1200, 1575, 1875, 2175, 2400]
    SCORE_MIN, SCORE_MAX = (CUT_POINTS[0], CUT_POINTS[-1])

    generated_scores = generate_overall_scores(PERCENTAGE, CUT_POINTS, SCORE_MIN, SCORE_MAX, TOTAL)
    assert len(generated_scores) == TOTAL
    print('generated min score', min(generated_scores), 'generated max score', max(generated_scores))
