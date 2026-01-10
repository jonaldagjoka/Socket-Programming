import socket
import threading
import base64

HOST = '192.168.133.34'
PORT = 5000

def encrypt(msg):
    return base64.b64encode(msg.encode()).decode()

def decrypt(msg):
    return base64.b64decode(msg.encode()).decode()

def receive_messages(sock):
    """Thread to continuously receive messages from server"""
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            message = decrypt(data)
            print(f"\n{message}")
            print("Message: ", end="", flush=True)  # Re-prompt
        except:
            break

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    username = input("Enter username: ")
    client_socket.sendall(encrypt(username).encode())
    
    # Start thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()
    
    print("\nYou can now start chatting! Type 'exit' to quit.\n")
    
    while True:
        message = input("Message: ")
        client_socket.sendall(encrypt(message).encode())
        
        if message.lower() == "exit":
            break

except ConnectionRefusedError:
    print("Could not connect to server. Make sure the server is running.")
except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()
    print("Disconnected from chat.")
