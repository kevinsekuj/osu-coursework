# Author: Kevin Sekuj
# Date: 07/24/21
# Description: CS362 A2: TDD Hands On - utilize and apply TDD techniques to
# implement a check_pwd function which checks input strings against a defined
# specification.

def check_pwd(param):
    if not param:
        return False

    if len(param) < 8:
        return False

    if len(param) > 20:
        return False

    contains_lower = False
    contains_upper = False
    contains_digit = False
    contains_special = False
    special_chars = "~`!@#$%^&*()_+-="

    for char in param:
        if char.islower():
            contains_lower = True
        elif char.isupper():
            contains_upper = True
        elif char.isdigit():
            contains_digit = True
        elif char in special_chars:
            contains_special = True

    if not contains_digit or not contains_upper or not contains_lower \
            or not contains_special:
        return False

    return True
