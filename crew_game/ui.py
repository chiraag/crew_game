import string

import urwid

from crew_game import core


class FixedNumericEdit(urwid.Edit):
    def __init__(
        self,
        caption="",
        edit_text="",
        width=1,
    ):

        self.max_width = width

        super().__init__(
            caption=caption,
            edit_text=edit_text,
        )

    def keypress(self, size, key):
        rc = super().keypress(size, key)
        if len(self.edit_text) > self.max_width:
            self.edit_text = self.edit_text[0 : self.max_width]
        else:
            urwid.emit_signal(self, "change")
        return rc

    def valid_char(self, ch):
        if len(self.edit_text) == self.max_width:
            return False
        else:
            return True if ch in string.digits else False


palette = [
    ("magenta_goal", "white,bold", "dark magenta"),
    ("yellow_goal", "white,bold", "brown"),
    ("blue_goal", "white,bold", "dark blue"),
    ("green_goal", "white,bold", "dark green"),
    ("green", "dark green,standout", ""),
    ("red", "dark red,standout", ""),
    ("reversed", "standout", ""),
]


class ActionButton(urwid.Button):
    def __init__(self, caption, callback):
        self._caption = " " + caption + " "

        super().__init__("")
        urwid.connect_signal(self, "click", callback)

        self.icon = urwid.SelectableIcon(
            ("green", self._caption), len(self._caption) + 1
        )
        self.icon.align = "center"
        self._w = urwid.AttrMap(self.icon, None, focus_map="reversed")

    def set_text(self, valid=True):
        self.icon.set_text((("green" if valid else "red"), self._caption))


class Settings(urwid.WidgetWrap):
    def __init__(self, callback):
        self.num_players = 4
        self.captain = 1
        self.num_goals = 5
        self.ordered_count = 2

        self.column_list = [
            FixedNumericEdit("# Players: ", "4"),
            FixedNumericEdit("Captain: ", "1"),
            FixedNumericEdit("Goals: ", "5"),
            FixedNumericEdit("Ordered Goals: ", "2"),
        ]

        self.randomize_button = ActionButton("New Game", lambda button: callback())

        panel = urwid.LineBox(
            urwid.Pile(
                [
                    urwid.Columns(self.column_list),
                    urwid.Divider(),
                    self.randomize_button,
                ]
            ),
            "Game Settings",
        )

        for edit_widget in self.column_list:
            urwid.connect_signal(edit_widget, "postchange", self.update)

        super().__init__(panel)

    def update(self, before, after):
        self.num_players = int("0" + self.column_list[0].edit_text)
        self.captain = int("0" + self.column_list[1].edit_text)
        self.num_goals = int("0" + self.column_list[2].edit_text)
        self.ordered_count = int("0" + self.column_list[3].edit_text)

        self.randomize_button.set_text(self.validate())

    def validate(self):
        valid_players = 3 <= self.num_players <= 5
        valid_captain = 0 < self.captain <= 4
        valid_ordered = self.ordered_count <= self.num_goals
        return valid_players and valid_captain and valid_ordered


class PickedGoals(urwid.WidgetWrap):
    def __init__(self, num_players):
        self.curr_player = 0
        self.picked_goals = [[] for _ in range(num_players)]
        self.panel = urwid.Columns(
            [self.get_column(idx) for idx, goals in enumerate(self.picked_goals)]
        )
        super().__init__(self.panel)

    def delete_goal(self, goal):
        for player, goals in enumerate(self.picked_goals):
            if goal in goals:
                idx = goals.index(goal)
                del goals[idx]
                self.panel.contents[player] = (
                    self.get_column(player),
                    self.panel.options(),
                )

    def clear(self, num_players, captain):
        self.curr_player = captain - 1
        self.picked_goals = [[] for _ in range(num_players)]
        for idx in range(num_players):
            self.panel.contents[idx] = (self.get_column(idx), self.panel.options())

    def get_column(self, idx):
        return urwid.LineBox(
            urwid.BoxAdapter(
                urwid.ListBox(
                    urwid.SimpleFocusListWalker(
                        [
                            GoalButton(goal, self.delete_goal)
                            for goal in self.picked_goals[idx]
                        ]
                    )
                ),
                height=4,
            ),
            f"Player {idx+1}",
            title_attr=("reversed" if idx == self.curr_player else None),
        )

    def pick_goal(self, goal):
        curr_idx = self.curr_player
        nxt_idx = (curr_idx + 1) % len(self.panel.contents)

        if goal is not None:
            self.picked_goals[curr_idx].append(goal)
        self.curr_player = nxt_idx

        for idx in [curr_idx, nxt_idx]:
            self.panel.contents[idx] = (self.get_column(idx), self.panel.options())


def get_attr(suit):
    suits = ["magenta", "yellow", "blue", "green"]
    return suits[suit] + "_goal"


class SkipButton(urwid.Button):
    def __init__(self, callback):
        super().__init__("")
        urwid.connect_signal(self, "click", lambda button: callback(None))

        self.icon = urwid.SelectableIcon("Skip", 5)
        self.icon.align = "center"
        self._w = urwid.AttrMap(self.icon, None, focus_map="reversed")


class GoalButton(urwid.Button):
    def __init__(self, goal, callback):
        super().__init__("")
        urwid.connect_signal(self, "click", lambda button: callback(goal))

        self.icon = urwid.SelectableIcon(goal.caption(), goal.caption_length() + 1)
        self.icon.align = "center"
        self._w = urwid.AttrMap(self.icon, None, focus_map="reversed")


class SampledGoals(urwid.WidgetWrap):
    def __init__(self, callback):
        self.goal_list = []
        self.ext_callback = callback
        self.box = urwid.Columns(self.widget_list(), min_width=20)
        self.panel = urwid.LineBox(
            self.box,
            f"Pending Goals",
        )

        super().__init__(self.panel)

    def select_callback(self, goal):
        self.ext_callback(goal)
        if goal is not None:
            del self.goal_list[self.box.focus_position - 1]
            del self.box.contents[self.box.focus_position]

    def widget_list(self):
        return [SkipButton(self.select_callback)] + [
            GoalButton(goal, self.select_callback) for goal in self.goal_list
        ]

    def update_goals(self, goal_list):
        self.goal_list = goal_list
        self.box.contents = [(w, self.box.options()) for w in self.widget_list()]


class Game:
    def __init__(self):
        self.settings = Settings(self.sample_goals)
        self.picked_goals = PickedGoals(self.settings.num_players)
        self.sampled_goals = SampledGoals(self.picked_goals.pick_goal)

        self.window = urwid.LineBox(
            urwid.Filler(
                urwid.Pile([self.picked_goals, self.sampled_goals, self.settings])
            ),
            "Crew Helper",
        )

    def sample_goals(self):
        max_suits = core.active_suits(self.settings.num_players)
        sampled_goals = core.sample_goals(
            self.settings.num_goals, max_suits, self.settings.ordered_count
        )
        self.sampled_goals.update_goals(sampled_goals)
        self.picked_goals.clear(self.settings.num_players, self.settings.captain)

    def exit_window(self, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()


def main():
    game = Game()
    urwid.MainLoop(game.window, palette=palette, unhandled_input=game.exit_window).run()


if __name__ == "__main__":
    main()
