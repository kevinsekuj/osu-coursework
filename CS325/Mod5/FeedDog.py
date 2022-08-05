# Author: Kevin Sekuj
# Date: 02/08/2022
# Description: Implement a greedy algorithm

def feedDog(hunger_level: list, biscuit_size: list) -> int:
    """
    Greedy algorithm for satisfying the maximum amount of hungry dogs.
    The function accepts two arrays containing hunger level of dogs and
    the size of the dog food, and our goal is to greedily satisfy the
    maximum number of dogs.

    :param hunger_level: array containing "hunger level" of dogs as integers
    :param biscuit_size: array containing dog food size as integers
    :return: count of dogs we have satisfied
    """
    # initialize pointers and satisfied dogs counter
    i, j, satisfied = 0, 0, 0

    # sort our input arrays to perform a greedy approach
    hunger_level.sort(), biscuit_size.sort()

    # greedily assign dog food to each dog where possible and increment pointers
    while i < len(hunger_level) and j < len(biscuit_size):
        if biscuit_size[j] >= hunger_level[i]:
            satisfied += 1
            i += 1
            j += 1

        else:
            j += 1

    return satisfied


if __name__ == '__main__':
    print(feedDog([1, 2, 3], [1, 1]) == 1)
    print(feedDog([2, 1], [1, 3, 2]) == 2)
