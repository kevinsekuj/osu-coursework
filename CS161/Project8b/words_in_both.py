# Author: Kevin Sekuj
# Date: 11/18/20
# Description: Program which takes two strings and returns a set of words
# contained in both strings, by converting them to lowercase and using
# the split function before finally casting them to two sets. Their common
# words are then found using Python's intersection functionality.

def words_in_both(s1, s2):
    """
    Returns a set containing the common words in two string parameters
    using the intersection functionality.
    """
    set1 = set(s1.lower().split())
    set2 = set(s2.lower().split())
    return set1 & set2
