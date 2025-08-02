from Board import Board
from Player import Player
from Bot import Bot
from NetworkPlayer import NetworkPlayer
import json

class Game:
    def __init__(self, board, player1, player2, current_player):
        self.current_player = current_player
        self.player1 = player1
        self.player2 = player2
        self.board = board

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
            
    def end_mach(self, move):
        if self.board.check_win(move):
            return True
        return False

    def play(self):
        while True:
            print(f"\nنوبت {self.current_player.name} ({self.current_player.symbol}) است.")
            
            move = None
            if isinstance(self.current_player, Bot):
                move = self.current_player.bot_move(self.board)
            elif not isinstance(self.current_player, NetworkPlayer):
                move = self.current_player.player_move(self.board)
            else:
                self.send_game_state_to_player()
                move_data = self.current_player.conn.recv(1024)
                if move_data:
                    try:
                        move_data = json.loads(move_data.decode('utf-8'))
                        move = move_data['move']
                    except (json.JSONDecodeError, KeyError):
                        print("خطا در دریافت داده از شبکه.")
                        continue
                else:
                    print("اتصال قطع شد.")
                    return

            self.send_move_to_opponent(move)
            
            if move is None:
                continue 
            
            self.board.makes_move(self.current_player.symbol, move)
            self.board.show()
            
            if self.board.check_win(move):
                print(f"{self.current_player.name} برد!")
                self.send_game_result("win")
                return

            if self.board.is_full():
                print("ای بابا، مساوی کردید که")
                self.send_game_result("draw")
                return
                
            self.switch_player()
            
    def send_game_state_to_player(self):
        if isinstance(self.current_player, NetworkPlayer):
            game_state = {
                "board": self.board.map,
                "current_player": self.current_player.symbol
            }
            message = json.dumps(game_state).encode('utf-8')
            self.current_player.conn.sendall(message)

    def send_move_to_opponent(self, move):
        if isinstance(self.player1, NetworkPlayer) and isinstance(self.player2, NetworkPlayer):
            opponent = self.player2 if self.current_player == self.player1 else self.player1
            move_data = {
                "move": move,
                "player": self.current_player.symbol
            }
            message = json.dumps(move_data).encode('utf-8')
            opponent.conn.sendall(message)
    
    def send_game_result(self, result):
        if isinstance(self.player1, NetworkPlayer) and isinstance(self.player2, NetworkPlayer):
            message = {
                "result": result,
                "winner": self.current_player.name if result == "win" else None
            }
            message = json.dumps(message).encode('utf-8')
            self.player1.conn.sendall(message)
            self.player2.conn.sendall(message)