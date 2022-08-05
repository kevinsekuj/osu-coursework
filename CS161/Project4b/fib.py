# Author: Kevin Sekuj
# Date: 10/13/20
# Description: Program that takes a positive integer parameter and returns
# the number at THAT position of the fibonacci sequence.

def fib(user_num):
    """Calculates fibonacci sequence position by setting a counter <
    user input num and summing it over n iterations."""
    if user_num <= 0:  # program ends if user doesn't input a positive integer
        return
    else:
        counter = 0
        first_num = 0
        second_num = 1
        while counter < user_num:   # while loop which iterates while counter is less than user input
            sum_num = first_num + second_num
            first_num = second_num
            second_num = sum_num
            counter += 1
    return first_num
