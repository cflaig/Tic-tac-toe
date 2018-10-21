from copy import deepcopy
from typing import List, Tuple


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
        self.fields = [['' for _ in range(self.board_size + 1)] for _ in range(self.board_size + 1)]

    def move(self, x: int, y: int):
        new_board: Board = deepcopy(self)
        new_board.fields[x][y] = new_board.first_player if new_board.is_first_player else new_board.second_player
        new_board.is_first_player = not new_board.is_first_player
        new_board.score(x, y)
        return new_board

    def score(self, x: int, y: int) -> int:
        symbol = self.fields[x][y]
        down_right_count = self.count_symbol(x, y, -1, -1, symbol) + self.count_symbol(x, y, 1, 1, symbol) - 1
        down_left_count = self.count_symbol(x, y, 1, -1, symbol) + self.count_symbol(x, y, -1, 1, symbol) - 1
        vertical = self.count_symbol(x, y, -1, 0, symbol) + self.count_symbol(x, y, 1, 0, symbol) - 1
        horizontal = self.count_symbol(x, y, 0, -1, symbol) + self.count_symbol(x, y, 0, 1, symbol) - 1

        return 100000 if max(down_right_count, down_left_count, vertical, horizontal) == self.required_for_winning else 0

    def possible_moves(self) -> List[Tuple[int, int]]:
        return [(x, y) for x in range(self.board_size) for y in range(self.board_size) if self.fields[x][y] == '']

    def count_symbol(self, x: int, y: int, x_step: int, y_step: int, symbol: str):
        count: int = 0

        while self.fields[x][y] == symbol:
            count += 1
            x += x_step
            y += y_step

        return count
