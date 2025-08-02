from Player import Player
import json

class NetworkPlayer(Player):
    def __init__(self, name, symbol, conn, addr):
        super().__init__(name, symbol)
        self.conn = conn
        self.addr = addr
    
    def player_move(self, board):      
        try:
            move_data = self.conn.recv(1024)
            if not move_data:
                raise ConnectionError("اتصال قطع شد.")
            
            # دریافت داده‌ها به صورت JSON
            move_data = json.loads(move_data.decode('utf-8'))
            move = move_data['move']
            
            if 0 < move < 10:
                move2 = [(move - 1) // 3, ((move - 1) % 3)]
                if board.get_symbol(move2) == "_":
                    return move2
                else:
                    self.conn.send(json.dumps({"error": "این خونه پره، یه خونه دیگه رو انتخاب کن!"}).encode('utf-8'))
            
        except (ValueError, ConnectionError):
            print("خطا در دریافت حرکت از شبکه.")
            return None