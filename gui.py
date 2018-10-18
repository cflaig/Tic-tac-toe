from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton


class Gui:

    layout: QGridLayout

    def __init__(self, board):
        self.board = board

    def show(self):
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle('Tic tac toe')
        self.layout = QGridLayout(window)
        self.create_buttons()

        window.show()
        app.exec()

    def create_buttons(self):
        for x in range(self.board.board_size):
            for y in range(self.board.board_size):
                field_content = self.board.fields[x][y]
                button = QPushButton(field_content)
                button.setDisabled(field_content != '')
                button.clicked.connect(lambda _, x=x, y=y: self.click_handler(x, y))
                self.layout.addWidget(button, x, y)

    def click_handler(self, x, y):
        self.board.move(x, y)
        self.create_buttons()