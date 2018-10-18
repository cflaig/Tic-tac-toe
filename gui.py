from PyQt5.QtWidgets import *
from board import Board


class Gui:

    board: Board
    layout: QGridLayout

    def __init__(self, board: Board):
        self.board = board

    def show(self):
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle('Tic tac toe')
        self.layout = QGridLayout(window)
        self._create_buttons()

        window.show()
        app.exec()

    def _create_buttons(self):
        for x in range(self.board.board_size):
            for y in range(self.board.board_size):
                field_content = self.board.fields[x][y]
                button = QToolButton()
                button.setText(field_content)
                button.setDisabled(field_content != '')
                button.clicked.connect(lambda _, x=x, y=y: self.click_handler(x, y))
                self.layout.addWidget(button, x, y)

    def click_handler(self, x, y):
        self.board.move(x, y)
        self._create_buttons()