import socket
import threading
import base64
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000
LOG_FILE = "./chat_log.txt"

def encrypt(msg):
    return base64.b64encode(msg.encode()).decode()

def decrypt(msg):
    return base64.b64decode(msg.encode()).decode()

def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def handle_client(conn, addr):
    username_enc = conn.recv(1024).decode()
    username = decrypt(username_enc)

    print(f"[+] {username} connected from {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        message = decrypt(data)

        if message.lower() == "exit":
            print(f"[-] {username} disconnected")
            break

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {username}: {message}"

        print(full_message)
        log_message(full_message)

        reply = encrypt("Message received")
        conn.sendall(reply.encode())

    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("Server running on port", PORT)

while True:
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
