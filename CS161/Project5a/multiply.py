# Author: Kevin Sekuj
# Date: 10/27/20
# Recursive function which takes two numbers and returns their product
# by adding them together through a given number of recursive calls

def multiply(num1, num2):
    """Calculates the product of two user input numbers using a
     number recursive calls depending on 2nd user input num"""

    if num2 > 0:  # ensures that parameters are positive
        return num1 + multiply(num1, num2 - 1)
    else:
        return 0  # call ends when num2 = 0
