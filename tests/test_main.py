from pathlib import Path

import pytest

from main import (
    Evolution,
    Mutation,
    MutationIterator,
    MutationList,
    filter_mutations_to_most_sorted,
    find_evolution_fast,
    find_evolutions,
    format_the_output,
    inverse_mutations,
    inverse_mutations_on_location,
    inversion_mutations,
    is_mutation_needed,
    is_solved,
    sequence_quality,
    find_mutations,
)


def test_with_files():
    input_file = Path("sample_sequence_set1.txt")
    output_file = Path("sample_sequence_set1_output.txt")
    inversion_mutations(input_file, output_file)

    input_file = Path("sample_sequence_set2.txt")
    output_file = Path("sample_sequence_set2_output.txt")
    inversion_mutations(input_file, output_file)


def test_inverse_mutations():
    assert inverse_mutations([1]) == [1]
    assert inverse_mutations([2, 1]) == [1, 2]
    assert inverse_mutations([3, 2, 1]) == [1, 2, 3]


def test_inverse_mutation_on_location():
    mut = Mutation(1, 2)
    assert inverse_mutations_on_location([1, 3, 2], mut) == [1, 2, 3]

    mut = Mutation(0, 2)
    assert inverse_mutations_on_location([2, 1, 3], mut) == [1, 2, 3]

    mut = Mutation(0, 3)
    assert inverse_mutations_on_location([3, 2, 1], mut) == [1, 2, 3]


def test_do_not_inverse_sorted_numbers():
    sequence = [1, 2]
    mut = Mutation(0, 2)
    assert not is_mutation_needed(sequence, mut)

    sequence = [2, 1]
    mut = Mutation(0, 2)
    assert is_mutation_needed(sequence, mut)


@pytest.mark.parametrize(
    "sequence, expected",
    [
        ([1, 2], 0),
        ([2, 1], 1),
        ([1, 2, 3], 0),
        ([2, 1, 3], 1),
        ([1, 2, 3, 4], 0),
        ([1, 2, 4, 3], 1),
        ([1, 3, 2, 4], 1),
        ([3, 1, 2, 4], 2),
        ([1, 2, 3, 5, 4], 1),
        ([1, 5, 3, 4, 2], 5),
        ([5, 4, 3, 2, 1], 10),
    ],
)
def test_sequence_quality(sequence, expected):
    assert sequence_quality(sequence) == expected


@pytest.mark.parametrize(
    "sequence, expected",
    [
        ([1, 2], True),
        ([2, 1], False),
    ],
)
def test_sequence_is_solved(sequence, expected):
    assert is_solved(sequence) == expected


@pytest.mark.parametrize(
    "sequence, expected",
    [
        ([2, 1], Mutation(0, 2)),
        ([3, 2, 1], Mutation(0, 3)),
        ([1, 3, 2], Mutation(1, 2)),
        ([1, 4, 3, 2], Mutation(1, 3)),
        ([1, 2, 4, 3], Mutation(2, 2)),
        ([2, 1, 4, 3], Mutation(0, 2)),
    ],
)
def test_sequence_quality_with_mutations(sequence, expected):
    best_mut = find_mutations(len(sequence))
    best_mut = filter_mutations_to_most_sorted(
        Evolution(sequence, MutationList([])), best_mut
    )
    assert best_mut[0] == expected


@pytest.mark.parametrize(
    "sequence, expected",
    [
        # ([1, 2], []),  # function should not run on a sequence in order
        # ([1, 2, 3], []),
        ([2, 1, 4, 3], [Mutation(0, 2), Mutation(2, 2)]),
        ([2, 4, 1, 3], [Mutation(0, 3), Mutation(1, 2), Mutation(1, 3)]),
    ],
)
def test_sequence_quality_with_mutations_multiple(sequence, expected):
    best_mut = find_mutations(len(sequence))
    best_mut = filter_mutations_to_most_sorted(
        Evolution(sequence, MutationList([])), best_mut
    )
    assert best_mut == expected


