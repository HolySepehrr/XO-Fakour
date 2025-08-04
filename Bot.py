from random import randint
import copy

class Bot:
    def __init__(self, symbol):
        if symbol.lower() == "x":
            self.symbol = "O"
            self.player_symbol = "X"
        else:
            self.symbol = "X"
            self.player_symbol = "O"
        self.name = "system"
        
        
    def bot_move(self, bord):
        for i in range(3):
            for j in range(3):
                test_bord = copy.deepcopy(bord)
                move = [i, j]
                if test_bord.map[i][j] == "_":
                    test_bord.makes_move(self.symbol, move)
                    if test_bord.check_win(move):
                        return move
        for i in range(3):
            for j in range(3):
                test_bord = copy.deepcopy(bord)
                move = [i, j]
                if test_bord.map[i][j] == "_":
                    test_bord.makes_move(self.player_symbol, move)
                    if test_bord.check_win(move):
                        return move

        test_bord = copy.deepcopy(bord)
        empty_spaces = []
        for i in range(3):
            for j in range(3):
                if test_bord.map[i][j] == "_":
                    empty_spaces.append([i, j])
        random = randint(0, len(empty_spaces)-1)
        move = empty_spaces[random]
        return move

                    
            
          
    def __eq__(self, other):
        if not isinstance(other, Bot):
            return False
        return True