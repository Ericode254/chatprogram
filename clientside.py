import socket
import threading

DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT: int = 12345
ENCODER: str = "utf-8"
BYTESIZE: int = 1024

alias = input("Choose an alias >>> ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

def send_message():
    while True:
        message = f"{alias}: {input('')}"
        client_socket.send(message.encode(ENCODER))

def receive_message():
    while True:
        try:
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            if message == "alias?":
                client_socket.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error")
            client_socket.close()
            break
        
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
