import socket
import threading

HOST = '127.0.0.1'
PORT = 65432


# این تابع در یک thread جداگانه اجرا میشه تا پیام‌ها رو دریافت کنه
def receive_messages(sock):
    while True:
        try:
            # دریافت داده‌ها از سرور
            data = sock.recv(1024).decode('utf-8')
            if not data:
                print("ارتباط با سرور قطع شد.")
                break

            # نمایش پیام دریافتی
            print(data)

            # اگر سرور پیام 'نوبت شماست' رو فرستاد، یک پرامپت برای ورودی چاپ کن
            if "نوبت شماست" in data:
                print(">>> ", end='', flush=True)

        except (socket.error, ConnectionResetError):
            print("ارتباط قطع شد.")
            break


# تابع اصلی که کلاینت رو اجرا می‌کنه
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # تلاش برای اتصال به سرور
        client_socket.connect((HOST, PORT))
        print("به سرور بازی دوز وصل شدید.")

        # یک thread برای دریافت پیام‌ها ایجاد و شروع می‌کنه
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True  # این خط باعث میشه برنامه با پایان thread اصلی، تموم بشه
        receive_thread.start()

        # حلقه اصلی برای ارسال ورودی کاربر
        while True:
            # گرفتن ورودی از کاربر
            move = input()
            # ارسال ورودی به سرور
            client_socket.sendall(move.encode('utf-8'))

    except ConnectionRefusedError:
        print("اتصال به سرور برقرار نشد. لطفا مطمئن شوید سرور در حال اجراست.")
    except (socket.error, ConnectionResetError):
        print("ارتباط قطع شد.")
    finally:
        # در نهایت، سوکت رو می‌بندیم
        client_socket.close()


if __name__ == "__main__":
    main()