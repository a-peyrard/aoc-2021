"""
--- Day 23: Amphipod ---

A group of amphipods notice your fancy submarine and flag you down. "With such an impressive shell," one amphipod says,
"surely you can help us with a question that has stumped our best scientists."
They go on to explain that a group of timid, stubborn amphipods live in a nearby burrow. Four types of amphipods live
there: Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a hallway and four side
 rooms. The side rooms are initially full of amphipods, and the hallway is initially empty.
They give you a diagram of the situation (your puzzle input), including locations of each amphipod (A, B, C, or D, each
of which is occupying an otherwise open space), walls (#), and open space (.).

For example:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

The amphipods would like a method to organize every amphipod into side rooms so that each side room contains one type
of amphipod and the types are sorted A-D going left to right, like this:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space. Each type of
amphipod requires a different amount of energy to move one step: Amber amphipods require 1 energy per step, Bronze
amphipods require 10 energy, Copper amphipods require 100, and Desert ones require 1000. The amphipods would like you
to find a way to organize the amphipods that requires the least total energy.
However, because they are timid and stubborn, the amphipods have some extra rules:

    Amphipods will never stop on the space immediately outside any room. They can move into that space so long as they
    immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that are directly
    above an amphipod starting position.)
    Amphipods will never move from the hallway into a room unless that room is their destination room and that room
    contains no amphipods which do not also have that room as their own destination. If an amphipod's starting room is
    not its destination room, it can stay in that room until it leaves the room. (For example, an Amber amphipod will
    not move from the hallway into the right three rooms, and will only move into the leftmost room if that room is
    empty or if it only contains other Amber amphipods.)
    Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. (That is,
    once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not move
    again until they can move fully into a room.)

In the above example, the amphipods can be organized using a minimum of 12521 energy. One way to do this is shown below.
Starting configuration:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

One Bronze amphipod moves into the hallway, taking 4 steps and using 40 energy:

#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########

The only Copper amphipod not in its side room moves there, taking 4 steps and using 400 energy:

#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########

A Desert amphipod moves out of the way, taking 3 steps and using 3000 energy, and then the Bronze amphipod takes its
place, taking 3 steps and using 30 energy:

#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########

The leftmost Bronze amphipod moves to its room using 40 energy:

#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########

Both amphipods in the rightmost room move into the hallway, using 2003 energy in total:

#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########

Both Desert amphipods move into the rightmost room using 7000 energy:

#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########

Finally, the last Amber amphipod moves into its room, using 8 energy:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

What is the least energy required to organize the amphipods?
"""
from typing import List, Optional, Callable, Tuple, Dict

from aoc.util.priority_queue import PriorityQueue


DEBUG = True


State = Tuple[Optional[str], ...]


class Neighbor:
    def __init__(self, destination: int, condition: Callable[[str, State], bool]):
        self.destination = destination
        self.condition = condition


class Cell:
    def __init__(self, idx: int, neighbors: List[Neighbor]):
        self.idx = idx  # for debugging purpose...
        self.neighbors = neighbors


def _empty_or_same(cell: int, amphipod: str, state: State) -> bool:
    return state[cell] is None or state[cell] == amphipod


def _empty(cell: int, state: State) -> bool:
    return state[cell] is None


