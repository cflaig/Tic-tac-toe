from typing import List, Tuple, Any

WON: int = 100000
INF: int = 9 * WON


class Board:

    first_player: str
    second_player: str
    required_for_winning: int
    board_size: int
    fields: List[List[str]]
    is_first_player: bool
    past_moves: List[Tuple[int, int]]
    num_evaluations: int
    sorted_range: List[int]
    verbose: int

    def __init__(self, first_player: str,
                 second_player: str,
                 board_size: int = 3,
                 required_for_winning: int = 3,
                 verbose: int = 0):
        self.first_player = first_player
        self.second_player = second_player
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.fields = [['' for _ in range(self.board_size + 1)] for _ in range(self.board_size + 1)]
        self.is_first_player = True
        self.past_moves = []
        self.verbose = verbose

        self.sorted_range = list(range(board_size))

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
        self.num_evaluations += 1
        if not self.past_moves:
            return 0

        x, y = self.past_moves[-1]
        symbol = self.fields[x][y]
        down_right_count = self.count_symbol(x, y, -1, -1, symbol) + self.count_symbol(x, y, 1, 1, symbol) - 1
        down_left_count = self.count_symbol(x, y, 1, -1, symbol) + self.count_symbol(x, y, -1, 1, symbol) - 1
        vertical = self.count_symbol(x, y, -1, 0, symbol) + self.count_symbol(x, y, 1, 0, symbol) - 1
        horizontal = self.count_symbol(x, y, 0, -1, symbol) + self.count_symbol(x, y, 0, 1, symbol) - 1

        return (WON - len(self.past_moves))\
            if max(down_right_count, down_left_count, vertical, horizontal) >= self.required_for_winning\
            else 0

    def possible_moves(self) -> List[Tuple[int, int]]:
        return [(x, y) for x in self.sorted_range for y in self.sorted_range if self.fields[x][y] == '']

    def count_symbol(self, x: int, y: int, x_step: int, y_step: int, symbol: str):
        count: int = 0

        while self.fields[x][y] == symbol:
            count += 1
            x += x_step
            y += y_step

        return count

    def cpu_move(self):
        self.num_evaluations = 0

        value, move = negamax(self, -INF, INF, 0, 3)
        if self.verbose > 0:
            print("Value: " + str(value) + " Move: " + str(move))
        if move is not None:
            self.move(move)
            if self.verbose > 0:
                print("number moves: " + str(self.num_evaluations))
        return self.num_evaluations


def negamax(node, alpha, beta, depth, debug_depth) -> Tuple[int, Any]:
    score = node.score()
    if score >= WON / 10:
        return -score, None

    possible_moves: List = node.possible_moves()

    if not possible_moves:
        return 0, None

    best: Tuple[int, Any] = (-INF, None)
    for move in possible_moves:
        node.move(move)
        value = -negamax(node, -beta, -alpha, depth + 1, debug_depth)[0]
        node.unmove()

        if value > best[0]:
            best = value, move
            alpha = max(value, alpha)
            if alpha >= beta:
                break
    return best
