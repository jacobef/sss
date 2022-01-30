import unittest
from enum import Enum, auto
from random import randint
from typing import Callable, Any

from directions import Direction
from player import Player


class NumChange(Enum):
    INCREASE = auto()
    DECREASE = auto()
    STAY = auto()


class SSSTest(unittest.TestCase):
    def assertChanges(self,
                      change_things: Callable[[], Any],
                      get_things: Callable[[], list[int]],
                      expected_net_changes: list[int],
                      messages: list[str]):
        things_before_change = get_things()
        change_things()
        things_after_change = get_things()
        for (thing_before_change, thing_after_change, expected_net_change, message) \
                in zip(things_before_change, things_after_change, expected_net_changes, messages):
            self.assertEqual(thing_after_change, thing_before_change + expected_net_change, message)


class TestPlayer(SSSTest):

    # If you're reading this trying to understand it, skip assertMovement and go to test_move_squares.
    # It will be much easier to understand that way.
    def assertMovement(self, direction: Direction,
                       x_expected_change: NumChange, y_expected_change: NumChange):
        player = Player(0, 0, 0, 0, "Test Name")
        num_squares_to_move: int = randint(-10 ** 10, 10 ** 10)

        # I am aware this copy-pasted code is a bit of un momento de bruh but idk how to fix it
        match x_expected_change:
            case NumChange.STAY:
                expected_dx: int = 0
                expected_x_effect: str = "not change x_square"
            case NumChange.DECREASE:
                expected_dx: int = -num_squares_to_move
                expected_x_effect: str = "decrease x_square by N, where N is the number of squares moved"
            case NumChange.INCREASE:
                expected_dx: int = num_squares_to_move
                expected_x_effect: str = "increase x_square by N, where N is the number of squares moved"
            case _:
                raise TypeError("x_expected_change must be a NumChange enum")
        match y_expected_change:
            case NumChange.STAY:
                expected_dy: int = 0
                expected_y_effect: str = "not change y_square"
            case NumChange.DECREASE:
                expected_dy: int = -num_squares_to_move
                expected_y_effect: str = "decrease y_square by N, where N is the number of squares moved"
            case NumChange.INCREASE:
                expected_dy: int = num_squares_to_move
                expected_y_effect: str = "increase y_square by N, where N is the number of squares moved"
            case _:
                raise TypeError("y_expected_change must be a NumChange enum")

        self.assertChanges(
            change_things=lambda: player.move_squares(direction, num_squares_to_move),
            get_things=lambda: [player.x_square, player.y_square],
            expected_net_changes=[expected_dx, expected_dy],
            messages=[f"Moving {direction.name.lower()} should {expected_x_effect}",
                      f"Moving {direction.name.lower()} should {expected_y_effect}"]
        )

    def test_move_squares(self):
        for i in range(0, 100):
            self.once_test_move_squares()

    def once_test_move_squares(self):
        self.assertMovement(
            direction=Direction.NORTH,
            x_expected_change=NumChange.STAY,
            y_expected_change=NumChange.INCREASE
        )
        self.assertMovement(
            direction=Direction.NORTHEAST,
            x_expected_change=NumChange.INCREASE,
            y_expected_change=NumChange.INCREASE
        )
        self.assertMovement(
            direction=Direction.EAST,
            x_expected_change=NumChange.INCREASE,
            y_expected_change=NumChange.STAY
        )
        self.assertMovement(
            direction=Direction.SOUTHEAST,
            x_expected_change=NumChange.INCREASE,
            y_expected_change=NumChange.DECREASE
        )
        self.assertMovement(
            direction=Direction.SOUTH,
            x_expected_change=NumChange.STAY,
            y_expected_change=NumChange.DECREASE
        )
        self.assertMovement(
            direction=Direction.SOUTHWEST,
            x_expected_change=NumChange.DECREASE,
            y_expected_change=NumChange.DECREASE
        )
        self.assertMovement(
            direction=Direction.WEST,
            x_expected_change=NumChange.DECREASE,
            y_expected_change=NumChange.STAY
        )
        self.assertMovement(
            direction=Direction.NORTHWEST,
            x_expected_change=NumChange.DECREASE,
            y_expected_change=NumChange.INCREASE
        )