STEPS = [
    [0, 1, 3, 4, 3, 5, 6, 5, 7, 8, 7, 9, 10, 9, 10],  # 0
    [1, 0, 2, 3, 2, 4, 5, 4, 6, 7, 6, 8, 9, 8, 9],  # 1
    [3, 2, 0, 1, 2, 4, 5, 4, 6, 7, 6, 8, 9, 8, 9],  # 2
    [4, 3, 1, 0, 3, 5, 6, 5, 7, 8, 7, 9, 10, 9, 10],  # 3
    [3, 2, 2, 3, 0, 2, 3, 2, 4, 5, 4, 6, 7, 6, 7],  # 4
    [5, 4, 4, 5, 2, 0, 1, 2, 4, 5, 4, 6, 7, 6, 7],  # 5
    [6, 5, 5, 6, 3, 1, 0, 3, 5, 6, 5, 7, 8, 7, 8],  # 6
    [5, 4, 4, 5, 2, 2, 3, 0, 2, 3, 2, 4, 5, 4, 5],  # 7
    [7, 6, 6, 7, 4, 4, 5, 2, 0, 1, 2, 4, 5, 4, 5],  # 8
    [8, 7, 7, 8, 5, 5, 6, 3, 1, 0, 3, 5, 6, 5, 6],  # 9
    [7, 6, 6, 7, 4, 4, 5, 2, 2, 3, 0, 2, 3, 2, 3],  # 10
    [9, 8, 8, 9, 6, 6, 7, 4, 4, 5, 2, 0, 1, 2, 3],  # 11
    [10, 9, 9, 10, 7, 7, 8, 5, 5, 6, 3, 1, 0, 3, 4],  # 12
    [9, 8, 8, 9, 6, 6, 7, 4, 4, 5, 2, 2, 3, 0, 1],  # 13
    [10, 9, 9, 10, 7, 7, 8, 5, 5, 6, 3, 3, 4, 1, 0],  # 14
]


WEIGHTS: Dict[str, int] = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


DONE_STATE: State = (
    None,  # 0
    None,  # 1
    "A",  # 2
    "A",  # 3
    None,  # 4
    "B",  # 5
    "B",  # 6
    None,  # 7
    "C",  # 8
    "C",  # 9
    None,  # 10
    "D",  # 11
    "D",  # 12
    None,  # 13
    None,  # 14
)


