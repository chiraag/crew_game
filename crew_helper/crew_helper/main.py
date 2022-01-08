import argparse

from crew_game import core, ui


def input_validation(args):
    if not 3 <= args.nplayers <= 5:
        print("Only 3 to 5 players are allowed")
        exit(2)

    if not 0 < args.goals <= 9:
        print("Goals must be from 1 to 9")
        exit(2)

    if not 0 <= args.ordered <= args.goals:
        print("Ordered goals must be from 0 to #goals")
        exit(2)


def main():
    parser = argparse.ArgumentParser("crew_helper")
    parser.add_argument("-g", "--goals", type=int, help="Number of goals")
    parser.add_argument(
        "-o", "--ordered", type=int, default=0, help="Ordered goals (default: 0)"
    )
    parser.add_argument(
        "-n", "--nplayers", type=int, default=4, help="Ordered goals (default: 4)"
    )
    args = parser.parse_args()

    if args.goals is None:
        ui.main()
    else:
        input_validation(args)
        core.display_goals(args.goals, args.ordered, args.nplayers)


if __name__ == "__main__":
    main()
