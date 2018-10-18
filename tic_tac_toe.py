from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from copy import deepcopy


BOARD_SIZE = 3
REQUIRED_FOR_WINNING = 3


class Board:

    def __init__(self, board_size, required_for_winning, other=None):
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.fields = {}

        self.fields = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

        if other:
            self.__dict__ = deepcopy(other.__dict__)


class Gui:

    def __init__(self, board):
        self.board = board

    def show(self):
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle('Tic tac toe')
        layout = QGridLayout(window)

        for x in range(self.board.board_size):
            for y in range(self.board.board_size):
                button = QPushButton(self.board.fields[x][y])
                button.clicked.connect(lambda _, x=x, y=y: print(str(x) + ', ' + str(y)))
                layout.addWidget(button, x, y)

        window.show()
        app.exec()


if __name__ == '__main__':
    Gui(Board(BOARD_SIZE, REQUIRED_FOR_WINNING)).show()
