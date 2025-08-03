from Board import Board
from Player import Player
from Bot import Bot
from Game import Game
import socket
from NetworkPlayer import NetworkPlayer

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
        ofline = input("میخوای روی یه سیستم بازی کنید؟(yes or no)           ")
        while True:
            if ofline.lower() == "yes":
                oline = True
                break
            if ofline.lower() == "no":
                ofline = False
                break
            ofline = input("just 'yes' or 'no'           ")
        
        if ofline:
            name1 = input("برای شروع بازی، اسم نفر اول رو وارد کن           ")
            name2 = input("حالا اسم نفر دوم رو وارد کن           ")
            player1 = Player(name1, "X")
            player2 = Player(name2, "O")
            final_current_player = player1
        else:
            role = input("میخوای به یه بازی اضافه بشی(1) یا بازی جدید بسازی(2)؟           ")
            while True:
                try:
                    role = int(role)
                except ValueError:
                    role = input("لطفا 1 یا 2 رو وارد کن           ")
                else:
                    if role in [1, 2]:
                        break
                    role = input("لطفا 1 یا 2 رو وارد کن           ")
            
            if role == 2:
                HOST = '127.0.0.1'
                PORT = 55555
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((HOST, PORT))
                server_socket.listen()
                print(f"سرور در حال گوش دادن روی پورت {HOST} منتظر رفیقتم...")

                conn, addr = server_socket.accept()
                player2_name = conn.recv(1024).decode('utf-8')

                print(f"رفیقت({player2_name}) از آدرس {addr}اومد")


                name1 = input("اسمت رو وارد کن (X هستی):           ")
                conn.send(name1.encode('utf-8'))
                

                player1 = NetworkPlayer(name1, "X", conn, addr)
                player2 = NetworkPlayer(player2_name, "O", conn, addr)
                
                final_current_player = player1
                server_socket.close()

            else:
                HOST = input("آدرس IP سرور رو وارد کن:           ")
                PORT = 55555
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    client_socket.connect((HOST, PORT))
                    print(f"اتصال به سرور {HOST} برقرار شد.")
                    name2 = input("اسمت رو وارد کن (O هستی):           ")
                    client_socket.send(name2.encode('utf-8'))
                    player1_name = client_socket.recv(1024).decode('utf-8')

                    player1 = NetworkPlayer(player1_name, "X", client_socket, None)
                    player2 = NetworkPlayer(name2, "O", client_socket, None)
                    
                    final_current_player = player1
                    
                except Exception as e:
                    print(f"خطا در اتصال به سرور: {e}")
                    return

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
        ask = input("فقط برام yes یا no رو وارد کن           ")