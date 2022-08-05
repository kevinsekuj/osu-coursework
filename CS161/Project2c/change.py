# Author: Kevin Sekuj
# Date: 10/5/20
# Description: Program which asks the user for a number of cents,
# then outputs how many coins of each type would represent that amount, using the fewest total number of coins.

print("Please enter an amount in cents less than a dollar.")
amount = int(input())
Q = (amount // 25)  # Floor division operation to determine fewest number of coins
Qr = (amount % 25)  # Mod operation to determine the remainder from division by the coin's value
D = (Qr // 10)
Dr = (Qr % 10)
N = (Dr // 5)
Nr = (Dr % 5)
P = (Nr // 1)
Pr = (Nr % 1)

print("Your change will be:")
print("Q:", + Q)
print("D:", + D)
print("N:", + N)
print("P:", + P)
