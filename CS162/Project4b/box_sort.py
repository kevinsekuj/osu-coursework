# Author: Kevin Sekuj
# Date:  1/15/2021
# Description: Program with a Box class which takes 3 parameters and uses them to
# initialize private length, width, and height data members, and has a method
# for returning the volume of the box, as well as its attributes. Separate function
# box_sort uses insertion sort to sort a list of Boxes from greatest to least volume.


class Box:
    """
    Box class containing private parameters for length, width, height.
    """

    def __init__(self, length, width, height):
        self._length = length
        self._width = width
        self._height = height

    def get_length(self):
        """
        Method for returning length of the box.
        """
        return self._length

    def get_width(self):
        """
        Method for returning width of the box.
        """
        return self._width

    def get_height(self):
        """
        Method for returning height of the box.
        """
        return self._height

    def volume(self):
        """
        Method to return the volume of the box.
        """
        return self._length * self._width * self._height


def box_sort(box_list):
    """
    Method using insertion sort to sort a list of Boxes from greatest volume
    to least volume, in descending order.
    """
    for index in range(1, len(box_list)):
        value = box_list[index]
        pos = index - 1
        while pos >= 0 and box_list[pos].volume() < value.volume():
            box_list[pos + 1] = box_list[pos]
            pos -= 1
        box_list[pos + 1] = value
