from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton


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