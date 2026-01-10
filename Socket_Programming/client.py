import socket
import base64
from datetime import datetime

HOST = '192.168.8.150'
PORT = 5000

def encrypt(msg):
    return base64.b64encode(msg.encode()).decode()

def decrypt(msg):
    return base64.b64decode(msg.encode()).decode()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input("Enter username: ")
client_socket.sendall(encrypt(username).encode())

while True:
    message = input("Message: ")
    client_socket.sendall(encrypt(message).encode())

    if message.lower() == "exit":
        break

    response = decrypt(client_socket.recv(1024).decode())
    print("Server:", response)

client_socket.close()
