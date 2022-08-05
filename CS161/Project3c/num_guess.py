# Author: Kevin Sekuj
# Date: 10/10/20
# Description: Program that prompts user for integer that a player has to guess, looping until they get it correct
# at which point it will print their attempts. If they get it first try, it will indicate so.

print("Enter the number for the player to guess.")
guessNum = int(input())        # user inputs mystery integer
print("Enter your guess.")
playerGuessNum = int(input())  # player inputs their guess
attempts = 1  # initialized counter variable to represent total attempts, which will increase by 1 with each guess
if playerGuessNum == guessNum:
    print("You guessed it in 1 try.")
else:
    while playerGuessNum != guessNum:
        if playerGuessNum > guessNum:
            print("Too high - try again:")
            playerGuessNum = int(input())
            attempts += 1
        if playerGuessNum < guessNum:
            print("Too low - try again:")
            playerGuessNum = int(input())
            attempts += 1
    print("You guessed it in", attempts, "tries.")
