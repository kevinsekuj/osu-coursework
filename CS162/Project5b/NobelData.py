# Author: Kevin Sekuj
# Date: 1/21/2021
# Description: Program which reads a JSON file with data on Nobel Prize winners,
# and allows the user to search the data. The NobelData class contains a method
# called search_nobel that allows a user to search with a year and category,
# returning a sorted list of surnames for the winners in that category, for that
# particular year.

import json


class NobelData:
    """
    NobleData class with init and search_nobel methods, allowing user to search
    nobel prize winners.
    """

    def __init__(self):
        """
        Constructor method opening and reading the prize.json file, and assigning
        its contents to a variable.
        """
        with open('nobels.json', 'r') as infile:
            prize_dict = json.load(infile)
        self._prize_dict = prize_dict

    def search_nobel(self, year, category):
        """
        Takes a year and category as string parameters, and searches
        the list members of prizes_dict. Each list contains a dict with 'year'
        and 'category' keys. If the values of those keys equal the params, their
        'laureates' key is looped through, adding each nobel laureate's surname to
        a surnames list, which is finally sorted and returned.
        """

        for index in range(len(self._prize_dict['prizes'])):

            if year == self._prize_dict['prizes'][index]['year'] and \
                    category == self._prize_dict['prizes'][index]['category']:

                # list comp looping through laureate key's lists, which hold dicts with
                # a surname key, and appending the values to the list.
                surnames = [self._prize_dict['prizes'][index]['laureates'][member]['surname']
                            for member in range(len(self._prize_dict['prizes'][index]['laureates']))]

            else:
                continue

            return sorted(surnames)
