import socket

HOST = '127.0.0.1'
PORT = 65432

server_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_soket.bind((HOST, PORT))

server_soket.listen(2)

while True:
    client_soket, client_addr = server_soket.accept()
    while True:
        try:
            data = client_soket.recv(1024)
            if not data:
                break
        except :
            break

    client_soket.close()

server_soket.close()

