from Board import Board
from Player import Player
from Bot import Bot
from Game import Game
# --- بخش اصلی برنامه (خارج از کلاس‌ها) ---
def start ():
    print()
    print("سلام سلام")
    name = input("برای شروع بازی، اسمتو وارد کن")
    symbol = input("دوست داری X باشی یا O؟")
    while True:
        if symbol.lower() == "x" or symbol.lower() == "o":
            break
        symbol = input("فقط X یا O رو برام وارد کن")

    player = Player(name, symbol.upper())
    bot = Bot(symbol) 

    current_player_input = input("اگه میخوای اول شروغ کنی 1 و اگه میخوای دوم باشی 2 رو بفرست برام")
    while True:
        try:
            current_player_input = int(current_player_input)
        except ValueError:
            current_player_input = input("ترو قرآن یا 1 رو بفرست یا 2 رو")
        else:
            
            if not (current_player_input == 1 or current_player_input == 2):
                current_player_input = input("ترو قرآن یا 1 رو بفرست یا 2 رو")
            else:
                if current_player_input == 1:
                    final_current_player = player 
                else:
                    final_current_player = bot 
                break

    board = Board()
    board.shwo()
    game = Game(board, player, bot, final_current_player)
while True: a
    start()
    ask = input("بازم میخوای بازی کنی؟(yes or no)")
    while True:
        
        if (ask.upper() == "NO")
            break a
        if (ask.upper() == "YES"):
            continue a
        ask = input("فقط برام yes یا no رو وارد کن")
        
    
    