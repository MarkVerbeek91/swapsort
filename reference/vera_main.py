# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:38:29 2024

@author: 20192547
"""


def is_sorted(sequence):
    """ "
    Function to check if the given sequence is sorted in ascending order.

    Parameters
    -----------
    sequence:   list
        list containing numbers.

    Returns
    --------
    bool_sorted: boolean
        True when the list is completely sorted in ascending order.
    """
    bool_sorted = all(sequence[i] <= sequence[i + 1] for i in range(len(sequence) - 1))
    return bool_sorted


def getInvCount(sequence):
    """
    Function to count the number of inversions of the sequence.

    Parameters
    -----------
    sequence:   list
        list containing numbers.

    Returns
    --------
    inv_count: integer
        number of inversion of the given sequence.
    """
    inv_count = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j]:
                inv_count += 1
    return inv_count


def closer_to_sorted(sequence, original_sequence):
    """
    Function to compare how many numbers of the sequence are on the same index as in the original sequence

    Parameters
    -----------
    sequence:   list
        list containing numbers.
    original_sequence:  list
        list containing numbers.

    Returns
    --------
    correct_positions:  integer
        number of integers that are on the same position as in the original sequence.
    """
    correct_positions = sum(
        1
        for i, (current, target) in enumerate(zip(sequence, original_sequence), start=1)
        if current == target
    )
    return correct_positions


def sort_sequence(source_sequence):
    """
    Function which sorts a given sequences by the minimal amount of inversions. This is done by determining each possible mutation for a given
    sequence and apply the mutation which meet certain criteria:
        -subsequence not already ordered
        -first integer not already on correct spot
        -mutated sequence less inversions than current sequence or more numbers on correct spot than current sequence
    and then check if this results in a sorted list. If not it will go on and for each mutated sequence (current sequence) determining each
    possible mutation and apply it on the current sequence and again check if it results in sorted list and so on until a sorted list is found.

    Parameters
    -----------
    source_sequence : list
        list containing numbers.

    Returns
    --------
    path : list
        list containing the minimal inversions needed for the sequence to become in ascending order

    """
    queue = [
        (source_sequence, [])
    ]  # Initialize queue with source sequence and empty path
    visited = set()  # Set to keep track of visited states
    front = 0  # Index to keep track of the front of the queue
    min_inversions = getInvCount(source_sequence)
    target_sequence = list(range(1, len(source_sequence) + 1))
    while front < len(queue):
        current_sequence, path = queue[front]
        front += 1

        if is_sorted(current_sequence):  # Check if current sequence is sorted
            return path

        if (
            tuple(current_sequence) not in visited
        ):  # checks if for the current sequence not already mutation are determined
            visited.add(tuple(current_sequence))
            # Generate all possible mutations and add them to the queue except the mutation which put already correct subsequences in wrong order
            for i in range(len(current_sequence) - 1):
                for j in range(i + 1, len(current_sequence)):
                    # checks if mutation is not going to invert already sorted subsequence or integer which is already on the correct spot
                    if (
                        not is_sorted(current_sequence[i : j + 1])
                        and current_sequence[i] != i + 1
                    ):
                        mutation = (
                            current_sequence[:i]
                            + current_sequence[i : j + 1][::-1]
                            + current_sequence[j + 1 :]
                        )
                        if (
                            tuple(mutation) not in visited
                        ):  # check if the given mutation is not already visited then it won't be added to the queue
                            new_inv_count = getInvCount(mutation)
                            # checks if mutation has less inversions than the source sequence or if the sequence has more correct positioned
                            # numbers in the sequence than the current sequence than it will be added to the queue
                            if new_inv_count <= min_inversions or closer_to_sorted(
                                mutation, target_sequence
                            ) >= closer_to_sorted(current_sequence, target_sequence):
                                queue.append((mutation, path + [(i, j)]))
                                if is_sorted(
                                    mutation
                                ):  # Check if mutated sequence is sorted
                                    path = path + [(i, j)]
                                    return path


def inversion_mutations(input_file, output_file):
    """
    Function which opens files and sorts all the sequences to ascending order using the sort_sequence function. It puts the output in the given
    output_file

    Parameters
    ----------
    input_file : string
        name of the inputfile including it's prefixed path. One line containing the number N of source sequences to be transformed and N lines
        each containing one source sequence.
    output_file : string
        name of the output file including it's prefixed path. One line with the number N corresponding to the length of the mutation series,
        i.e., the number of transformation steps that transform the sequence into its sorted version. One line with the source sequence and
        after that k lines each containing the resulting sequence after the corresponding transformation

    Returns
    -------
    None.

    """
    file = open(input_file, "r")
    raw_data = file.read()
    data = raw_data.split("\n")[1:]
    output_data = ""
    n = 0
    for seq in data:
        source_sequence = [int(ele) for ele in seq.split(" ")]
        # Run sort_sequence to sort the sequence
        path = sort_sequence(source_sequence)
        if n > 0:
            output_data += "\n"
        output_data += str(len(path))
        output_data += "\n" + seq
        current_sequence = source_sequence.copy()
        for i, j in path:
            current_sequence[i : j + 1] = reversed(current_sequence[i : j + 1])
            output_data += "\n" + " ".join(map(str, current_sequence))
        n += 1
    with open(output_file, "w") as f:
        f.write(output_data)
