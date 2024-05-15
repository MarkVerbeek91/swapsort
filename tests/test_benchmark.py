from time import time

import pytest

from main import (
    Evolution,
    EvolutionIterator,
    MutationIterator,
    MutationList,
    find_evolution_fast,
    find_evolution_lean,
    format_the_output,
)


def find_evolution_wrapper(long_sequence):
    evolution = Evolution(long_sequence, MutationList([]))
    mutation_iterator = MutationIterator(len(long_sequence))

    return find_evolution_fast([evolution], mutation_iterator)


def find_evolution_fast_wrapper(long_sequence):
    evolution = Evolution(long_sequence, MutationList([]))
    mutation_iterator = MutationIterator(len(long_sequence))

    return find_evolution_fast([evolution], mutation_iterator)


def find_evolution_lean_wrapper(long_sequence):
    evolution = Evolution(long_sequence, MutationList([]))
    mutation_iterator = MutationIterator(len(long_sequence))
    evolution_iter = EvolutionIterator(evolution, [mutation_iterator])

    return find_evolution_lean(evolution_iter, mutation_iterator)


@pytest.mark.parametrize(
    "long_sequence, function",
    [
        ([1, 2, 4, 3, 5, 8, 7, 10, 9, 6], find_evolution_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 10, 9, 6], find_evolution_fast_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 10, 9, 6], find_evolution_lean_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 9, 6, 12, 11], find_evolution_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 9, 6, 12, 11], find_evolution_fast_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 9, 6, 12, 11], find_evolution_lean_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 9, 6, 13, 12, 11], find_evolution_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 9, 6, 13, 12, 11], find_evolution_fast_wrapper),
        ([1, 2, 4, 3, 5, 8, 7, 9, 6, 13, 12, 11], find_evolution_lean_wrapper),
    ],
)
def test_benchmark(long_sequence, function):
    start_time = time()

    solution = function(long_sequence)

    end_time = time()

    print(f"Execution time: {end_time - start_time:.2f} seconds")

    print(format_the_output(long_sequence, solution.mutations))


def test_very_long_sequence():
    # long_sequence = [1, 2, 4, 3, 5, 8, 7, 9, 6, 13, 14, 15, 12, 11]
    long_sequence = [1, 2, 4, 3, 5, 8, 7, 12, 13, 11, 10, 9, 6]

    start_time = time()

    solution = find_evolution_lean_wrapper(long_sequence)

    end_time = time()

    print(f"Execution time: {end_time - start_time:.2f} seconds")

    print(format_the_output(long_sequence, solution.mutations))
