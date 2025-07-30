class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def player_move(self):
        move = input(f"{self.name} نوبتته، بازی کن")
        while True:
            try:
                move = int(move)
            except ValueError: 
                move = input(f"یچی بزن بفهمم چکار باید بکنم من {self.name}")
            else:
                if 0 < move < 10:
                    move2 = [(move - 1) // 3, ((move - 1) % 3)]
                    return move2
                else:
                    move = input(f"یچی بزن بفهمم چکار باید بکنم من {self.name}(یه عدد از 1 تا 9)")