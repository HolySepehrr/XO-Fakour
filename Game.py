
from board import Board
from player import Player
from bot import Bot

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
        if self.switch_player == self.player1:
            self.switch_player = self.player2
        else:
            self.switch_player = self.player1

    def play(self):
        
        return

