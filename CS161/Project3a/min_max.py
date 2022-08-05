# Author: Kevin Sekuj
# Date: 10/10/20
# Description: Program that asks the user how many integers they'd like to enter, then enter that
# that many integers, and finally display the minimum and maximum from the numbers they input.

print("How many integers would you like to enter?")
num = int(input())
print("Please enter", num, "integers.")
rangeMin = 999999999  # initialize variables for min and max
rangeMax = -999999999
for i in range(0, num):  # loop will run up to num
    x = int(input())    # loop reads integer input by user one by one
    if x > rangeMax:    # stores integer in rangeMax or rangeMin if conditions met
        rangeMax = x    # and rechecks each loop
    if x < rangeMin:
        rangeMin = x
print("min:", rangeMin)
print("max:", rangeMax)
