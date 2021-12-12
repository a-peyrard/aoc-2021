"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave
anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to
find all of them.
Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle
input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the
cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
   \\    /
     end

Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than
 once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase,
 like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it
 might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can
 visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they
are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice
(once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not
allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?

"""
from collections import defaultdict
from typing import Tuple, List, Dict, Set


DEBUG = False


class Path:
    @staticmethod
    def initialize(initial: str) -> "Path":
        return Path(["start", initial])

    def __init__(self, path: List[str]):
        self._path = path
        self._seen = set(path)
        self._current = path[-1]

    def push(self, vertex: str) -> "Path":
        new = Path(list(self._path))
        new._path.append(vertex)
        new._seen.add(vertex)
        new._current = vertex
        return new

    @property
    def path(self) -> List[str]:
        return self._path

    @property
    def seen(self) -> Set[str]:
        return self._seen

    @property
    def current(self) -> str:
        return self._current

    @property
    def finished(self) -> bool:
        return self._current == "end"

    def __repr__(self):
        return str(self._path)


def count_paths(edges: List[Tuple[str, str]]):
    adjacency_list = _build_adjacency_list(edges)

    paths_queue: List[Path] = [
        Path.initialize(successor)
        for successor in adjacency_list["start"]
    ]
    paths: List[Path] = []
    while len(paths_queue) > 0:
        path = paths_queue.pop(0)
        for successor in adjacency_list[path.current]:
            if successor.isupper() or successor not in path.seen:
                new_path = path.push(successor)
                if new_path.finished:
                    paths.append(new_path)
                else:
                    paths_queue.append(new_path)

    DEBUG and _print_paths(paths)
    return len(paths)


def _build_adjacency_list(edges: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    adjacency_list = defaultdict(list)
    for from_vertex, to_vertex in edges:
        adjacency_list[from_vertex].append(to_vertex)
        adjacency_list[to_vertex].append(from_vertex)

    return adjacency_list


def _print_paths(paths: List[Path]):
    print(f'\nAll paths found ({len(paths)}): \n')
    for path in paths:
        print(path.path)
