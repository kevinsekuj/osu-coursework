# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment:  1 // Python Fundamentals Review
# Description: Python fundamentals consisting of 14 assignments using the StaticArray
# class and its basic methods. Does not use any other data structures or data
# structure methods.

import random
import string
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------


def min_max(arr: StaticArray) -> ():
    """
    Sets the initial max/min to the first element of the array. Iterates through
    the array checking each element and updating its maximum/minimum when necessary.
    When the length of the array is traversed, it returns a tuple of min and max.
    """
    max_num = arr[0]
    min_num = max_num
    for index in range(arr.size()):
        if arr[index] > max_num:
            max_num = arr[index]
        elif arr[index] < min_num:
            min_num = arr[index]

    return min_num, max_num


# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------


def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Creates a new static array object set to the size of the array passed as a param.
    Iterates through the array checking whether each value is divisible by 3 and 5, or
    3 or 5, filling in the new array accordingly, and finally returns the new array.
    """
    new_arr = StaticArray(arr.size())
    for index in range(arr.size()):
        if arr[index] % 3 == 0 and arr[index] % 5 == 0:
            new_arr[index] = 'fizzbuzz'
        elif arr[index] % 3 == 0:
            new_arr[index] = 'fizz'
        elif arr[index] % 5 == 0:
            new_arr[index] = 'buzz'
        else:
            new_arr[index] = arr[index]
    return new_arr


# ------------------- PROBLEM 3 - REVERSE -----------------------------------


def reverse(arr: StaticArray) -> None:
    """
    Reversing an array by moving inwards from the first and last array elements.
    Start is set to the 0th index of the array whereas end is set to the last index,
    and temp variables hold the element at each index. On each iteration of the while
    loop, the array indices are swapped until start = end at which point all elements
    have been swapped.
    """
    start = 0
    end = arr.size() - 1
    while start < end:
        temp_start = arr[start]
        temp_end = arr[end]

        arr[start] = temp_end
        arr[end] = temp_start

        start += 1
        end -= 1


# ------------------- PROBLEM 4 - ROTATE ------------------------------------


def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Rotating an array will be a matter of adding or subtracting to the index of
    the old array. Indices at the end of an array for rotating right for example
    have to be shifted to the start of the array. This can be done using the
    modulo operator. A similar method is done with left-rotations, but the steps
    must first be subtracted from the length of the array to avoid moving out of range.
    """
    new_arr = StaticArray(arr.size())
    for index in range(arr.size()):
        if steps > 0:
            shifted = (index + steps) % arr.size()
            new_arr[shifted] = arr[index]
        elif steps < 0:
            shifted = ((index + (arr.size() - steps)) % arr.size())
            new_arr[index] = arr[shifted]
        else:
            new_arr[index] = arr[index]
    return new_arr


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------


def sa_range(start: int, end: int) -> StaticArray:
    """
    Method receives two integers and returns a static array containing all
    numbers between those values. The interval is calculated and the array
    instance is created with that size. If the sequence is not in ascending,
    order, start and end are exchanged and the range is iterated over in
    reverse.
    """
    interval = abs(end - start) + 1
    array = StaticArray(interval)
    count = 0

    if start > end:
        temp = start
        start = end
        end = temp

        for index in reversed(range(start, end + 1)):
            array[count] = index
            count += 1
    else:
        for index in range(start, end + 1):
            array[count] = index
            count += 1

    return array


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------


def is_sorted(arr: StaticArray) -> int:
    """
    Method which checks if an array is in ascending, descending, or mixed order.
    It an array is of one element it's considered to be in ascending order and
    returns 1. Otherwise, the array calls two helper methods which will iterate
    through the array checking the order of the elements and returning 1 or 2
    if they are in ascending or descending order, respectively. If neither are
    true, the method returns 0.
    """
    if arr.size() == 1:
        return 1
    if is_sorted_asc(arr):
        return 1
    if is_sorted_desc(arr):
        return 2
    return 0


def is_sorted_asc(arr: StaticArray) -> bool:
    """
    Helper method which iterates through the array checking
    order of elements, in  ascending order.
    """
    for index in range(arr.size()):
        if index > 0 and arr[index - 1] >= arr[index]:
            return False
    return True


