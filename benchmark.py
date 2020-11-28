from board import Board

import time

BOARD_SIZE = 4
REQUIRED_FOR_WINNING = 4


def run_benchmark(move):
    print("Run with move {}\n".format(move))
    print("| evaluated nodes | elapsed time | move / s  |")
    print("|-----------------|--------------|-----------|")

    board = Board('X', 'O', BOARD_SIZE, REQUIRED_FOR_WINNING)
    board.move(move)
    start_time = time.time()
    nr_nodes = board.cpu_move()
    elapsed_time = time.time() - start_time
    print("| {:15,d} | {:12.2f} | {:8.2f}k |".format(nr_nodes, elapsed_time, nr_nodes/elapsed_time/1000))
    print("|-----------------|--------------|-----------|")
    print("\n")


if __name__ == '__main__':
    run_benchmark((0, 0))
    run_benchmark((1, 1))

