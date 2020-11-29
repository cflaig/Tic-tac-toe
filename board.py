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
    transposition_table: List
    sorted_range: List[int]
    table_size: int
    verbose: int

    def __init__(self, first_player: str,
                 second_player: str,
                 board_size: int = 3,
                 required_for_winning: int = 3,
                 hash_table_size: int = 19,
                 verbose: int = 0):
        self.first_player = first_player
        self.second_player = second_player
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.fields = [['' for _ in range(self.board_size + 1)] for _ in range(self.board_size + 1)]
        self.is_first_player = True
        self.past_moves = []
        self.table_size = min(3**(board_size**2), 2**hash_table_size - 1)
        self.transposition_table = [None for _ in range(self.table_size)]
        self.verbose = verbose
        if verbose > 0:
            print("transposition count: " + str(len(self.transposition_table)))

        r = list(range(board_size))
        self.sorted_range = []
        while len(r) > 0:
            self.sorted_range.append(r.pop())
            if len(r) > 0:
                self.sorted_range.append(r.pop(0))
        self.sorted_range.reverse()
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

    def possible_moves(self, move: Tuple[int, int]) -> List[Tuple[int, int]]:
        if move is None:
            return [(x, y) for x in self.sorted_range for y in self.sorted_range if self.fields[x][y] == '']

        moves = [move]
        mx, my = move
        for x in self.sorted_range:
            for y in self.sorted_range:
                if self.fields[x][y] == '' and (mx != x or my != y):
                    moves.append((x, y))
        return moves

    def count_symbol(self, x: int, y: int, x_step: int, y_step: int, symbol: str):
        count: int = 0

        while self.fields[x][y] == symbol:
            count += 1
            x += x_step
            y += y_step

        return count

    def cpu_move(self):
        self.num_evaluations = 0
        if self.verbose > 0:
            print("hash of actual board: " + str(self.get_hash()))

        value, move = negamax(self, -INF, INF, 0, 3)
        if self.verbose > 0:
            print("Value: " + str(value) + " Move: " + str(move))
        if move is not None:
            self.move(move)
            if self.verbose > 0:
                print("number moves: " + str(self.num_evaluations))
                print("hash: " + str(self.get_hash()))
                print("hash: " + str(self.transposition_table[self.get_hash()[0]]))
        return self.num_evaluations

    def get_hash(self) -> (int, int):
        value = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                field = self.fields[x][y]
                value = value * 3 + (1 if field == self.first_player else (2 if field == self.second_player else 0))

        return (1009*value % self.table_size, value)


EXACT = 0
LOWER_BOUND = 1
UPPER_BOUND = 2


def negamax(node, alpha, beta, depth, debug_depth) -> Tuple[int, Any]:
    alpha_orig = alpha
    hash_value, pos = node.get_hash()
    tmp = node.transposition_table[hash_value]
    move = None

    if tmp is not None and tmp[2] == pos:
        flag = tmp[1]
        value, move = tmp[0]
        if flag == EXACT:
            return tmp[0]
        elif flag == LOWER_BOUND:
            alpha = max(alpha, value)
        elif flag == UPPER_BOUND:
            beta = min(beta, value)
        if alpha >= beta:
            return tmp[0]

    score = node.score()
    if score >= WON / 10:
        return -score, None

    possible_moves: List = node.possible_moves(move)

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
                break;

    if best[0] < alpha_orig:
        flag = UPPER_BOUND
        move_value = best[0]
    elif best[0] >= beta:
        flag = LOWER_BOUND
        move_value = best[0]
    else:
        flag = EXACT
        move_value = best[0]
    node.transposition_table[hash_value] = ((move_value, best[1]), flag, pos)
    return best