def test_format_the_output():
    data = [3, 2, 1, 4, 8, 7, 6, 5, 9]
    mutations = MutationList([Mutation(0, 3), Mutation(4, 4)])

    assert format_the_output(data, mutations) == (
        "2\n" "3 2 1 4 8 7 6 5 9\n" "1 2 3 4 8 7 6 5 9\n" "1 2 3 4 5 6 7 8 9\n"
    )

    data = [1, 2, 4, 3, 5, 8, 7, 9, 6]
    mutations = MutationList([Mutation(2, 2), Mutation(7, 2), Mutation(5, 3)])
    assert format_the_output(data, mutations) == (
        "3\n"
        "1 2 4 3 5 8 7 9 6\n"
        "1 2 3 4 5 8 7 9 6\n"
        "1 2 3 4 5 8 7 6 9\n"
        "1 2 3 4 5 6 7 8 9\n"
    )


def test_acceptance_test():
    sequence = [3, 2, 1, 4, 8, 7, 6, 5, 9]
    evolution = Evolution(sequence, MutationList([]))

    solution = find_evolutions([evolution])
    output = format_the_output(sequence, solution.mutations)
    assert output == (
        "2\n" "3 2 1 4 8 7 6 5 9\n" "1 2 3 4 8 7 6 5 9\n" "1 2 3 4 5 6 7 8 9\n"
    )


def test_acceptance_test_01():
    sequence = [1, 2, 4, 3, 5, 8, 7, 9, 6]
    evolution = Evolution(sequence, MutationList([]))

    solution = find_evolutions([evolution])
    output = format_the_output(sequence, solution.mutations)
    assert output == (
        "3\n"
        "1 2 4 3 5 8 7 9 6\n"
        "1 2 3 4 5 8 7 9 6\n"
        "1 2 3 4 5 8 7 6 9\n"
        "1 2 3 4 5 6 7 8 9\n"
    )


def test_acceptance_test_02():
    sequence = [1, 2, 4, 3, 5, 8, 7, 9, 6]
    evolution = Evolution(sequence, MutationList([]))
    mutation_iterator = MutationIterator(len(sequence))
    solution = find_evolution_fast([evolution], mutation_iterator)
    output = format_the_output(sequence, solution.mutations)
    assert output == (
        "3\n"
        "1 2 4 3 5 8 7 9 6\n"
        "1 2 3 4 5 8 7 9 6\n"
        "1 2 3 4 5 8 7 6 9\n"
        "1 2 3 4 5 6 7 8 9\n"
    )


def test_acceptance_test_03():
    long_sequence = [1, 2, 4, 3, 5, 8, 7, 10, 9, 6]

    evolution = Evolution(long_sequence, MutationList([]))
    mutation_iterator = MutationIterator(len(long_sequence))
    solution = find_evolution_fast([evolution], mutation_iterator)
    output = format_the_output(long_sequence, solution.mutations)
    assert output == (
        "3\n"
        "1 2 4 3 5 8 7 10 9 6\n"
        "1 2 3 4 5 8 7 10 9 6\n"
        "1 2 3 4 5 8 7 6 9 10\n"
        "1 2 3 4 5 6 7 8 9 10\n"
    )


def test_acceptance_test_04():
    long_sequence = [1, 2, 4, 3, 5, 8, 7, 10, 9, 6]
    evolution = Evolution(long_sequence, MutationList([]))
    solution = find_evolutions([evolution])
    output = format_the_output(long_sequence, solution.mutations)
    assert output == (
        "3\n"
        "1 2 4 3 5 8 7 10 9 6\n"
        "1 2 3 4 5 8 7 10 9 6\n"
        "1 2 3 4 5 8 7 6 9 10\n"
        "1 2 3 4 5 6 7 8 9 10\n"
    )
