from board import Board
from gui import Gui


BOARD_SIZE = 4
REQUIRED_FOR_WINNING = 3

if __name__ == '__main__':
    Gui(Board('X', 'O', BOARD_SIZE, REQUIRED_FOR_WINNING)).show()
