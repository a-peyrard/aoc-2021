"""
--- Day 17: Trick Shot ---

You finally decode the Elves' message. HI, the message says. You continue searching for the sleigh keys.
Ahead of you is what appears to be a large ocean trench. Could the keys have fallen into it? You'd better send a probe
to investigate.
The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or
downward if negative) directions. For example, an initial x,y velocity like 0,10 would fire the probe straight up, while
 an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.
The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these
changes occur in the following order:

    The probe's x position increases by its x velocity.
    The probe's y position increases by its y velocity.
    Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater
    than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
    Due to gravity, the probe's y velocity decreases by 1.

For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within
a target area after any step. The submarine computer has already calculated this target area (your puzzle input). For
example:
target area: x=20..30, y=-10..-5
This target area means that you need to find initial x,y velocity values such that after any step, the probe's x
position is at least 20 and at most 30, and the probe's y position is at least -10 and at most -5.
Given this target area, one initial velocity that causes the probe to be within the target area after any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate increases to the right, and the y coordinate
increases upward. In the bottom right, positions that are within the target area are shown as T. After each step (until
the target area is reached), the position of the probe is marked with #. (The bottom-right # is both a position the
probe reaches and a position in the target area.)
Another initial velocity that causes the probe to be within the target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

One initial velocity that doesn't cause the probe to be within the target area after any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#

The probe appears to pass through the target area, but is never within it after any step. Instead, it continues down
and to the right - only the first few steps are shown.
If you're going to fire a highly scientific probe out of a super cool probe launcher, you might as well do it with
style. How high can you make the probe go while still reaching the target area?
In the above example, using an initial velocity of 6,9 is the best you can do, causing the probe to reach a maximum y
position of 45. (Any higher initial y velocity causes the probe to overshoot the target area entirely.)
Find the initial velocity that causes the probe to reach the highest y position and still eventually be within the
target area after any step. What is the highest y position it reaches on this trajectory?

"""
from typing import Tuple, List

from aoc.util.matrix import initialize_matrix


def launch_probe(target: Tuple[int, int, int, int]) -> int:
    velocity = _find_highest_y_velocity(target)
    return int((velocity[1] * (velocity[1] + 1)) / 2)


def _find_highest_y_velocity(target: Tuple[int, int, int, int]) -> Tuple[int, int]:
    xi, xa, yi, ya = target

    step_min = -1
    step_max = -1
    val = 0
    step = 0
    while val <= xa:
        if val >= xi:
            if step_min == -1:
                step_min = step
            step_max = step
        step += 1
        val += step

    # for the y, we target to fall straight, the y velocity will be equals
    # to -initial_y velocity when arriving to 0, and then our best case is to have
    # -initial_y - 1 to be inside the target. The last line of the target being the better,
    # so let's go with: initial_y = (-1 * yi) - 1

    return step_min, (-1 * yi) - 1


def count_number_of_solutions(target: Tuple[int, int, int, int]) -> int:
    """
    - we have one solution per target cell
    - then we now the min x_velocity, we can compute the range for y_velocity based on first solution
    - finally we can compute all missing solution between those two extreme cases, by creating
    an algo playing the probe, we don't have so many step every time, so we can afford
    to run a lot of samples
    """

    xi, xa, yi, ya = target

    height = ya - yi + 1
    width = xa - xi + 1

    number_of_direct_solutions = height * width

    min_x, max_y = _find_highest_y_velocity(target)
    max_x, min_y = int(xa / 2) + 1, ya + 1

    successful_launches = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            velocity = (x, y)
            if simulate_launch(velocity, target):
                successful_launches += 1

    return number_of_direct_solutions + successful_launches


def simulate_launch(velocity: Tuple[int, int],
                    target: Tuple[int, int, int, int],
                    generate_image: bool = False) -> bool:

    x_velocity, y_velocity = velocity
    x, y = 0, 0
    xi, xa, yi, ya = target

    if generate_image:
        image_max_y = 0
        image_min_y = yi
        image_min_x = 0
        image_max_x = xa
        if y_velocity > 0:
            image_max_y = int((y_velocity * (y_velocity + 1)) / 2)
        image_width = image_max_x - image_min_x + 1
        image_height = image_max_y - image_min_y + 1
        image = initialize_matrix(".", image_height, image_width)
        _draw_on_image(0, 0, "S", image, image_max_y)
        for tx in range(xi, xa + 1):
            for ty in range(yi, ya + 1):
                _draw_on_image(tx, ty, "T", image, image_max_y)

    while x <= xa and y >= yi:
        x += x_velocity
        y += y_velocity
        generate_image and _draw_on_image(x, y, "#", image, image_max_y)
        if xi <= x <= xa and yi <= y <= ya:
            generate_image and print(f"\nimage success launch {velocity}: \n{_print_image(image)}")
            return True

        if x_velocity:
            x_velocity -= 1
        y_velocity -= 1

    generate_image and print(f"\nimage fail launch {velocity}: \n{_print_image(image)}")
    return False


def _translate_coord(px: int, py: int, image_max_y: int) -> Tuple[int, int]:
    return px, image_max_y - py


def _draw_on_image(x: int, y: int, char: str, image: List[List[str]], image_max_y: int):
    x, y = _translate_coord(x, y, image_max_y)
    if x >= len(image[0]) or y >= len(image):
        _increase_image_size(x, y, image)

    image[y][x] = char


def _print_image(image: List[List[str]]) -> str:
    return "\n".join((
        "".join(row)
        for row in image
    ))


def _increase_image_size(x: int, y: int, image: List[List[str]]):
    height = len(image) - 1
    width = len(image[0]) - 1
    missing_rows = y - height
    missing_cols = x - width
    if missing_cols > 0:
        for row in image:
            row.extend(["."] * missing_cols)
        width += missing_cols
    if missing_rows > 0:
        for _ in range(missing_rows):
            image.append(["."] * width)
