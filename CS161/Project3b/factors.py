# Author: Kevin Sekuj
# Date: 10/10/20
# Description: Program which lists all positive numbers that divide a
# user input integer evenly, in ascending order

userNum = int(input("Please enter a positive integer: "))
print("The factors of", userNum, "are:")
for integerInRange in range(1, userNum + 1):  # iterates integers from 1 to the user input integer
    if userNum % integerInRange == 0:  # mod operation between user input integer and each integer in range from
        print(integerInRange)          # 1 to user input integer (userNum) to check if it's divisible and thus a factor
