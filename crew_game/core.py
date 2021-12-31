import random
from dataclasses import dataclass

from termcolor import colored

NUM_GOALS = 9
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

    def cli(self):
        card = colored(
            f"  {self.value}  ", "white", "on_" + SUITS[self.suit], attrs=["bold"]
        )
        return (f"({self.order}) " if self.order else "    ") + card

    def __str__(self):
        card = colored(
            f"  {self.value}  ", "white", "on_" + SUITS[self.suit], attrs=["bold"]
        )
        return (f"({self.order}) " if self.order else "") + card


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
        value = random.randint(1, NUM_GOALS)
        order = len(sampled_goals) + 1 if len(sampled_goals) < ordered_count else 0
        candidate = Goal(value, suit, order)
        if not contains(candidate, sampled_goals):
            sampled_goals.append(candidate)
    return sampled_goals


def display_goals(num_goals, ordered_count=0, num_players=4):
    max_suits = active_suits(num_players)
    sampled_goals = sample_goals(num_goals, max_suits, ordered_count)
    for goal in sampled_goals:
        print(goal.cli())
