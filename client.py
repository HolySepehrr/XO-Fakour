import socket

HOST = '127.0.0.1'
PORT = 65432
client_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_soket.connect((HOST, PORT))
