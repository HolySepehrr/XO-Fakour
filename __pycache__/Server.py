import socket
import threading
from Board import Board
from Player import Player

HOST = "127.0.0.1"
PORT = 65432

# این کلاس مسئول مدیریت همه چیز تو بازیه
class GameServer:

    def __init__(self):
        # تخته بازی رو میسازیم
        self.board = Board.Board()
        # لیست بازیکنان و اتصالاتشون رو خالی میذاریم
        self.players = []
        self.player_connections = []
        # نوبت رو میدیم به بازیکن اول
        self.current_player_index = 0
        # بازی هنوز تموم نشده
        self.game_over = False
        # این قفل برای اینکه دوتا بازیکن همزمان نخوان کاری کنن
        self.lock = threading.Lock()

    # این تابع رو برای هر بازیکن تو یه نخ جدا اجرا می‌کنیم
    def handle_client(self, conn, player_index):
        # بازیکن رو از لیست پیدا می‌کنیم
        player = self.players[player_index]
        # یه پیام خوشامدگویی بهش میفرستیم
        conn.sendall(f"به بازی خوش آمدی! شما بازیکن {player.name} و نماد شما {player.symbol} هستید.".encode('utf-8'))
        
        # تا وقتی بازی تموم نشده، تو این حلقه میمونیم
        while not self.game_over:
            # فقط وقتی نوبت این بازیکنه، بهش پیام میدیم
            if self.current_player_index == player_index:
                conn.sendall(f"نوبت شماست، حرکت خود را وارد کنید (1-9) ".encode('utf-8'))
                
                try:
                    # از بازیکن حرکت رو می‌گیریم
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        # اگه چیزی نیومد، یعنی ارتباط قطع شده
                        print("اتصال قطع شد:(")
                        break
                    
                    # با lock مطمئن میشیم که بقیه کارها منتظر میمونن
                    with self.lock:
                        try:
                            # حرکت رو به عدد تبدیل می‌کنیم
                            move = int(data)
                            if 0 < move < 10:
                                # حرکت رو به مختصات تبدیل می‌کنیم
                                row, col = (move - 1) // 3, (move - 1) % 3
                                
                                # چک می‌کنیم حرکت درست هست یا نه
                                if self.board.is_valid_move((row, col)):
                                    # اگه درست بود، حرکت رو روی تخته انجام میدیم
                                    self.board.makes_move(player.symbol, (row, col))
                                    # تخته رو برای همه میفرستیم
                                    self.send_board_to_all_clients()
                                    
                                    # چک می‌کنیم کسی برنده شده یا نه
                                    if self.board.check_win((row, col)):
                                        self.game_over = True
                                        self.send_message_to_all_clients(f"خب خب، {player.name} برد")
                                    # چک می‌کنیم تخته پر شده یا نه
                                    elif self.board.is_full():
                                        self.game_over = True
                                        self.send_message_to_all_clients("مساوی کردید به سلامتی")
                                    else:
                                        # اگه بازی تموم نشده، نوبت رو عوض می‌کنیم
                                        self.current_player_index = (self.current_player_index + 1) % 2
                                        self.send_message_to_all_clients(f"نوبت بازیکن {self.players[self.current_player_index].name} است.")
                                else:
                                    # اگه خونه پر بود، بهش میگیم
                                    conn.sendall("این خونه پره، باید یه خونه دیگه رو برای حرکت انتخاب کنی!      ".encode('utf-8'))
                            else:
                                # اگه عدد بین 1 تا 9 نبود
                                conn.sendall("یچی بزن بفهمم چکار باید بکنم من (یه عدد از 1 تا 9)            ".encode('utf-8'))
                        except ValueError:
                            # اگه ورودی عدد نبود
                            conn.sendall("یچی بزن بفهمم چکار باید بکنم من (یه عدد از 1 تا 9)            ".encode('utf-8'))
                
                except (socket.error, ConnectionResetError):
                    # اگه ارتباط قطع شد، پیام میدیم و بازی رو تموم میکنیم
                    print(f"ارتباط با بازیکن {player.name} قطع شد.")
                    self.game_over = True
                    self.send_message_to_all_clients(f"بازیکن {player.name} قطع شد. بازی به پایان رسید.")
                    break
        
        # وقتی حلقه تموم شد، ارتباط رو میبندیم
        conn.close()

    # این تابع تخته رو برای همه میفرسته
    def send_board_to_all_clients(self):
        board_str = "\n".join([" ".join(row) for row in self.board.map])
        message = f"وضعیت جدید تخته:\n{board_str}"
        self.send_message_to_all_clients(message)

    # این تابع هم یه پیام رو به همه کلاینت‌ها میفرسته
    def send_message_to_all_clients(self, message):
        for conn in self.player_connections:
            try:
                conn.sendall(message.encode('utf-8'))
            except socket.error:
                # اگه اتصال قطع بود، ایرادی نداره
                pass

    # تابع اصلی که سرور رو راه میندازه
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        print(f"سرور بازی روی {HOST}:{PORT} منتظر بازیکنان است...")

        # دوتا بازیکن رو قبول میکنیم
        for i in range(2):
            conn, addr = server_socket.accept()
            if i == 0:
                player = Player.Player("بازیکن 1", "X")
            else:
                player = Player.Player("بازیکن 2", "O")

            # اطلاعات بازیکن و اتصالش رو ذخیره می‌کنیم
            self.player_connections.append(conn)
            self.players.append(player)
            print(f" {player.name} از {addr} متصل شد.")

            # هر بازیکن رو تو یه نخ جدا میذاریم تا کارش رو انجام بده
            client_thread = threading.Thread(target=self.handle_client, args=(conn, i))
            client_thread.start()

        print("بازی شروع شد!")
        # وضعیت اولیه تخته رو میفرستیم
        self.send_board_to_all_clients()

if __name__ == "__main__":
    game_server = GameServer()
    game_server.start()