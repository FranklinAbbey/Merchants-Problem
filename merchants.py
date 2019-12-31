"""
CSAPX Lab 3: Merchants of Venice

merchants.py reads a .txt file and creates a collection of Merchants with attributes
"name" and "location". Two sorting methods are provided to display the processing speeds
associated with determining the optimal location for a new merchant to set-up.

command line argument:
python3 merchants.py [slow|fast] input-file

Author: Sean Strout @ RIT CS
Author: Franklin Abbey
"""

import collections  # namedtuple
import math  # math
import sys  # arg
import time  # clock
import random  # random

from typing import List  # List
# using a Named Tuple to create Merchant "objects"
Merchant = collections.namedtuple("Merchant", ("name", "location"))
merchant_list = []


def read_merchants(input_file):
    """
    extracts merchant information within a .txt file and creates a
    list of Merchant named tuples
    :param input_file: the name of a .txt file
    :return: merchant_list: the information extracted from the file in the
                            form of a list of namedTuples
    """
    with open(input_file) as f:
        for line in f:
            line_list = line.split()
            merchant_list.append(Merchant(name=line_list[0], location=line_list[1]))

    return merchant_list


def partition(data: List[Merchant], pivot: int):
    """
    Three way partition the data into smaller, equal and greater lists,
    in relationship to the pivot
    :param data: The data to be sorted (a list)
    :param pivot: The value to partition the data on
    :return: Three list: smaller, equal and greater
    """
    less, equal, greater = [], [], []
    for element in data:

        if int(element.location) < pivot:
            less.append(element)
        elif int(element.location) > pivot:
            greater.append(element)
        else:
            equal.append(element)

    return less, equal, greater


def quick_sort(data: List[Merchant]):
    """
    Performs a quick sort and returns a newly sorted list
    :param data: The data to be sorted (a list)
    :return: A sorted list
    """
    if len(data) == 0:
        return []
    else:
        # here the pivot point is NOT random, and may result in inefficiency
        pivot = int(data[0].location)
        less, equal, greater = partition(data, pivot)

        return quick_sort(less) + equal + quick_sort(greater)


def quick_select_sort(data: List[Merchant], k: int):
    """
    Quickselect is a specialized version of the standard quick sort, where
    instead of sorting every item in the collection, once the position of a
    particular item is confirmed, it is returned.
    :param data: the list of Merchants
    :param k: the position within the sorted list that is most optimal
    :return: the Merchant named tuple that would be at the optimal location
    """
    # safeguard for an empty list
    if len(data) == 0:
        return []
    else:
        # a random pivot is chosen to improve efficiency
        random_index = random.randrange(0, len(data) - 1)

        pivot = int(data[random_index].location)
        less, equal, greater = partition(data, pivot)

        # the amount of items in the "less" list
        m = len(less)
        # the amount of items in the "equal" list
        count = len(equal)

        # the median value is the pivot
        if m <= k < (m + count):
            return equal[0]
        # the median value is in the 'less' list portion
        elif m > k:
            return quick_select_sort(less, k)
        # the median value is in the 'greater' list portion
        else:
            return quick_select_sort(greater, k - m - count)


def sum_of_dist(data: List[Merchant], median: int):
    """
    Using the locations of all Merchants and the ideal location,
    "sum_of_distances" calculates the average distance a merchant will
    need to travel.
    :param data: a list of Merchants
    :param median: the median value of the locations to base calculations from
    :return: sum: the sum of distances regarding the Merchants
    """
    sum = 0
    for element in data:
        # using locations for the formula
        sum += int(math.fabs(int(element.location) - median))
    return sum


def main() -> None:
    """
    The main function reads arguments, and determines whether to use
    "quick_sort" or "quick_select_sort" based on user preference.
    :return: None
    """
    merch_list = read_merchants(sys.argv[2])
    choice = sys.argv[1]

    # use quick_sort
    if choice == 'slow':
        # start timer
        start_time = time.perf_counter()
        new_list = quick_sort(merch_list)
        # find median value
        optimal = new_list[len(new_list) // 2]
        # stop timer
        elapsed_time = time.perf_counter() - start_time
        # calculate sum of distances
        total = sum_of_dist(merch_list, int(optimal.location))

    # use quickSelect_sort
    else:
        # start timer
        start_time = time.perf_counter()
        # run quick_select_sort to half sort/ find median value all at once
        optimal = quick_select_sort(merch_list, len(merch_list) // 2)
        # stop timer
        elapsed_time = time.perf_counter() - start_time
        # calculate sum of distances
        total = sum_of_dist(merch_list, int(optimal.location))

    print("\nSearch Type: " + str(choice))
    print("Number of Merchants: " + str(len(merch_list)))
    print("Elapsed Time: " + format(elapsed_time, ".10f"))
    print("Optimal Store Location: " + str(optimal))
    print("Sum of Distances: " + str(total))


if __name__ == '__main__':
    main()
