# Author: Kevin Sekuj
# Date: 2/22/21
# Description: Program with a decorator function that uses the time module to
# get the time elapsed for sorting lists of 1000 to 10000 random integers by
# bubble and insertion sorts. The matplotlib package's pyplot module is then
# used to generate a graph comparing the time at various list sizes for both
# functions.


import time
import random
import functools
from matplotlib import pyplot


def sort_timer(func):
    """
    Decorator function using functool's wraps() and the time module to record
    the time taken for bubble and insertion sort functions at various list sizes.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function returning the time taken for each sort method's completion.
        """

        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()

        result = end - start

        return result

    return wrapper


@sort_timer
def bubble_sort(a_list):
    """
    Bubble sort function, sorting a list in ascending order.
    """
    for pass_num in range(len(a_list) - 1):
        for index in range(len(a_list) - 1 - pass_num):
            if a_list[index] > a_list[index + 1]:
                temp = a_list[index]
                a_list[index] = a_list[index + 1]
                a_list[index + 1] = temp


@sort_timer
def insertion_sort(a_list):
    """
    Insertion sort function, sorting a list in ascending order.
    """
    for index in range(1, len(a_list)):
        value = a_list[index]
        pos = index - 1
        while pos >= 0 and a_list[pos] > value:
            a_list[pos + 1] = a_list[pos]
            pos -= 1
        a_list[pos + 1] = value


def compare_sorts(func1, func2):
    """
    Takes the two decorated sort functions as parameters, appending the time
    time elapsed at each list size (resulting from sorts_timer) to two lists. The
    results are then used to produce a comparison graph using the matplotlib's py-
    plot module.
    """

    arrays = [1000, 2000, 3000, 4000, 5000,
              6000, 7000, 8000, 9000, 10000]
    bubble_time = []
    insertion_time = []

    for array_size in arrays:
        list_1 = [random.randint(1, 10000) for _ in range(array_size)]
        list_2 = list(list_1)

        bubble_time.append(func1(list_1))
        insertion_time.append(func2(list_2))

    pyplot.plot([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                bubble_time, 'ro--', linewidth=2)

    pyplot.plot([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                insertion_time, 'go--', linewidth=2)

    pyplot.xlabel("Array sizes")
    pyplot.ylabel("Time (seconds)")
    pyplot.show()


# line to call compare_sorts() to generate the graph
compare_sorts(bubble_sort, insertion_sort)
