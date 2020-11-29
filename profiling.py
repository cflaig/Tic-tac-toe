from board import Board

import cProfile

BOARD_SIZE = 4
REQUIRED_FOR_WINNING = 4

if __name__ == '__main__':
    board = Board('X', 'O', BOARD_SIZE, REQUIRED_FOR_WINNING, 19)
    board.move((1,1))
    board.cpu_move()

    board = Board('X', 'O', BOARD_SIZE, REQUIRED_FOR_WINNING, 19)
    cProfile.run('board.cpu_move()')
