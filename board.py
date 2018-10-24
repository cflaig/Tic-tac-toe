from typing import List, Tuple, Any

PRIME = (2 ** 19 - 1)

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
    transposition_table: List

    def __init__(self, first_player: str, second_player: str, board_size: int = 3, required_for_winning: int = 3):
        self.first_player = first_player
        self.second_player = second_player
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.fields = [['' for _ in range(self.board_size + 1)] for _ in range(self.board_size + 1)]
        self.is_first_player = True
        self.past_moves = []
        self.transposition_table = [None for _ in range(PRIME)]

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
        self.num_evaluations = 0
        move = negamax(self, -INF, INF)[1]
        if not move is None:
            self.move(move)
        print(self.num_evaluations)
        print(self.transposition_table[self.get_hash()])

    def get_hash(self):
        hash_value = 0

        for x in range(self.board_size):
            for y in range(self.board_size):
                field = self.fields[x][y]
                hash_value = 3 * hash_value + (1 if field == self.first_player else 2 if field == self.second_player else 0)

        return hash_value % PRIME


def negamax(node, alpha, beta) -> Tuple[int, Any]:
    possible_moves: List = node.possible_moves()
    entry = node.transposition_table[node.get_hash()]

    if not entry is None:
        return entry

    score = node.score()

    if not possible_moves or score == WON:
        return -score, None

    best = -INF, None
    for move in possible_moves:
        node.move(move)
        value = -negamax(node, -beta, -alpha)[0]
        node.unmove()

        if value > best[0]:
            best = value, move

        alpha = max(alpha, value)

        if alpha >= beta:
            break

    node.transposition_table[node.get_hash()] = best
    return best