def is_sorted_desc(arr: StaticArray) -> bool:
    """
    Helper method which iterates through the array checking
    order of elements, in descending order.
    """
    for index in range(arr.size()):
        if index > 0 and arr[index - 1] <= arr[index]:
            return False
    return True


# ------------------- PROBLEM 7 - SA_SORT -----------------------------------


def sa_sort(arr: StaticArray) -> None:
    """
    Insertion sort implementation for sorting array in ascending order. This
    method sorts the array in place and does not have a return.
    """
    for index in range(1, arr.size()):
        val = arr[index]
        pos = index - 1
        while pos >= 0 and arr[pos] > val:
            arr[pos + 1] = arr[pos]
            pos -= 1
        arr[pos + 1] = val


# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------


def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Removes duplicates by passing the static array passed to the helper get_length,
    which calculates the length of the array without duplicates. Then, a new static
    array instance is created set to that length. The method iterates through the array
    filling in the new static array with elements that are not duplicates, and returns
    when the array is traversed. A counter variable is used in cases where i == i+1
    (i.e, they are duplicates) so as not to skip over indices of the new array.
    """
    new_arr = StaticArray(get_length(arr))
    count = 0
    for index in range(arr.size()):

        if arr.size() == 1:
            new_arr[index] = arr[index]
            return new_arr

        if index == 0:
            new_arr[index] = arr[index]
            count += 1
            continue

        if index == arr.size() - 1:
            if arr[index] != arr[index - 1]:
                new_arr[count] = arr[index]
                return new_arr
            return new_arr

        if arr[index] != arr[index - 1]:
            new_arr[count] = arr[index]
            count += 1

    return new_arr


def get_length(arr: StaticArray) -> int:
    """
    Helper method which takes a static array instance as a parameter and
    returns the length of the array in the "elements" variable. This variable
    is incremented when a unique array element is found.
    """
    elements = 0
    for index in range(arr.size()):
        if arr.size() == 1:
            return 1

        if index == 0:
            elements += 1
            continue

        if index == arr.size() - 1:
            if arr[index] != arr[index - 1]:
                elements += 1
                return elements
            return elements

        if arr[index] != arr[index - 1]:
            elements += 1

    return elements


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    """
    Implementation of the counting sort algorithm. A static array is created
    and filled with zeros, and each instance of each number in the input array
    is incremented in the counts array. These values are then summed and mapped
    to the output array, decrementing the value each time. Finally, the array's
    order is reversed and returned.
    """

    # # get the max number of the array and create a StaticArray of that size
    # min_num, max_num = min_max(arr)
    # count_arr = StaticArray(max_num + 1)
    #
    # # create output array of input array size
    # output_arr = StaticArray(arr.size())
    #
    # # set elements to 0
    # for index in range(count_arr.size()):
    #     count_arr[index] = 0
    #
    # # increment count array with occurrences of each number in input array
    # for index in range(arr.size()):
    #     index = arr[index]
    #     count_arr[index] += 1
    #
    # # sum the values of each element with the element before it
    # for index in range(count_arr.size()):
    #     if index > 0:
    #         count_arr[index] += count_arr[index - 1]
    #
    # # pass element of input array to count array to get element value, and
    # # pass that to the output array
    # for index in range(arr.size()):
    #     val = count_arr[arr[index]]
    #     output_arr[val - 1] = arr[index]
    #
    #     # decrement count array element
    #     count_arr[arr[index]] -= 1
    #
    # reverse(output_arr)
    # return output_arr


# ------------------- PROBLEM 10 - SA_INTERSECTION --------------------------


def sa_intersection(arr1: StaticArray, arr2: StaticArray, arr3: StaticArray) \
        -> StaticArray:
    """
    Finding the intersection of three arrays using a three pointer approach.
    Approach explained in detail in block comments for each step of the imp-
    lementation.
    """
    temp_array = StaticArray(arr3.size())

    # pointers
    i = 0
    j = 0
    k = 0
    index = 0

    # array lengths for keeping track of index
    size1 = arr1.size()
    size2 = arr2.size()
    size3 = arr3.size()

    # iterate through all 3 arrays with a while loop, which is active until any
    # of the arrays has been traversed. the element corresponding to each index, i, j, and k
    # will be compared across all 3 arrays. if the element is the same, the indices are
    # incremented and the value is passed to a temporary static array

    while (i < size1 and j < size2) and k < size3:
        if arr1[i] == arr2[j] and arr2[j] == arr3[k]:
            temp_array[index] = arr1[i]
            index += 1
            i += 1
            j += 1
            k += 1

        # if the compared value is not in all 3 arrays, then one of the three arrays
        # indices will be incremented depending on the value of the elements in each
        # array and the values will be compared again. if one of the arrays is traversed,
        # there is no element which appears in all 3 arrays

        # increment first array index
        elif arr2[j] > arr1[i]:
            i += 1

        # ditto for second array
        elif arr3[k] > arr2[j]:
            j += 1

        # ditto for third array
        else:
            k += 1

    # get length of non-None values in temporary array for creating output array
    counter = 0
    for index in range(temp_array.size()):
        if temp_array[index] is not None:
            counter += 1

    if counter == 0:
        return StaticArray(1)

    output_arr = StaticArray(counter)

    for index in range(temp_array.size()):
        if temp_array[index] is not None:
            output_arr[index] = temp_array[index]

    return output_arr


# ------------------- PROBLEM 11 - SORTED SQUARES ---------------------------


def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Method for sorting squares using an approach similar to the two pointer
    approach in sa_reverse.

    If the element at "start" is greater/equal to the element at "end",
    it indicates a negative value. In that case, the square is placed
    at the "temp" pointer, initially at the end of the array. Start
    is then incremented to point to the next element of the array
    to be squared. Since temp has now been decremented, the next
    greatest or equal value can then be placed into the next index
    to the left.

    In the case that the start element is less than the end element,
    such as in an ascending array of positives, the outermost square,
    which is greatest, will be placed at the end of the array, and
    "end" will be decremented along with temp.
    """

    # set up pointers and create new StaticArray of input array size
    squared = StaticArray(arr.size())
    start = 0
    end = arr.size() - 1
    temp = end

    while start <= end:
        if abs(arr[start]) <= abs(arr[end]):
            squared[temp] = arr[end] ** 2
            end -= 1
        else:
            squared[temp] = arr[start] ** 2
            start += 1
        temp -= 1

    return squared


