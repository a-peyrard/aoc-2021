"""
--- Day 21: Dirac Dice ---

There's not much to do as you slowly descend to the bottom of the ocean. The submarine computer challenges you to a nice
 game of Dirac Dice.
This game consists of a single die, two pawns, and a game board with a circular track containing ten spaces marked 1
through 10 clockwise. Each player's starting space is chosen randomly (your puzzle input). Player 1 goes first.
Players take turns moving. On each player's turn, the player rolls the die three times and adds up the results. Then,
the player moves their pawn that many times forward around the track (that is, moving clockwise on spaces in order of
increasing value, wrapping back around to 1 after 10). So, if a player is on space 7 and they roll 2, 2, and 1, they
would move forward 5 times, to spaces 8, 9, 10, 1, and finally stopping on 2.
After each player moves, they increase their score by the value of the space their pawn stopped on. Players' scores
start at 0. So, if the first player starts on space 7 and rolls a total of 5, they would stop on space 2 and add 2 to
their score (for a total score of 2). The game immediately ends as a win for any player whose score reaches at least
1000.
Since the first game is a practice game, the submarine opens a compartment labeled deterministic dice and a 100-sided
die falls out. This die always rolls 1 first, then 2, then 3, and so on up to 100, after which it starts over at 1
again. Play using this die.

For example, given these starting positions:

Player 1 starting position: 4
Player 2 starting position: 8

This is how the game would go:

    Player 1 rolls 1+2+3 and moves to space 10 for a total score of 10.
    Player 2 rolls 4+5+6 and moves to space 3 for a total score of 3.
    Player 1 rolls 7+8+9 and moves to space 4 for a total score of 14.
    Player 2 rolls 10+11+12 and moves to space 6 for a total score of 9.
    Player 1 rolls 13+14+15 and moves to space 6 for a total score of 20.
    Player 2 rolls 16+17+18 and moves to space 7 for a total score of 16.
    Player 1 rolls 19+20+21 and moves to space 6 for a total score of 26.
    Player 2 rolls 22+23+24 and moves to space 6 for a total score of 22.

...after many turns...

    Player 2 rolls 82+83+84 and moves to space 6 for a total score of 742.
    Player 1 rolls 85+86+87 and moves to space 4 for a total score of 990.
    Player 2 rolls 88+89+90 and moves to space 3 for a total score of 745.
    Player 1 rolls 91+92+93 and moves to space 10 for a final score, 1000.

Since player 1 has at least 1000 points, player 1 wins and the game ends. At this point, the losing player had 745
points and the die had been rolled a total of 993 times; 745 * 993 = 739785.
Play a practice game using the deterministic 100-sided die. The moment either player wins, what do you get if you
multiply the score of the losing player by the number of times the die was rolled during the game?

--- Part Two ---

Now that you're warmed up, it's time to play the real game.
A second compartment opens, this time labeled Dirac dice. Out of it falls a single three-sided die.
As you experiment with the die, you feel a little strange. An informational brochure in the compartment explains that
this is a quantum die: when you roll it, the universe splits into multiple copies, one copy for each possible outcome of
 the die. In this case, rolling the die always splits the universe into three copies: one where the outcome of the roll
 was 1, one where it was 2, and one where it was 3.
The game is played the same as before, although to prevent things from getting too far out of hand, the game now ends
when either player's score reaches at least 21.
Using the same starting positions as in the example above, player 1 wins in 444356092776315 universes, while player 2
merely wins in 341960390180808 universes.
Using your given starting positions, determine every possible outcome. Find the player that wins in more universes; in
how many universes does that player win?


"""
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Tuple, NamedTuple, Dict, Optional


class Dice(ABC):
    @abstractmethod
    def roll(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def number_of_rolls(self) -> int:
        raise NotImplementedError()


class Deterministic100SidesDice(Dice):
    def __init__(self):
        self._count = 0

    def roll(self) -> int:
        self._count += 1
        return ((self._count - 1) % 100) + 1

    @property
    def number_of_rolls(self) -> int:
        return self._count


def play(player_1: int, player_2: int, dice: Dice, winning_score: int) -> Tuple[int, int]:
    scores = [0, 0]
    positions = [player_1, player_2]
    turn = 0
    while max(scores) < winning_score:
        player = turn % 2
        draw = sum((
            dice.roll()
            for _ in range(3)
        ))
        positions[player] = ((positions[player] + draw - 1) % 10) + 1
        scores[player] += positions[player]

        turn += 1

    return scores[0], scores[1]


def solution_1(player_1: int, player_2: int) -> int:
    dice = Deterministic100SidesDice()
    player_1_score, player_2_score = play(player_1, player_2, dice, winning_score=1000)
    loser_score = min(player_1_score, player_2_score)

    return loser_score * dice.number_of_rolls


class Game(NamedTuple):
    player_1_pos: int
    player_2_pos: int
    player_1_score: int = 0
    player_2_score: int = 0
    player_1_turn: bool = True


ROLLS = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]


def solution_2(player_1: int, player_2: int) -> Tuple[int, int]:
    wins = [0, 0]
    games = defaultdict(int)
    games[Game(
        player_1_pos=player_1,
        player_2_pos=player_2
    )] = 1
    while len(games) > 0:
        new_games: Dict[Game, int] = defaultdict(int)
        for game, occurrences in games.items():
            for draw, frequency in ROLLS:
                new_game = _update_game(game, draw)
                winner = _get_winner_index(new_game)
                if winner is not None:
                    wins[winner] += occurrences * frequency
                else:
                    _merge(new_games, new_game, occurrences * frequency)
        games = new_games

    return wins[0], wins[1]


def _update_game(game: Game, draw: int) -> Game:
    if game.player_1_turn:
        new_position = _update_position(game.player_1_pos, draw)
        return Game(
            player_1_pos=new_position,
            player_2_pos=game.player_2_pos,
            player_1_score=game.player_1_score + new_position,
            player_2_score=game.player_2_score,
            player_1_turn=False
        )
    else:
        new_position = _update_position(game.player_2_pos, draw)
        return Game(
            player_1_pos=game.player_1_pos,
            player_2_pos=new_position,
            player_1_score=game.player_1_score,
            player_2_score=game.player_2_score + new_position,
            player_1_turn=True
        )


def _update_position(position: int, draw: int) -> int:
    return ((position + draw - 1) % 10) + 1


def _merge(games: Dict[Game, int], game: Game, occurrences: int):
    games[game] += occurrences


def _get_winner_index(game: Game) -> Optional[int]:
    if game.player_1_score >= 21:
        return 0
    if game.player_2_score >= 21:
        return 1

    return None
