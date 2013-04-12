'''
Module to generate scores with percentage, cut 
points, min score, max score and total number
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
    for i in range(len(percentage)):
        random_numbers_level.extend(generate_random_numbers(cut_points[i], cut_points[i + 1], total * percentage[i] / 100))
    return random_numbers_level


def generate_random_numbers(min_number, max_number, count):
    '''
    Generate count number of integer, in the range of input min_number and max_number
    '''
    if min_number < max_number and count > 0:
        return [random.randint(int(min_number), int(max_number)) for _i in range(int(count))]


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
        print('actual_avg', actual_avg)
        print('actual_std', actual_std)
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
    assert len(percentage) == len(cut_points) - 1
    adjusted_list = []
    for i in range(len(cut_points) - 1):
        split_list = [x for x in total_list if cut_points[i] < x < cut_points[i + 1]]
        split_adjust = add_or_delete(split_list, total * percentage[i] / 100)
        adjusted_list.extend(split_adjust)
    return adjusted_list


def add_or_delete(score_list, required_number):
    '''
    Given a list of scores, and required number of scores, delete or add new scores for the input score_list
    '''
    print('doing adjustment...')
    print('already have:', len(score_list), 'target number:', required_number, 'need more, or less ', (int(required_number) - len(score_list)))

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
        score_list = random.sample(score_list, int(required_number))

    return score_list
    

if __name__ == '__main__':
    # total number 10000
    TOTAL = 10000
    PERCENTAGE = [30, 34, 28, 8]
    CUT_POINTS = [1200, 1575, 1875, 2175, 2400]
    SCORE_MIN, SCORE_MAX = (CUT_POINTS[0], CUT_POINTS[-1])

    generated_scores = generate_overall_scores(PERCENTAGE, CUT_POINTS, SCORE_MIN, SCORE_MAX, TOTAL)
    assert len(generated_scores) == TOTAL
    print('generated min score', min(generated_scores), 'generated max score', max(generated_scores))