# ------------------- PROBLEM 12 - ADD_NUMBERS ------------------------------

def add_numbers(arr1: StaticArray, arr2: StaticArray) -> StaticArray:
    """
    Adding the numbers of two arrays representing integer values.
    The array containing the most values is found and a static array
    is created with that size. Next, the input array is traversed
    in reverse, adding the elements of each array. When one of the
    arrays is totally traversed, the process_arr helper is called to
    take the modulo of double digit elements and carry them to the next
    index over, such as in carry addition.
    """

    # get largest number array
    size = max(arr1.size() - 1, arr2.size() - 1)

    # set resultant array to that size + 1
    sum_arr = StaticArray(size + 2)

    # pointers j and k at the end of each array
    j, k = arr1.size() - 1, arr2.size() - 1

    # index pointer
    arr_index = sum_arr.size() - 1

    for index in range(sum_arr.size()):
        sum_arr[index] = 0

    for index in range(size, -1, -1):

        total = arr1[j] + arr2[k]
        sum_arr[arr_index] += total
        arr_index -= 1

        if j == 0:
            k -= 1
            while k >= 0:
                sum_arr[arr_index] += arr2[k]
                k -= 1
                arr_index -= 1

            return process_arr(sum_arr)

        elif k == 0:
            j -= 1
            while j >= 0:
                sum_arr[arr_index] += arr1[j]
                j -= 1
                arr_index -= 1

            return process_arr(sum_arr)

        else:
            j -= 1
            k -= 1

    return sum_arr


def process_arr(arr) -> StaticArray:
    """
    Helper method for add numbers. An array is created containing the amount
    of digits in the input array, and filled with zeros. Next, the method
    takes the modulo of array elements >9 and carries the 1 over to the next
    element. Finally, the resultant array is processed removing any extraneous
    zeros and filling the results into a new StaticArray and returning it.
    """

    count = 0
    for index in range(1, arr.size()):
        count += 1

    sum_arr = StaticArray(count)
    for index in range(sum_arr.size()):
        sum_arr[index] = 0

    arr_index = sum_arr.size() - 1
    for index in range(arr.size() - 1, 0, -1):
        if arr[index] > 9:
            sum_arr[arr_index] += arr[index] % 10
            sum_arr[arr_index - 1] += 1
            arr_index -= 1
        else:
            sum_arr[arr_index] += arr[index]
            arr_index -= 1

    if sum_arr[0] > 9:
        out_arr = StaticArray(sum_arr.size() + 1)
        out_arr[0] = 1
        out_arr[1] = sum_arr[0] % 10

        arr_index = 2
        for index in range(1, sum_arr.size()):
            out_arr[arr_index] = sum_arr[index]
            arr_index += 1
        return out_arr

    return sum_arr


