from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from copy import deepcopy


BOARD_SIZE = 3
REQUIRED_FOR_WINNING = 3


class Board:

    def __init__(self, board_size, required_for_winning, other=None):
        self.required_for_winning = required_for_winning
        self.board_size = board_size

        if other:
            self.__dict__ = deepcopy(other.__dict__)


class Gui:

    def __init__(self, board):
        self.board = board

    def show(self):
        app = QApplication([])
        window = QWidget()
        layout = QGridLayout(window)

        for x in range(self.board.board_size):
            for y in range(self.board.board_size):
                layout.addWidget(QPushButton(), x, y)

        window.show()
        app.exec_()


if __name__ == '__main__':
    Gui(Board(BOARD_SIZE, REQUIRED_FOR_WINNING)).show()
