import socket
import threading
import base64
from datetime import datetime
#Broadcast_Server
HOST = '0.0.0.0'
PORT = 5000
LOG_FILE = "./broadcast_chat_log.txt"

clients = []  
clients_lock = threading.Lock()

def encrypt(msg):
    return base64.b64encode(msg.encode()).decode()

def decrypt(msg):
    return base64.b64decode(msg.encode()).decode()

def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def broadcast(message, sender_conn):
    """Send message to all clients except the sender"""
    with clients_lock:
        for client_conn, client_username in clients:
            if client_conn != sender_conn:
                try:
                    encrypted_msg = encrypt(message)
                    client_conn.sendall(encrypted_msg.encode())
                except:
                   
                    clients.remove((client_conn, client_username))

def handle_client(conn, addr):
    username = None
    try:
        
        username_enc = conn.recv(1024).decode()
        username = decrypt(username_enc)
        print(f"[+] {username} connected from {addr}")
        
        
        with clients_lock:
            clients.append((conn, username))
        
        
        join_msg = f"{username} has joined the chat!"
        broadcast(join_msg, conn)
        log_message(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {join_msg}")
        
       
        welcome = encrypt(f"Welcome to the chat, {username}! There are {len(clients)} users online.")
        conn.sendall(welcome.encode())
        
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
            
            
            broadcast(f"{username}: {message}", conn)
            
           
            reply = encrypt("Message sent to all users")
            conn.sendall(reply.encode())
    
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    
    finally:
        
        if username:
            with clients_lock:
                clients[:] = [(c, u) for c, u in clients if c != conn]
            
           
            leave_msg = f"{username} has left the chat"
            broadcast(leave_msg, conn)
            log_message(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {leave_msg}")
        
        conn.close()

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server running on port {PORT}")
    
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

except OSError as e:
    print(f"Server error: {e}")
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server_socket.close()