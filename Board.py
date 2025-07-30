
class Board:
    def __init__(self):
        self.map = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]

    def show(self):
        print("""
              
              """)
        for i in range(3):
            for j in range(3):
                print(self.map[i][j], " ", end="")
            print()
        print("""
              """)
    def makes_move(self, symbol, move):
        if self.is_valid_move(move):
            self.map[move[0]][move[1]] = symbol
            self.show()
            return True
        else:
            print("این خونه پره، باید یه خونه دیگه رو برای حرکت انتخاب کنی!")
            return False

    def is_valid_move(self, move): 
            return (self.get_symbol(move) == "_")
                


    def is_full(self):
        for i in range(3):
            for j in range(3):
                if self.map[i][j] == "_":
                    return False
        return True

    def get_symbol(self, move):
        return self.map[move[0]][move[1]]

    def check_win(self, move):
        """
        bad az harekat dorost call beshe
        """
        if self.map[move[0]][move[1]] == self.map[(move[0] + 1) % 3][move[1]] and self.map[move[0]][move[1]] == self.map[(move[0] + 2) % 3][move[1]]:
            return True

        if self.map[move[0]][move[1]] == self.map[move[0]][(move[1] + 1) % 3] and self.map[move[0]][move[1]] == self.map[move[0]][(move[1] + 2) % 3]:
            return True

        if self.map[0][0] == self.map[1][1] and self.map[1][1] == self.map[2][2] and (not(self.map[1][1] == "_")):
            return True

        if self.map[0][2] == self.map[1][1] and self.map[1][1] == self.map[2][0] and (not(self.map[1][1] == "_")):
            return True

        return False