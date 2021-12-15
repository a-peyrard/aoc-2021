"""
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization
equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves
should even have the necessary input elements in sufficient quantities.
The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer
template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result
after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

The first line is the polymer template - this is the starting point of the process.
The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are
immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.
So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

    The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
    The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
    The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all
pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.
After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs
1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common
element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.
Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What
 do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

--- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair
insertion process; a total of 40 steps should do it.
In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H
(occurring 3849876073 times); subtracting these produces 2188189693529.
Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result.
What do you get if you take the quantity of the most common element and subtract the quantity of the least common
element?



"""
from collections import defaultdict
from typing import Dict, Tuple


def generate_template(initial: str,
                      rules: Dict[str, str],
                      nb_steps: int) -> int:

    known_generation: Dict[str, Tuple[str, str]] = {}

    # count the pairs for the initial template
    pairs: Dict[str, int] = defaultdict(int)
    previous = initial[0]
    for char in initial[1:]:
        current_pair = previous + char
        pairs[current_pair] += 1
        previous = char

    for step in range(nb_steps):
        new_pairs = defaultdict(int)
        for pair, occurrences in pairs.items():
            pair1, pair2 = _generate_pairs(pair, known_generation, rules)
            pairs[pair] = 0
            new_pairs[pair1] += occurrences
            new_pairs[pair2] += occurrences
        pairs = new_pairs

    count_characters = defaultdict(int)
    for pair, occurrences in pairs.items():
        count_characters[pair[0]] += occurrences
        count_characters[pair[1]] += occurrences

    # divide by 2 as all letters are counted twice, except for the first and last letter
    values = sorted(
        (
            (int(count / 2) + (1 if char == initial[0] or char == initial[-1] else 0), char)
            for char, count in count_characters.items()
        ),
        key=lambda t: t[0]
    )

    max_occurrence, max_char = values[-1]
    min_occurrence, min_char = values[0]
    print(f'char {max_char} found {max_occurrence} times')
    print(f'char {min_char} found {min_occurrence} times')
    print(f'values {values}')

    return max_occurrence - min_occurrence


def _generate_pairs(pair: str,
                    known_generations: Dict[str, Tuple[str, str]],
                    rules: Dict[str, str]) -> Tuple[str, str]:
    generated = known_generations.get(pair)
    if not generated:
        char_to_add = rules[pair]
        generated = (pair[0] + char_to_add, char_to_add + pair[1])
        known_generations[pair] = generated

    return generated
