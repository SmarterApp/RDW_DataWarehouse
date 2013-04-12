'''
Module to generate scores with percentage, cut
points, minimum score, maximum score and total number
'''
import random


def generate_overall_scores(percentage, cut_points, min_score, max_score, total):
    '''
    Main function to generate given total number of scores in range(min_score, max_score)
    Generated scores satisfy given percentage distribution, and cut_points
    '''
    # generate random scores
    generated_random_numbers = generate_random_scores(percentage, cut_points, total)

    # calculate average, and standard deviation from generated_random_numbers
    actual_avg, actual_std = calculate_avg_std(generated_random_numbers)

    # generate normal distribution with actual avg and std
    gauss_numbers = gauss_list(actual_avg, actual_std, total)

    # merge generated_random_numbers and gauss_numbers
    gauss_and_random_lists = gauss_numbers + generated_random_numbers

    # select total number from gauss_and_random_lists
    sample_in_gauss_and_random_lists = random.sample(gauss_and_random_lists, total)

    # do adjustment for the list
    final_scores_list = adjust_list(sample_in_gauss_and_random_lists, percentage, cut_points, total)

    return final_scores_list
#    return {
#            'gauss_numbers': [min_score, max_score, 20, gauss_numbers, 'gauss_numbers'],
#            'generated_random_numbers': [min_score, max_score, 20, generated_random_numbers, 'generated_random_numbers'],
#            'sample_in_gauss_and_random_lists': [min_score, max_score, 20, sample_in_gauss_and_random_lists, 'sample_in_gauss_and_random_lists'],
#            'adjust_lists_from_sample_list': [min_score, max_score, 20, final_scores_list, 'adjust_lists_from_sample_list']
#            }


def generate_random_scores(percentage, cut_points, total):
    '''
    Generate random scores by input mode parameter
    if triangle_mode is true, for level 1 and level 4, generate scores by triangular method
    Otherwise, generate scores in each level randomly
    '''
    assert len(percentage) == len(cut_points) - 1
    random_numbers_level = []
    # calculate the absolute count for each performance level
    count_for_level = calculate_absolute_values(percentage, total)
    for i in range(len(percentage)):
        # for the last performance level, the max number should be included
        if i == len(percentage) - 1:
            high_bound = cut_points[i + 1]
        else:
            high_bound = cut_points[i + 1] - 1
        # add generated random numbers into list. each generated number should be: cut_points[i] <= number <= high_bound
        random_numbers_level.extend(generate_random_numbers(cut_points[i], high_bound, count_for_level[i]))
    assert len(random_numbers_level) == total
    return random_numbers_level


def calculate_absolute_values(percentage, total):
    '''
    Calculate absolute numbers.
    For example, percentage = [14,42, 34, 10], total = 2371
    First three numbers are calculated as int(percentage[i] * total / 100)
    The last number is calculated as total - sum(first three numbers)
    '''
    count_for_level = []
    for i in range(len(percentage) - 1):
        count_for_level.append(int(percentage[i] * total / 100))
    count_for_level.append(total - sum(count_for_level))
    return count_for_level


def generate_random_numbers(min_number, max_number, count):
    '''
    Generate count number of integer x, so that min_number <=x<= max_number
    '''
    if min_number < max_number and count > 0:
        random_numbers = [random.randint(int(min_number), int(max_number)) for _i in range(int(count))]
        # print("randomly generated result", len(random_numbers), min(random_numbers), max(random_numbers))
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
        # print('actual_avg', actual_avg)
        # print('actual_std', actual_std)
        return actual_avg, actual_std


def gauss_list(avg, std, num):
    """
    return list of random number with gauss distribution
    """
    result = [0] * num
    for i in range(num):
        result[i] = int(random.gauss(avg, std))
    return result


def adjust_list(total_list, percentage, cut_points, total):
    '''
    Make adjustment of input total_list
    First, split the total list into each level
    For each split list, call function add_or_delete(), return a split_adjust_list
    Return combination of all split_adjust_list
    '''
    assert len(percentage) == len(cut_points) - 1 and len(cut_points) >= 3
    adjusted_list = []
    required_numbers = calculate_absolute_values(percentage, total)
    for i in range(len(cut_points) - 1):
        # for last level, the cut_points[i + 1] should be included
        if i == len(cut_points) - 2:
            high_bound = cut_points[i + 1]
        else:
            high_bound = cut_points[i + 1] - 1
        # print('split list range', cut_points[i], high_bound)
        split_list = [x for x in total_list if cut_points[i] <= x <= high_bound]
        split_adjust = add_or_delete(split_list, required_numbers[i])
        adjusted_list.extend(split_adjust)
    return adjusted_list


def add_or_delete(score_list, required_number):
    '''
    Given a list of scores, and required number of scores, delete or add new scores for the input score_list
    '''
    # print('doing adjustment...')
    # print('already have:', len(score_list), 'target number:', required_number, 'need more, or less ', (int(required_number) - len(score_list)))

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

    # print('finish add and delete, required', required_number, 'adjust to', len(score_list))
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
