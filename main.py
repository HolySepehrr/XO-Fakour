
from Board import Board
from Player import Player
from Bot import Bot
from Game import Game


def start ():
    print()
    print("سلام سلام")
    teo_player = input("میخوای دو نفره بازی کنی (1) یا تنهایی(2)؟           ")
    while True:
        try:
            teo_player = int(teo_player)
        except ValueError:
            current_player_input = input("           ترو قرآن یا 1 رو بفرست یا 2 رو")
        else:
            if not (teo_player == 1 or teo_player == 2):
                teo_player = input("           ترو قرآن یا 1 رو بفرست یا 2 رو")
            else:
                if teo_player == 1:
                    teo_player = True 
                else:
                    teo_player = False 
                break

            
    if not(teo_player) :
        name = input("برای شروع بازی، اسمتو وارد کن           ")
        symbol = input("دوست داری X باشی یا O؟           ")
        while True:
            if symbol.lower() == "x" or symbol.lower() == "o":
                break
            symbol = input("فقط X یا O رو برام وارد کن           ")
    
        player1 = Player(name, symbol.upper())
        player2 = Bot(symbol) 
    
        current_player_input = input("اگه میخوای اول شروغ کنی 1 و اگه میخوای دوم باشی 2 رو بفرست برام           ")
              
        while True:
            try:
                current_player_input = int(current_player_input)
            except ValueError:
                current_player_input = input("           ترو قرآن یا 1 رو بفرست یا 2 رو")
            else:
                
                if not (current_player_input == 1 or current_player_input == 2):
                    current_player_input = input("           ترو قرآن یا 1 رو بفرست یا 2 رو")
                else:
                    if current_player_input == 1:
                        final_current_player = player1 
                    else:
                        final_current_player = player2 
                    break

    else :
        name1 = input("برای شروع بازی، اسم نفر اول رو وارد کن           ")
        name2 = input("حالا اسم نفر دوم رو وارد کن           ")

    
    
        player1 = Player(name1, "X")
        player2 = Player(name2, "O")

              
        final_current_player = player1



    board = Board()
    board.show()
    game = Game(board, player1, player2, final_current_player)
    
    game.play()
    return
test = True
while test: 
    start()
    ask = input("بازم میخوای بازی کنی؟(yes or no)           ")
    while True:
        if (ask.upper() == "NO"):
            test = False
            break 
        if (ask.upper() == "YES"):
            break
        ask = input("فقط برام yes یا no رو وارد کن          ")
            

    