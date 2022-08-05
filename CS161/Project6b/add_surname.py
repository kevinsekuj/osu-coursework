# Author: Kevin Sekuj
# Date: 11/02/20
# Description: Program which uses a list of first names as a parameter and
# uses list comprehension to return a list of names starting with K plus
# the surname "Kardashian", with a space in between.

def add_surname(first_names_list):
    """
    Function that takes string parameter from list of first names and checks if
    the name starts with the letter K. If so, it returns the first name
    added with the surname "Kardashian" with a space in between.
    """
    names_list = [name + " Kardashian" for name in first_names_list if name[0] == "K"]
    return names_list


first_names_list = ["Kiki", "Krystal", "Pavel", "Annie", "Koala"]  # original list of first names to be used in function
