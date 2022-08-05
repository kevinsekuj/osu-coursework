# Author: Kevin Sekuj
# Date: 02/08/2022
# Description: Implement a backtracking algorithm


def amount(A: list, S: int) -> list:
    """
    Backtracking function which takes an amount of values as an input array, and
    returns all unique combinations up to the sum S.

    :param A: collection of amount values
    :param S: target sum
    :return: unique combinations of sums up to S
    """
    result = []
    A.sort()

    def backtrack(pos, total, subset):
        # base case - invalid path
        if total > S:
            return

        # base case - found a solution, copy over to our result array
        if total == S:
            result.append(subset[:])
            return

        # else perform a backtrack while taking account for non-unique numbers
        for i in range(pos, len(A)):
            if A[i] == A[i - 1] and i > pos:
                continue

            backtrack(i + 1, total + A[i], subset + [A[i]])

    backtrack(0, 0, [])
    return result


if __name__ == '__main__':
    print(amount([11, 1, 3, 2, 6, 1, 5], 8))
