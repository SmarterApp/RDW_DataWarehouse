import itertools

def all_combinations(elements, include_empty=True):
    """
    generate all combinations of the elements

    :param elements: a collection with a length
    :param include_empty: if False, don't include the empty set
    :return: a generator of all combinations
    """
    if include_empty:
        yield ()

    for r in range(1, len(elements) + 1):
        yield from itertools.combinations(elements, r)


