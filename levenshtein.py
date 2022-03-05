from typing import Tuple

import numpy as np


def min_edit_distance(source: str,
                      target: str,
                      insert_cost: int = 1,
                      delete_cost: int = 1,
                      replace_cost: int = 2) -> Tuple[np.ndarray, int]:
    """Implementation of minimum edit distance (Levenshtein distance) using dynamic programming.

    Args:
        source (str): First string.
        target (str): Second string.
        insert_cost (int): Insertion cost of one character, by default set to 1.
        delete_cost (int): Deletion cost of one character, by default set to 1.
        replace_cost (int): Replacement of one character to another, by default set to 2.

    Returns:
        Tuple[np.ndarray, int]: 2D numpy array with cost table and resulting edit distance.
    """
    source_length = len(source)
    target_length = len(target)

    # Initialize cost table with zeros and dimensions (source_length+1,target_length+1)
    cost_table = np.zeros((source_length + 1, target_length + 1), dtype=int)

    # Fill in column 0, from row 1 till the end
    for row in range(1, source_length + 1):
        cost_table[row, 0] = cost_table[row - 1, 0] + delete_cost

    # Fill in row 0, from column 1 till the end
    for col in range(1, target_length + 1):
        cost_table[0, col] = cost_table[0, col - 1] + insert_cost

    # Loop through row 1 till the end
    for row in range(1, source_length + 1):

        # Loop through column 1 till the end
        for col in range(1, target_length + 1):

            # Initialize temporal replace cost to the replace cost that is passed into this function
            temp_replace_cost = replace_cost

            # Check if source character at the previous row matches the target character at the
            # previous column and update the replacement cost to 0 if source and target are the same
            if source[row - 1] == target[col - 1]:
                temp_replace_cost = 0

            # Update the cost at row, col based on previous entries in the cost table
            cost_table[row, col] = min([
                cost_table[row - 1, col] + delete_cost,
                cost_table[row, col - 1] + insert_cost,
                cost_table[row - 1, col - 1] + temp_replace_cost
            ])

    # Fetch the minimum edit distance as the cost found at the last indices of table
    minimum_edit_distance = cost_table[-1, -1]

    return cost_table, minimum_edit_distance


print(min_edit_distance('asudf', 'asdfvbd'))
