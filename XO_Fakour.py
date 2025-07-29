class game_page:
    
    
    def __init__(self):
        
        self.map =[["_"," _"," _"],["_"," _"," _"],["_"," _"," _"]]
        
        
    def show (self):
        for i in range(3):
            for j in range(3):
                print(self.map[i][j], " ", end="")
            print()
            
            
    def make_move(self, player, move):
        
        if self.is_valid_move(move):
            if player == f"{player.name}" :
                self.map[move[0]][move[1]] = "X"
            else:
                self.map[move[0]][move[1]] = "O"
            return self.map

                
        print("این خونه پره، یه خونه دیگه رو برای حرکت انتخاب کنی!")
        return self.map

    
    def is_valid_move(self, move):
        return (self.map[move[0]][move[1]] == '_')
            
    
    
class player:
    
    def __init__(self, name,):
        self.name = name
    
    def player_move(self):
        move = input(f"{self.player.name}  نوبتته، بازی کن")
        try:
            move = int(move)
        except:
            print(f"یچی بزن بفهمم چکار باید بکنم من {self.player.name}")
        else :
            return move
            

a = game_page()
a.show()
        
