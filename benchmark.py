from board import Board

import time

BOARD_SIZE = 4
REQUIRED_FOR_WINNING = 4


def run_different_table_size(move):
    print("Run with move {}\n".format(move))
    print("|Hash table size | evaluated nodes | elapsed time | move / s  |")
    print("|----------------|-----------------|--------------|-----------|")

    for i in range(27, 0, -2):
        board = Board('X', 'O', BOARD_SIZE, REQUIRED_FOR_WINNING, i)
        board.move(move)
        start_time = time.time()
        nr_nodes = board.cpu_move()
        elapsed_time = time.time() - start_time
        print("|{:15,d} | {:15,d} | {:12.2f} | {:8.2f}k |".format(2 ** i - 1, nr_nodes, elapsed_time, nr_nodes/elapsed_time/1000))
    print("|----------------|-----------------|--------------|-----------|")
    print("\n")

if __name__ == '__main__':
    run_different_table_size((0, 0))
    run_different_table_size((1, 1))
