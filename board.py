from copy import deepcopy


class Board:

    def __init__(self, board_size, required_for_winning, other=None):
        self.required_for_winning = required_for_winning
        self.board_size = board_size
        self.fields = {}

        self.fields = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

        if other:
            self.__dict__ = deepcopy(other.__dict__)