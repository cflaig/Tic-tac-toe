from typing import List, Tuple, Any


WON: int = 100000


class Board:

    first_player: str
    second_player: str
    required_for_winning: int
    board_size: int
    fields: List[List[str]]
    is_first_player: bool
    past_moves: List[Tuple[int, int]]

    def __init__(self, first_player: str, second_player: str, board_size: int = 3, required_for_winning: int = 3):
        self.first_player = first_player
        self.second_player = second_player
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.fields = [['' for _ in range(self.board_size + 1)] for _ in range(self.board_size + 1)]
        self.is_first_player = True
        self.past_moves = []

    def move(self, move: Tuple[int, int]) -> None:
        self.fields[move[0]][move[1]] = self.first_player if self.is_first_player else self.second_player
        self.switch_player()
        self.past_moves.append(move)

    def unmove(self):
        x, y = self.past_moves.pop()
        self.fields[x][y] = ''
        self.switch_player()

    def switch_player(self):
        self.is_first_player = not self.is_first_player

    def score(self) -> int:
        if not self.past_moves:
            return 0

        x, y = self.past_moves[-1]
        symbol = self.fields[x][y]
        down_right_count = self.count_symbol(x, y, -1, -1, symbol) + self.count_symbol(x, y, 1, 1, symbol) - 1
        down_left_count = self.count_symbol(x, y, 1, -1, symbol) + self.count_symbol(x, y, -1, 1, symbol) - 1
        vertical = self.count_symbol(x, y, -1, 0, symbol) + self.count_symbol(x, y, 1, 0, symbol) - 1
        horizontal = self.count_symbol(x, y, 0, -1, symbol) + self.count_symbol(x, y, 0, 1, symbol) - 1

        return WON if max(down_right_count, down_left_count, vertical, horizontal) >= self.required_for_winning else 0

    def possible_moves(self) -> List[Tuple[int, int]]:
        return [(x, y) for x in range(self.board_size) for y in range(self.board_size) if self.fields[x][y] == '']

    def count_symbol(self, x: int, y: int, x_step: int, y_step: int, symbol: str):
        count: int = 0

        while self.fields[x][y] == symbol:
            count += 1
            x += x_step
            y += y_step

        return count

    def cpu_move(self):
        move = negamax(self, WON, -WON)[1]
        if not move is None:
            self.move(move)


def negamax(node, alpha, beta) -> Tuple[int, Any]:
    possible_moves: List = node.possible_moves()
    score = node.score()

    if not possible_moves or score == WON:
        return score, None

    best = WON, None
    for move in possible_moves:
        node.move(move)
        value = -negamax(node, -beta, -alpha)[0]
        node.unmove()

        if value < best[0]:
            best = value, move

        alpha = min(alpha, value)

        if alpha <= beta:
            break

    return best
