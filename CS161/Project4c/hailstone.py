# Author: Kevin Sekuj
# Date: 10/13/20
# Description: Hailstone sequence program which requires the user to input
# a positive integer, then divides it by 2 or multiplies it by 3 and adds 1
# depending on whether it's even or odd, respectively, until it gets to the
# integer 1 at which point it will end and return the total steps it took.

def hailstone(user_num):
    """Takes a positive int as an initial integer and returns how many
        steps it takes to reach the integer 1 through hailstone sequence."""
    count = 0  # variable for number of steps it takes to reach 1
    while user_num != 1:  # while loop for producing next num in sequence
        if user_num % 2 == 0:  # while user_num != 1
            user_num //= 2
            count += 1
        else:
            user_num = user_num * 3 + 1
            count += 1
    return count
