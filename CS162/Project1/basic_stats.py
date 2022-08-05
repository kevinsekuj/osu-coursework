# Author: Kevin Sekuj
# Date: 1/1/20
# Description: Program that takes a person's name and age as private data members in each
# person object. The person objects are passed to a method which gets their private age data
# member and appends it to an empty list. Lastly, the statistics module is used to return
# the mean, median, and mode of the ages passed to the class.

import statistics as stats


class Person:
    def __init__(self, person, age):
        """
        Method for initializing the private name and age data members of each
        argument passed to the class.
        """
        self._name = person
        self._age = age

    def get_age(self):
        """
        Method for getting the private age data member of a person object, used
        in the basic_stats function.
        """
        return self._age


def basic_stats(person_object):
    """
    Indexes through the the Person object, getting the age attribute at each index
    and appending it to an empty list, calculating the mean, median, and mode of
    the list using statistics and then returning them as a tuple.
    """
    ages_list = [index.get_age() for index in person_object]
    return stats.mean(ages_list), stats.median(ages_list), stats.mode(ages_list)
