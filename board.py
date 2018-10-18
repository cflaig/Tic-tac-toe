from copy import deepcopy
from typing import List


class Board:

    first_player: str
    second_player: str
    required_for_winning: int
    board_size: int
    fields: List[List[str]]
    is_first_player: bool
    previous_state: 'Board'

    def __init__(self, first_player: str, second_player: str, board_size: int = 3, required_for_winning: int = 3):
        self.first_player = first_player
        self.second_player = second_player
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.is_first_player = True

        self.fields = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def move(self, x, y):
        self.previous_state = deepcopy(self)
        self.fields[x][y] = self.first_player if self.is_first_player else self.second_player
        self.is_first_player = not self.is_first_player
