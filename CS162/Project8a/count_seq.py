# Author: Kevin Sekuj
# Date: 2/18/2021
# Description: Generator function that takes no parameters and generates a sequence
# by enumerating each digit in the previous term.

def count_seq():
    """
    Generator function returning the results of the sequence 2..12..etc. The function
    indexes through the string sequence checking the value at each index - if the value
    equals the next index value over, then count is incremented to represent, such as
    in the case of having "two 1's." Finally, the count and the value itself is added
    to the temporary sequence variable and then the next index is checked.
    """
    # initializing starting sequence to '12'
    seq = "12"
    yield "2"  # yield 2, 12 on first generator calls
    yield "12"
    # continuous loop for following generator calls
    while True:
        # initializing temporary sequence to an empty string and string index to 0
        temp_seq = ""
        index = 0

        while index < len(seq):
            next_index = index + 1
            count = 1

            # if current index's value = next index's value
            # and the next index is not out of bounds
            while next_index < len(seq) and seq[index] == seq[index + 1]:
                index += 1
                count += 1

            # add count of index value plus value itself to temp sequence
            temp_seq += str(count) + seq[index]
            index += 1  # move onto next index

        seq = temp_seq
        yield temp_seq