# pylint: disable
CELLS = [
    Cell(
        idx=0,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty(1, s) and _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(1, s) and _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty(1, s) and _empty(4, s) and _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(1, s) and _empty(4, s) and _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty(1, s) and _empty(4, s) and _empty(7, s) and _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(1, s) and _empty(4, s) and _empty(7, s) and _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty(1, s) and _empty(4, s) and _empty(7, s) and _empty(10, s)
                and _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(1, s) and _empty(4, s) and _empty(7, s) and _empty(10, s)
                and _empty(11, s)
            )
        ]
    ),
    Cell(
        idx=1,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty(4, s) and _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(4, s) and _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty(4, s) and _empty(7, s) and _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(4, s) and _empty(7, s) and _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty(4, s) and _empty(7, s) and _empty(10, s)
                and _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(4, s) and _empty(7, s) and _empty(10, s)
                and _empty(11, s)
            )
        ]
    ),
    Cell(
        idx=2,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: _empty(4, s)
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: _empty(4, s) and _empty(7, s)
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(4, s) and _empty(7, s) and _empty(10, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(4, s) and _empty(7, s) and _empty(10, s) and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=3,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(2, s) and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(2, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: _empty(2, s)
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: _empty(2, s) and _empty(4, s)
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: _empty(2, s) and _empty(4, s) and _empty(7, s)
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(2, s) and _empty(4, s) and _empty(7, s) and _empty(10, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(2, s) and _empty(4, s) and _empty(7, s) and _empty(10, s)
                and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=4,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty(7, s) and _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(7, s) and _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty(7, s) and _empty(10, s) and _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(7, s) and _empty(10, s) and _empty(11, s)
            )
        ]
    ),
    Cell(
        idx=5,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(4, s) and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(4, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: _empty(7, s)
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(7, s) and _empty(10, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(7, s) and _empty(10, s) and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=6,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(5, s) and _empty(4, s) and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(5, s) and _empty(4, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: _empty(5, s)
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: _empty(5, s)
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: _empty(5, s) and _empty(7, s)
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(5, s) and _empty(7, s) and _empty(10, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(5, s) and _empty(7, s) and _empty(10, s) and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=7,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty(4, s) and _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(4, s) and _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty(10, s) and _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(10, s) and _empty(11, s)
            )
        ]
    ),
    Cell(
        idx=8,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(7, s) and _empty(4, s) and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(7, s) and _empty(4, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: _empty(7, s)
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(10, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(10, s) and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=9,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(8, s) and _empty(7, s) and _empty(4, s) and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(8, s) and _empty(7, s) and _empty(4, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: _empty(8, s) and _empty(7, s)
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: _empty(8, s)
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: _empty(8, s)
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(8, s) and _empty(10, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(8, s) and _empty(10, s) and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=10,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty(7, s) and _empty(4, s) and _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(7, s) and _empty(4, s) and _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty(7, s) and _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(7, s) and _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(11, s)
            )
        ]
    ),
    Cell(
        idx=11,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(10, s) and _empty(7, s) and _empty(4, s) and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(10, s) and _empty(7, s) and _empty(4, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: _empty(10, s) and _empty(7, s)
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: _empty(10, s)
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: True
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=12,
        neighbors=[
            Neighbor(
                destination=0,
                condition=lambda a, s: _empty(11, s) and _empty(10, s) and _empty(7, s) and _empty(4, s)
                and _empty(1, s)
            ),
            Neighbor(
                destination=1,
                condition=lambda a, s: _empty(11, s) and _empty(10, s) and _empty(7, s) and _empty(4, s)
            ),
            Neighbor(
                destination=4,
                condition=lambda a, s: _empty(11, s) and _empty(10, s) and _empty(7, s)
            ),
            Neighbor(
                destination=7,
                condition=lambda a, s: _empty(11, s) and _empty(10, s)
            ),
            Neighbor(
                destination=10,
                condition=lambda a, s: _empty(11, s)
            ),
            Neighbor(
                destination=13,
                condition=lambda a, s: _empty(11, s)
            ),
            Neighbor(
                destination=14,
                condition=lambda a, s: _empty(11, s) and _empty(13, s)
            ),
        ]
    ),
    Cell(
        idx=13,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty(10, s) and _empty(7, s) and _empty(4, s) and _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(10, s) and _empty(7, s) and _empty(4, s) and _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty(10, s) and _empty(7, s) and _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(10, s) and _empty(7, s) and _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty(10, s) and _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(10, s) and _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(11, s)
            )
        ]
    ),
    Cell(
        idx=14,
        neighbors=[
            Neighbor(
                destination=2,
                condition=lambda a, s: _empty(13, s) and _empty(10, s) and _empty(7, s) and _empty(4, s)
                and _empty_or_same(3, a, s)
            ),
            Neighbor(
                destination=3,
                condition=lambda a, s: _empty(13, s) and _empty(10, s) and _empty(7, s) and _empty(4, s)
                and _empty(2, s)
            ),
            Neighbor(
                destination=5,
                condition=lambda a, s: _empty(13, s) and _empty(10, s) and _empty(7, s) and _empty_or_same(6, a, s)
            ),
            Neighbor(
                destination=6,
                condition=lambda a, s: _empty(13, s) and _empty(10, s) and _empty(7, s) and _empty(5, s)
            ),
            Neighbor(
                destination=8,
                condition=lambda a, s: _empty(13, s) and _empty(10, s) and _empty_or_same(9, a, s)
            ),
            Neighbor(
                destination=9,
                condition=lambda a, s: _empty(13, s) and _empty(10, s) and _empty(8, s)
            ),
            Neighbor(
                destination=11,
                condition=lambda a, s: _empty(13, s) and _empty_or_same(12, a, s)
            ),
            Neighbor(
                destination=12,
                condition=lambda a, s: _empty(13, s) and _empty(11, s)
            )
        ]
    )
]


def _neighbors_for_cell(cell_idx: int, amphipod: str, state: State) -> List[int]:
    cell = CELLS[cell_idx]

    return [
        neighbor.destination
        for neighbor in cell.neighbors
        if _empty(neighbor.destination, state) and neighbor.condition(amphipod, state)
    ]


def _possible_next_states(state: State) -> Dict[State, int]:
    next_states: Dict[State, int] = {}
    for cell_idx, amphipod in enumerate(state):
        if amphipod:
            neighbors = _neighbors_for_cell(cell_idx, amphipod, state)
            for neighbor in neighbors:
                next_state = _move_amphipod(amphipod, cell_idx, neighbor, state)
                cost = STEPS[cell_idx][neighbor] * WEIGHTS[amphipod]
                _merge(next_state, cost, next_states)

    # print("............START possible next state....")
    # for state_tmp, cost in next_states.items():
    #     print(f"\npossible state with cost: {cost}\n{serialize_state(state_tmp)}\n")
    # print("............END possible next state....")

    return next_states


def _merge(state: State, cost: int, states: Dict[State, int]) -> None:
    existing = states.get(state)
    if existing:
        cost = min(existing, cost)

    states[state] = cost


def _move_amphipod(amphipod: str, cell_from: int, cell_to: int, state: State) -> State:
    if cell_from < cell_to:
        first = cell_from
        second = cell_to
        first_value = None
        second_value = amphipod
    else:
        first = cell_to
        second = cell_from
        first_value = amphipod
        second_value = None

    return state[:first] + (first_value, ) + state[first + 1:second] + (second_value, ) + state[second + 1:]


def _is_done(state: State) -> bool:
    return state == DONE_STATE


HEURISTIC_GOAL = {
    2: "A",
    3: "A",
    5: "B",
    6: "B",
    8: "C",
    9: "C",
    11: "D",
    12: "D"
}

DESTINATIONS: Dict[str, Tuple[int, ...]] = {
    "A": (2, 3),
    "B": (5, 6),
    "C": (8, 9),
    "D": (11, 12),
}

MAX_WEIGHT = max(WEIGHTS.values())


def _heuristic(state: State) -> int:
    score = 0
    for cell, expected in HEURISTIC_GOAL.items():
        if state[cell] == expected:
            score += 1

    # return ((len(HEURISTIC_GOAL) - score) * 3 * MAX_WEIGHT) + _sum_distances(state)
    return _sum_distances(state)


def _sum_distances(state: State) -> int:
    distance = 0
    for cell_idx, amphipod in enumerate(state):
        if amphipod is None:
            continue

        if cell_idx not in DESTINATIONS[amphipod]:
            first_target = DESTINATIONS[amphipod][0]
            distance += STEPS[cell_idx][first_target] * WEIGHTS[amphipod]

    return distance


def organize(state: State, done_state: State = DONE_STATE) -> int:
    frontier = PriorityQueue()
    frontier.push(state, 0)
    came_from: Dict[State, Optional[State]] = {
        state: None
    }
    cost_so_far: Dict[State, int] = {
        state: 0
    }
    while frontier.length() > 0:
        current: State = frontier.pop()

        if current == done_state:
            break

        # print(f"\nCurrent is:\n{serialize_state(current)}\n")

        next_states = _possible_next_states(current)
        for next_state, cost in next_states.items():
            new_cost = cost_so_far[current] + cost
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + _heuristic(next_state)

                # print(f"\npush in frontier with priority {priority}: \n{serialize_state(next_state)}\n")

                frontier.push(next_state, priority)
                came_from[next_state] = current

    DEBUG and _print_path(state, done_state, came_from)

    return cost_so_far[done_state]


def _print_path(start: State, end: State, came_from: Dict[State, Optional[State]]) -> None:
    print("\n========Winning path=========")
    path = [end]
    current = end
    while current != start:
        current = came_from[current]
        path.append(current)

    for segment in reversed(path):
        print(f"\n{serialize_state(segment)}\n")


def serialize_state(state: State) -> str:
    return f"""#############
#{_ser(state[0])}{_ser(state[1])}.{_ser(state[4])}.{_ser(state[7])}.{_ser(state[10])}.{_ser(state[13])}{_ser(state[14])}#
###{_ser(state[2])}#{_ser(state[5])}#{_ser(state[8])}#{_ser(state[11])}###
  #{_ser(state[3])}#{_ser(state[6])}#{_ser(state[9])}#{_ser(state[12])}#
  #########
"""


def _ser(val: Optional[str]) -> str:
    return val if val else "."