# ------------------- PROBLEM 13 - SPIRAL MATRIX -------------------------


def spiral_matrix(rows: int, cols: int, start: int) -> StaticArray:
    """
    Spiral matrix implementation consisting of four pointers at each border
    of the matrix. When a segment is filled in, such as the rightmost column
    of the matrix, the right pointer is then shifted inwards. This applies
    to all pointers in their respective directions. This method uses a "layer"
    approach where each outer layer of the matrix is filled in, until two pointers
    meet, at which point the matrix will have been completed.
    """

    if start < 0:
        return negative_spiral_matrix(rows, cols, start)

    spiral = StaticArray(rows)
    for index in range(spiral.size()):
        spiral[index] = StaticArray(cols)

    left, right = 0, cols - 1
    top, bottom = 0, rows - 1

    while left <= right and top <= bottom:
        # right column
        for index in range(top, bottom + 1):
            spiral[index][right] = start
            start += 1
        right -= 1

        # bottom row
        for index in range(right, left - 1, -1):
            spiral[bottom][index] = start
            start += 1
        bottom -= 1

        # left column
        for index in range(bottom, top - 1, -1):
            spiral[index][left] = start
            start += 1
        left += 1

        # top row
        for index in range(left, right + 1):
            spiral[top][index] = start
            start += 1
        top += 1

    return spiral


def negative_spiral_matrix(rows: int, cols: int, start: int) -> StaticArray:
    """
    Negative spiral helper method consisting of a similar implementation to
    the clockwise spiral matrix implementation. In this case, pointers are
    and iterators are shifted in order to implement a counter-clockwise
    matrix.
    """

    neg_spiral = StaticArray(rows)
    for index in range(neg_spiral.size()):
        neg_spiral[index] = StaticArray(cols)

    left, right = 0, cols - 1
    top, bottom = 0, rows - 1

    while left <= right and top <= bottom:
        # bottom row
        for index in range(left, right + 1):
            neg_spiral[bottom][index] = start
            start -= 1
        bottom -= 1

        # handle edge cases where the matrix has completed but top and bottom
        # pointers have not met
        if (bottom == 0 and top == 1) or bottom < 0:
            break

        # right column
        for index in range(bottom, top - 1, -1):
            neg_spiral[index][right] = start
            start -= 1
        right -= 1

        # top row
        for index in range(right, left - 1, -1):
            neg_spiral[top][index] = start
            start -= 1
        top += 1

        # left column
        for index in range(top, bottom + 1):
            neg_spiral[index][left] = start
            start -= 1
        left += 1

    return neg_spiral


# ------------------- PROBLEM 14 - TRANSFORM_STRING -------------------------


