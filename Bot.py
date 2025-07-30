from Board import Board


class Bot:
    def __init__(self, symbol):
        if symbol.lower() == "x":
            self.symbol = "O"
        else:
            self.symbol = "X"

    def bot_move(self):
        return