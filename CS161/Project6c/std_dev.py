# Author: Kevin Sekuj
# Date: 11/03/20
# Description:
# Program which calculates the standard deviation of age from a list of people.
# The program class initializes their name and age to private data members which
# the standard deviation method gets for its calculation. The standard deviation is
#  calculated using the variance and mean calculations of the list of people's ages.

class Person:
    """
    Class with two private data members for a person's name and age,
    including an init method that initializes those data members.
    """
    def __init__(self, name, age):
        """
        Initializes private name and age data members.
        """
        self._name = name
        self._age = age

    def get_age(self):
        """
        Get method for returning the private age variable
        which is used in standard deviation calculation.
        """
        return self._age


def std_dev(person_list):
    """
    Method which calculates the standard deviation. The mean is
    calculated by summing the ages of the people in person.list and
    calculating their mean age. Then, the variance is calculated by
    subtracting the mean from the person's ages and squaring them
    and then summing the results. Lastly, using mean and variance
    calculations, the standard deviation can be calculated.
    """
    mean = 0  # initializing mean variable
    for person in person_list:
        # sums the ages of people in person.list to be calculated in mean
        mean += person.get_age()  # summation for mean calculation
    mean /= len(person_list)  # mean calculation
    total = 0  # initializing variable to be used for variance calc
    for person in person_list:
        # variance calculation by subtracting mean from ages in person.age
        # and squaring them, as well as summing them
        total += (person.get_age() - mean) ** 2
        # standard deviation calculation by dividing sum of variance
    return (total / (len(person_list))) ** 0.5
