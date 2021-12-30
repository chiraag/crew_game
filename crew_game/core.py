import os
import random
from dataclasses import dataclass

import tabulate
from termcolor import colored

NUM_GOALS = 9
MAX_SUITS = 4
SUITS = ["magenta", "yellow", "blue", "green"]


@dataclass(frozen=True)
class Goal:
    value: int
    suit: int
    order: int

    def caption(self):
        attr = SUITS[self.suit] + "_goal"
        return [
            f"({self.order}) " if self.order else "",
            (attr, f"  {self.value}  "),
        ]

    def caption_length(self):
        return len((f"({self.order}) " if self.order else "") + f"  {self.value}  ")

    def __str__(self):
        card = colored(
            f"  {self.value}  ", "white", "on_" + SUITS[self.suit], attrs=["bold"]
        )
        return (f"({self.order}) " if self.order else "") + card


def tabulate_goals(sampled_goals, filter_list=None):
    if filter_list is None:
        filter_list = [True for _ in sampled_goals]

    header = ["id", "Goal"]
    table = []
    for idx, goal in enumerate(sampled_goals):
        table.append([f"{idx:2d}", str(goal)])
    return header, table


def tabulate_picked(picked_goals):
    header = [f"Player {idx}" for idx, _ in enumerate(picked_goals)]
    table = []
    max_rows = max([len(player_goals) for player_goals in picked_goals])
    for row_idx in range(max_rows):
        table.append(
            [
                str(player_goals[row_idx]) if row_idx < len(player_goals) else ""
                for player_goals in picked_goals
            ]
        )
    return header, table


def fmt_table(header, table):
    return tabulate.tabulate(table, header, stralign="right", tablefmt="fancy_grid")


def active_suits(num_players):
    if num_players == 3:
        return 3
    elif num_players in [4, 5]:
        return 4
    else:
        raise ValueError("Cannot play with %d players" % num_players)


def contains(goal, goal_list):
    for tgt in goal_list:
        if tgt.value == goal.value and tgt.suit == goal.suit:
            return True
    return False


def sample_goals(num_goals, max_suits, ordered_count):
    # rejection sample all goals
    sampled_goals = []
    while len(sampled_goals) < num_goals:
        suit = random.randint(0, max_suits - 1)
        value = random.randint(1, 9)
        order = len(sampled_goals) + 1 if len(sampled_goals) < ordered_count else 0
        candidate = Goal(value, suit, order)
        if not contains(candidate, sampled_goals):
            sampled_goals.append(candidate)
    return sampled_goals


def pick_captain(num_players):
    while True:
        try:
            captain = 0  # int(input("Enter captain: "))
            assert 0 <= captain < num_players
            return captain
        except:
            print("Validataion error, try again")


def print_picked_goals(picked_goals):
    print(picked_goals)


def pick_goal(player, candidates):
    print()
    while True:
        try:
            goal_idx = int(input(f"Player {player}, Pick goal by id: "))
            assert 0 <= goal_idx < len(candidates)
            return (
                candidates[goal_idx],
                [goal for idx, goal in enumerate(candidates) if idx != goal_idx],
            )
        except:
            print("Validataion error, try again")


def print_screen(picked_goals, sampled_goals, ordered_count, num_players, final=False):
    os.system("clear")
    print("Picked Goals:")
    header, table = tabulate_picked(picked_goals)
    print(fmt_table(header, table))
    print()

    if not final:
        print("Available Goals:")
        header, table = tabulate_goals(sampled_goals)
        print(fmt_table(header, table))


def pick_loop(captain, sampled_goals, ordered_count, num_players):
    picked_goals = [[] for _ in range(num_players)]
    candidates = [goal for goal in sampled_goals]

    player = captain
    while candidates:
        print_screen(picked_goals, candidates, ordered_count, num_players, False)
        goal, candidates = pick_goal(player, candidates)
        picked_goals[player].append(goal)
        player = (player + 1) % num_players
    return picked_goals


def main(num_goals, ordered_count=0, num_players=4):
    max_suits = active_suits(num_players)

    sampled_goals = sample_goals(num_goals, max_suits, ordered_count)
    header, table = tabulate_goals(sampled_goals)
    print(fmt_table(header, table))

    captain = pick_captain(num_players)
    picked_goals = pick_loop(captain, sampled_goals, ordered_count, num_players)

    print_screen(picked_goals, sampled_goals, ordered_count, num_players, True)


if __name__ == "__main__":
    args = {
        "num_players": 4,
        "num_goals": 5,
        "ordered_count": 2,
    }

    main(**args)
