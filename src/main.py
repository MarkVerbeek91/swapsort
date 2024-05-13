import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Generator


@dataclass
class Mutation:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length

    def __eq__(self, other: "Mutation") -> bool:
        return self.start == other.start and self.length == other.length

    def __str__(self) -> str:
        return f"Mutation: {self.start} {self.end}"


@dataclass
class MutationList:
    mutations: list[Mutation]

    def __add__(self, other: Mutation) -> "MutationList":
        return MutationList([*self.mutations, other])

    def __len__(self) -> int:
        return len(self.mutations)

    def __getitem__(self, item: int) -> Mutation:
        return self.mutations[item]

    def __str__(self) -> str:
        return "->".join([f"Mut: '{mut.start}-{mut.length}'" for mut in self.mutations])


class MutationIterator:
    def __init__(self, length: int) -> None:
        self.mutations = find_mutations(length)
        self._index = 0

    def __iter__(self) -> "MutationIterator":
        self._index = 0
        return self

    def __next__(self) -> Mutation:
        try:
            result = self.mutations[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result


class Evolution:
    def __init__(self, sequence: list[int], mutations: MutationList) -> None:
        self.sequence = sequence
        self.mutations = mutations
        self.solved = is_solved(self.sequence)

    def __or__(self, other: Mutation) -> bool:
        return other in self.mutations or not is_mutation_needed(self.sequence, other)

    def __add__(self, other: Mutation) -> "Evolution":
        sequence = inverse_mutations_on_location(self.sequence, other)
        return Evolution(sequence, self.mutations + other)

    def __len__(self) -> int:
        return len(self.sequence)

    def __str__(self) -> str:
        return f"Evolution: {self.solved}:{len(self.mutations)}\n{str(self.mutations)}"


def inversion_mutations(input_file: Path, output_file: Path) -> None:
    with open(input_file, "r") as f:
        raw_data = f.read()

    data = raw_data.split("\n")[1:]

    sequences: list[list[int]] = []
    for i, line in enumerate(data):
        sequences.append(list(map(int, line.split())))

    data = ""
    for sequence in sequences:
        # solution = find_evolutions([Evolution(sequence, MutationList([]))])
        print(f"Sequence: {sequence}")
        mutation_iterator = MutationIterator(len(sequence))
        solution = find_evolution_fast(
            [Evolution(sequence, MutationList([]))], mutation_iterator
        )
        data += format_the_output(sequence, solution.mutations)

    with open(output_file, "w") as f:
        f.write(data)


def find_evolutions(evolutions: list[Evolution]) -> Evolution:
    # list all possible mutations.
    mutations = find_mutations(len(evolutions[0]))

    # create a list of evolutions.
    evolutions = [ev + mu for ev in evolutions for mu in mutations if not ev | mu]

    # check if any of the evolutions are already solved.
    solutions = list(filter(lambda x: x.solved, evolutions))

    if solutions:
        return solutions[0]

    # recurse to find the best solution
    return find_evolutions(evolutions)


def find_evolution_fast(
        evolutions: list[Evolution], mutation_iterator: MutationIterator
) -> Evolution:
    evaluated_evolutions: list[Evolution] = []

    for evolution in evolution_iterator(evolutions, mutation_iterator):
        if evolution.solved:
            return evolution
        evaluated_evolutions.append(evolution)

    return find_evolution_fast(evaluated_evolutions, mutation_iterator)


def evolution_iterator(
        evolutions: list[Evolution], mutations: MutationIterator
) -> Generator[Evolution, None, None]:
    yield from iter(ev + mu for ev in evolutions for mu in mutations if not ev | mu)


def find_mutations(length: int) -> list[Mutation]:
    mutation_options = itertools.product(range(length), range(2, length + 1))
    mutation_filtered = filter(lambda x: x[0] + x[1] <= length, mutation_options)
    mutation_objects = list(map(lambda x: Mutation(x[0], x[1]), mutation_filtered))

    return mutation_objects


def filter_mutations_to_most_sorted(
        evolution: Evolution, mutations: list[Mutation]
) -> list[Mutation]:
    mutation_sequences = list(
        map(
            lambda mut: inverse_mutations_on_location(evolution.sequence, mut),
            mutations,
        )
    )

    seq_quality = list(map(sequence_quality, mutation_sequences))

    min_quality = min(seq_quality)
    best_mut = [
        x[0] for i, x in enumerate(zip(mutations, seq_quality)) if (x[1] == min_quality)
    ]
    return best_mut


def inverse_mutations_on_location(sequence: list[int], mutation: Mutation) -> list[int]:
    start, end = mutation.start, mutation.end
    return sequence[:start] + inverse_mutations(sequence[start:end]) + sequence[end:]


def inverse_mutations(sequence: list[int]) -> list[int]:
    return sequence[::-1]


def is_solved(sequence: list[int]) -> bool:
    return sequence_quality(sequence) == 0


def is_mutation_needed(sequence: list[int], mut: Mutation) -> bool:
    return not is_solved(sequence[mut.start: mut.end])


def sequence_quality(seq: list[int]) -> int:
    return sum(
        [1 for i, x in enumerate(seq) for j, y in enumerate(seq[i + 1:]) if x > y]
    )


def format_the_output(sequence: list[int], mutations: MutationList) -> str:
    steps: list[list[int]] = [sequence]
    for mutation in mutations.mutations:
        sequence = inverse_mutations_on_location(sequence, mutation)
        steps.append(sequence)

    steps_str = "\n".join([" ".join(map(str, m)) for m in steps])

    return f"{len(mutations)}\n{steps_str}\n"


if __name__ == "__main__":
    inversion_mutations(Path("input.txt"), Path("output.txt"))
