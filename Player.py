class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def player_move(self, board):
        move = input(f"{self.name} نوبتته، بازی کن           ")
        while True:
            try:
                move = int(move)
            except ValueError: 
                move = input(f"یچی بزن بفهمم چکار باید بکنم من {self.name}        ")
            else:
                if 0 < move < 10:
                    move2 = [(move - 1) // 3, ((move - 1) % 3)]
                    if not(board.get_symbol(move2) == "_"):
                        move = input("این خونه پره، یه خونه دیگه رو برای حرکت انتخاب کنی!      ")


                    return move2
                else:
                    move = input(f"یچی بزن بفهمم چکار باید بکنم من {self.name}(یه عدد از 1 تا 9)            ")
                    
                    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.symbol == other.symbol
    