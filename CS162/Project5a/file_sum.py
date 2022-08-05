# Author: Kevin Sekuj
# Date: 1/21/2021
# Description: Program with a function that takes a text file name as a parameter,
# containing a list of numbers, one on each line. Strip is called on the numbers to
# remove new lines, and the strings are converted to ints. Lastly, The program's function
# sums the values, and writes their sums to a file called sum.txt.

def file_sum(file_nums):
    """
    Function takes a file name holding a list of numbers as a parameter, then
    sums the numbers and writes them to a new text file.
    """
    with open(file_nums, 'r') as infile:
        nums_sum = 0
        for nums in infile:
            nums_sum += float(nums.strip())

    with open('sum.txt', 'w') as outfile:
        outfile.write(str(nums_sum))
