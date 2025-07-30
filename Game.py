

class Game:
    def __init__(self, board, player1, player2, current_player):
        self.current_player = current_player
        self.player1 = player1
        self.player2 = player2
        self.board = board

    def switch_player(self):
        """
        bad az check_win call beshe
        """
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
            
    def end_mach(self, move):
        if self.board.check_win(move):
            return True

    def play(self):
        while True:
            if self.current_player == self.player1:
                move = self.player1.player_move()
            else:
                move = self.player2.bot_move(self.board)
                
            self.board.makes_move(self.current_player.symbol, move)
                
            self.board.show()
            if self.board.check_win(move):
                print(f"{self.current_player.name} برد!")
                return

            if self.board.is_full():
                print("ای بابا، مساوی کردی که")
                return
                
            self.switch_player()
            
        
        return

