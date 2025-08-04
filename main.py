from Board import Board
from Player import Player
from Bot import Bot
from Game import Game
import socket
import threading

# آدرس و پورت سرور
HOST = '127.0.0.1'
PORT = 65432

# تابع برای دریافت پیام‌ها از سرور
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                print("ارتباط با سرور قطع شد.")
                break
            
            print(data)
            
            if "نوبت شماست" in data:
                print(">>> ", end='', flush=True)

        except (socket.error, ConnectionResetError):
            print("ارتباط قطع شد.")
            break

# تابع اصلی کلاینت برای اتصال و ارسال پیام
def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("به سرور بازی دوز وصل شدید.")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            move = input()
            client_socket.sendall(move.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("اتصال به سرور برقرار نشد. لطفا مطمئن شوید سرور در حال اجراست.")
    except (socket.error, ConnectionResetError):
        print("ارتباط قطع شد.")
    finally:
        client_socket.close()


def start():
    print()
    print("سلام سلام")
    teo_player = input("میخوای دو نفره بازی کنی (1) یا تنهایی(2)؟           ")
    while True:
        try:
            teo_player = int(teo_player)
        except ValueError:
            teo_player = input("ترو قرآن یا 1 رو بفرست یا 2 رو           ")
        else:
            if not (teo_player == 1 or teo_player == 2):
                teo_player = input("ترو قرآن یا 1 رو بفرست یا 2 رو           ")
            else:
                teo_player = (teo_player == 1)
                break
    
    player1 = None
    player2 = None
    final_current_player = None
    
    if not teo_player:
        name = input("برای شروع بازی، اسمتو وارد کن           ")
        symbol = input("دوست داری X باشی یا O؟           ")
        while True:
            if symbol.lower() in ["x", "o"]:
                break
            symbol = input("فقط X یا O رو برام وارد کن           ")
        player1 = Player(name, symbol.upper())
        player2 = Bot(symbol)
        current_player_input = input("اگه میخوای اول شروع کنی 1 و اگه میخوای دوم باشی 2 رو بفرست برام           ")
        while True:
            try:
                current_player_input = int(current_player_input)
            except ValueError:
                current_player_input = input("ترو قرآن یا 1 رو بفرست یا 2 رو           ")
            else:
                if not (current_player_input == 1 or current_player_input == 2):
                    current_player_input = input("ترو قرآن یا 1 رو بفرست یا 2 رو           ")
                else:
                    final_current_player = player1 if current_player_input == 1 else player2
                    break
    else:
        offline = input("میخوای روی یه سیستم بازی کنید؟(yes or no)           ")
        while True:
            if offline.lower() == "yes":
                offline = True
                break
            if offline.lower() == "no":
                offline = False
                break
            offline = input("just 'yes' or 'no'           ")
        
        if offline:
            name1 = input("برای شروع بازی، اسم نفر اول رو وارد کن           ")
            name2 = input("حالا اسم نفر دوم رو وارد کن           ")
            player1 = Player(name1, "X")
            player2 = Player(name2, "O")
            final_current_player = player1
            board = Board()
            board.show()
            game = Game(board, player1, player2, final_current_player)
            game.play()
        else:
            # اینجا تابع کلاینت برای بازی آنلاین اجرا میشه
            run_client()
            
    if player1 and player2 and final_current_player:
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
        if ask.upper() == "NO":
            test = False
            break 
        if ask.upper() == "YES":
            break
        ask = input("فقط برام yes یا no رو وارد کن          ")