# Author: Kevin Sekuj
# Date: 11/18/20
# Description: Program which takes a string from a user and converts it
# to uppercase. It then checks if the string's letters are in the English
# alphabet. If so, it adds the letter to a dictionairy key and then counts
# the presence of that specific letter.

def count_letters(user_string):
    """
    Checks if user string is in the English alphabet, converts their
    string to uppercase, and then outputs the count of each letter
    in dictionairy form.
    """
    string_dict = {}  # initializing dictionairy for return
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for letter in user_string.upper():  # converting string to all uppercase
        if letter in alphabet_list:
            if letter in string_dict:
                string_dict[letter] += 1
            else:
                string_dict[letter] = 1
    return string_dict
