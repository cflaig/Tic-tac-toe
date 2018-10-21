from copy import deepcopy
from typing import List


class Board:

    first_player: str
    second_player: str
    required_for_winning: int
    board_size: int
    fields: List[List[str]]
    is_first_player: bool

    def __init__(self, first_player: str, second_player: str, board_size: int = 3, required_for_winning: int = 3):
        self.first_player = first_player
        self.second_player = second_player
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.is_first_player = True

        self.fields = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def move(self, x, y):
        new_board: Board = deepcopy(self)
        new_board.fields[x][y] = new_board.first_player if new_board.is_first_player else new_board.second_player
        new_board.is_first_player = not new_board.is_first_player
        return new_board
