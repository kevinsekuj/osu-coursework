# Author: Kevin Sekuj
# Date: 1/21/2021
# Description: Program which reads a JSON file containing 2010 SAT results for
# New York City, and saves the data containing the results themselves to a private
# data member of the constructor method. The program contains a save_as_csv method
# which takes specific district bureau numbers as parameters, and writes the rows
# containing their SAT data (such as school, number of pupils, and scores) to a csv
# file.

import json


class SatData:
    """
    SatData class with constructor method and save_as_csv methods. Reads
    a sat.json file and writes specific DBN entries in the file to a new
    file in ascending order.
    """

    def __init__(self):
        """
        Constructor method, reading a sat.json file, and saving the ['data'] key
        of the dict (containing lists of SAT results by school) to a private data
        member.
        """
        with open('sat.json', 'r') as infile:
            sat_data = json.load(infile)
        self._sat_data = sat_data['data']

    def save_as_csv(self, dbns):
        """
        Method which accepts DBN numbers as parameters, sorts them, and searches
        _sat_data for the corresponding lists containing that data. When they're
        found, it slices the list so as to keep only the rows corresponding to
        DBNs, and appends it to dbn_list. The list 'rows' are then written to
        output.csv.
        """

        # hardcoded header
        dbn_list = [['DBN', 'School Name', 'Number of Test Takers',
                     'Critical Reading Mean', 'Mathematics Mean', 'Writing Mean']]

        for dbn in sorted(dbns):
            for index in range(len(self._sat_data)):
                if dbn in self._sat_data[index]:
                    dbn_list.append(self._sat_data[index][8:])

        with open('output.csv', 'w') as outfile:
            for row in dbn_list:
                outfile.write(','.join(row) + '\n')