def transform_string(source: str, s1: str, s2: str) -> str:
    """
    Transform string implementation consisting of a series of four conditionals
    to replace the input strings' characters depending on their value. The results
    are concatenated to outstring and returned.
    """
    outstring = ""

    for index in range(len(source)):
        if source[index] in s1:
            outstring += s2[s1.find(source[index])]
        else:
            if source[index].isupper():
                outstring += ' '
            elif source[index].islower():
                outstring += '#'
            elif source[index].isdigit():
                outstring += '!'
            else:
                outstring += '='

    return outstring


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(min_max(arr))

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(min_max(arr))

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(min_max(arr))

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        print(rotate(arr, steps), steps)
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-105, -99), (-99, -105)]
    for start, end in cases:
        print(start, end, sa_range(start, end))

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print('Result:', is_sorted(arr), arr)

    print('\n# sa_sort example 1')
    test_cases = (
        [1, 10, 2, 20, 3, 30, 4, 40, 5],
        ['zebra2', 'apple', 'tomato', 'apple', 'zebra1'],
        [(1, 1), (20, 1), (1, 20), (2, 20)],
        [random.randint(-10 ** 7, 10 ** 7) for _ in range(5_000)]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr if len(case) < 50 else 'Started sorting large array')
        sa_sort(arr)
        print(arr if len(case) < 50 else 'Finished sorting large array')

    print('\n# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr if len(case) < 50 else 'Started sorting large array')
        result = count_sort(arr)
        print(result if len(case) < 50 else 'Finished sorting large array')

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sa_intersection example 1')
    test_cases = (
        ([1, 2, 3], [3, 4, 5], [2, 3, 4]),
        ([1, 2], [2, 4], [3, 4]),
        ([1, 1, 2, 2, 5, 75], [1, 2, 2, 12, 75, 90], [-5, 2, 2, 2, 20, 75, 95])
    )
    for case in test_cases:
        arr = []
        for i, lst in enumerate(case):
            arr.append(StaticArray(len(lst)))
            for j, value in enumerate(sorted(lst)):
                arr[i][j] = value
        print(sa_intersection(arr[0], arr[1], arr[2]))

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# add_numbers example 1')
    test_cases = (
        ([1, 2, 3], [4, 5, 6]),
        ([0], [2, 5]), ([0], [0]),
        ([2, 0, 9, 0, 7], [1, 0, 8]),
        ([9, 9, 9], [9, 9, 9, 9])
    )
    for num1, num2 in test_cases:
        n1 = StaticArray(len(num1))
        n2 = StaticArray(len(num2))
        for i, value in enumerate(num1):
            n1[i] = value
        for i, value in enumerate(num2):
            n2[i] = value
        print('Original nums:', n1, n2)
        print('Sum: ', add_numbers(n1, n2))

    print('\n# spiral matrix example 1')
    matrix = spiral_matrix(1, 1, 7)
    print(matrix)
    if matrix: print(matrix[0])
    matrix = spiral_matrix(3, 2, 12)
    if matrix: print(matrix[0], matrix[1], matrix[2])

    print('\n# spiral matrix example 2')


    def print_matrix(matrix: StaticArray) -> None:
        rows, cols = matrix.size(), matrix[0].size()
        for row in range(rows):
            for col in range(cols):
                print('{:4d}'.format(matrix[row][col]), end=' ')
            print()
        print()


    test_cases = (
        (4, 4, 1), (3, 4, 0), (2, 3, 10), (1, 2, 1), (1, 1, 42),
        (4, 4, -1), (3, 4, -3), (2, 3, -12), (1, 2, -42),
    )
    for rows, cols, start in test_cases:
        matrix = spiral_matrix(rows, cols, start)
        if matrix: print_matrix(matrix)

    print('\n# transform_strings example 1')
    test_cases = ('eMKCPVkRI%~}+$GW9EOQNMI!_%{#ED}#=-~WJbFNWSQqDO-..@}',
                  'dGAqJLcNC0YFJQEB5JJKETQ0QOODKF8EYX7BGdzAACmrSL0PVKC',
                  'aLiAnVhSV9}_+QOD3YSIYPR4MCKYUF9QUV9TVvNdFuGqVU4$/%D',
                  'zmRJWfoKC5RDKVYO3PWMATC7BEIIVX9LJR7FKtDXxXLpFG7PESX',
                  'hFKGVErCS$**!<OS<_/.>NR*)<<+IR!,=%?OAiPQJILzMI_#[+}',
                  'EOQUQJLBQLDLAVQSWERAGGAOKUUKOPUWLQSKJNECCPRRXGAUABN',
                  'WGBKTQSGVHHHHHTZZZZZMQKBLC66666NNR11111OKUN2KTGYUIB',
                  'YFOWAOYLWGQHJQXZAUPZPNUCEJABRR6MYR1JASNOTF22MAAGTVA',
                  'GNLXFPEPMYGHQQGZGEPZXGJVEYE666UKNE11111WGNW2NVLCIOK',
                  'VTABNCKEFTJHXATZTYGZVLXLAB6JVGRATY1GEY1PGCO2QFPRUAP',
                  'UTCKYKGJBWMHPYGZZZZZWOKQTM66666GLA11111CPF222RUPCJT')
    for case in test_cases:
        print(transform_string(case, '612HZ', '261TO'))
