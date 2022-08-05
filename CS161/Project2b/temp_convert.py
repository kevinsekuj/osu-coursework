# Author: Kevin Sekuj
# Date: 10/5/20
# Description: Program which converts a user input celsius temperature into fahrenheit.

print("Please enter a Celsius temperature. ", )
tempc = float(input())  # tempc refers to user input temperature in celsius
tempf = float((9/5) * tempc + 32)  # tempf refers to converted temperature in fahrenheit
print("The equivalent Fahrenheit temperature is: ")
print(tempf)
