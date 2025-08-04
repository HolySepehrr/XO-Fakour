import socket
import threading
from Board import Board
from Player import Player

HOST = "127.0.0.1"
PORT = 65432


class GameServer:

    def __init__(self):
        self.board = Board()
        self.players = []
        self.player_connections = []
        self.current_player_index = 0
        self.game_over = False
        self.lock = threading.Lock()
        # این barrier تضمین می‌کنه که بازی تا وقتی دو بازیکن وصل نشدن، شروع نشه
        self.barrier = threading.Barrier(2)

    def handle_client(self, conn, player_index):
        player = self.players[player_index]
        conn.sendall(f"به بازی خوش آمدی! شما بازیکن {player.name} و نماد شما {player.symbol} هستید.".encode('utf-8'))

        # اینجا منتظر می‌مونیم تا بازیکن دوم وصل بشه
        self.barrier.wait()

        # بعد از اینکه هر دو بازیکن وصل شدن، بهشون پیام می‌دیم که بازی شروع شده
        if player_index == 0:
            self.send_message_to_all_clients("بازی شروع شد!")
            self.send_board_to_all_clients()

        while not self.game_over:
            if self.current_player_index == player_index:
                conn.sendall(f"نوبت شماست، حرکت خود را وارد کنید (1-9) ".encode('utf-8'))

                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        print("اتصال قطع شد:(")
                        break

                    with self.lock:
                        if self.game_over:
                            break
                        try:
                            move = int(data)
                            if 0 < move < 10:
                                row, col = (move - 1) // 3, (move - 1) % 3

                                if self.board.is_valid_move((row, col)):
                                    self.board.makes_move(player.symbol, (row, col))
                                    self.send_board_to_all_clients()

                                    if self.board.check_win((row, col)):
                                        self.game_over = True
                                        self.send_message_to_all_clients(f"خب خب، {player.name} برد")
                                    elif self.board.is_full():
                                        self.game_over = True
                                        self.send_message_to_all_clients("مساوی کردید به سلامتی")
                                    else:
                                        self.current_player_index = (self.current_player_index + 1) % 2
                                        self.send_message_to_all_clients(
                                            f"نوبت بازیکن {self.players[self.current_player_index].name} است.")
                                else:
                                    conn.sendall("این خانه پر است، لطفاً خانه دیگری انتخاب کنید.".encode('utf-8'))
                            else:
                                conn.sendall("ورودی نامعتبر است، یک عدد بین 1 تا 9 وارد کنید.".encode('utf-8'))
                        except ValueError:
                            conn.sendall("ورودی نامعتبر است، یک عدد بین 1 تا 9 وارد کنید.".encode('utf-8'))

                except (socket.error, ConnectionResetError):
                    print(f"ارتباط با بازیکن {player.name} قطع شد.")
                    self.game_over = True
                    self.send_message_to_all_clients(f"بازیکن {player.name} قطع شد. بازی به پایان رسید.")
                    break

        conn.close()

    def send_board_to_all_clients(self):
        board_str = "\n".join([" ".join(row) for row in self.board.map])
        message = f"وضعیت جدید تخته:\n{board_str}"
        self.send_message_to_all_clients(message)

    def send_message_to_all_clients(self, message):
        for conn in self.player_connections:
            try:
                conn.sendall(message.encode('utf-8'))
            except socket.error:
                pass

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        print(f"سرور بازی روی {HOST}:{PORT} منتظر بازیکنان است...")

        for i in range(2):
            conn, addr = server_socket.accept()
            if i == 0:
                player = Player("بازیکن 1", "X")
            else:
                player = Player("بازیکن 2", "O")

            self.player_connections.append(conn)
            self.players.append(player)
            print(f" {player.name} از {addr} متصل شد.")

            client_thread = threading.Thread(target=self.handle_client, args=(conn, i))
            client_thread.start()

        print("هر دو بازیکن متصل شدند. بازی در حال شروع است...")


if __name__ == "__main__":
    game_server = GameServer()
    game_server.start()