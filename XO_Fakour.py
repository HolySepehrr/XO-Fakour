class Board:
    
    
    def __init__(self):
        
        self.map =[["_","_","_"],["_","_","_"],["_","_","_"]]
        
        
    def show (self):
        for i in range(3):
            for j in range(3):
                print(self.map[i][j], " ", end="")
            print()
            
            
    def makes_move(self, player, move):
        
        if self.is_valid_move(move):
            self.map[move[0]][move[1]] = player.symbol
            return True
        else:
            print("این خونه پره، یه خونه دیگه رو برای حرکت انتخاب کنی!")
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
        if self.map[move[0]][move[1]] == self.map[(move[0]+1)%3][move[1]] and self.map[(move[0]+1)%3][move[1]] == self.map[(move[0]+2)%3][move[1]]:
            return True
        
        if self.map[move[0]][move[1]] == self.map[move[0]][(move[1]+1)%3] and self.map[move[0]][(move[1]+1)%3] == self.map[move[0]][(move[1]+2)%3]:
            return True
        
        if self.map[0][0] == self.map[1][1] and self.map[1][1] == self.map[2][2] :
            return True
        
        if self.map[0][2] == self.map[1][1] and self.map[1][1] == self.map[2][0] :
            return True
        
        return False
        
    
    
class Player:
    
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
    
    def player_move(self):
        move = input(f"{self.name}  نوبتته، بازی کن")
        while True:
            try:
                move = int(move)
            except:
                move = input(f"یچی بزن بفهمم چکار باید بکنم من {self.name}")
            else :
                
                if 0 < move < 10:
                    move2 = [(move-1)//3, (move-1)//3]
                    return move2
                else:
                    move = input(f"یچی بزن بفهمم چکار باید بکنم من {self.name}(یه عدد از 1 تا 9)")
                



class Game:
    def __init__(self, board, player1 , player2 , current_player):
        self.current_player = current_player
        self.player1 = player1
        self.player2 = player2        
        self.board = board
        
    def switch_player(self):
        """
        bad az check_win call beshe 
        """
        if self.switch_player == self.player1:
            self.switch_player =  self.player2
        else:
            self.switch_player =  self.player1
            
    
    
    
    def play(self):
        return
        
        
class Bot:
    def __init__(self , symbol):
        if symbol.lower() == "x" :
            self.symbol = "O"
        else:
            self.symbol = "X"
    def bot_move(self, bord):
        return
        
        
        
        
        
        
        
        
print()
print("سلام سلام")
name = input("برای شروع بازی، اسمتو وارد کن")
symbol = input("دوست داری X باشی یا O؟")
while True:
    if symbol.lower() == "x" or symbol.lower() == "o" :
        break
    symbol = input("فقط X یا O رو برام وارد کن")
player = Player(name, symbol.upper())
bot = Bot(symbol)
current_player = input("اگه میخوای اول شروغ کنی 1 و اگه میخوای دوم باشی 2 رو بفرست برام")
while True:
    try:
        current_player = int(current_player)
    except:
        current_player = input("ترو قرآن یا 1 رو بفرست یا 2 رو")
    else:
        if not(current_player == 1 or current_player == 2) :
            current_player = input("ترو قرآن یا 1 رو بفرست یا 2 رو")
        else:
            if current_player == 1:
                current_player = player
            else:
                current_player = bot
            break
                
        
board = Board()
        
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        