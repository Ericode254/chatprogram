import socket
import threading

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT: int = 12345
ENCODER: str = "utf-8"
BYTESIZE: int = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

clients = []
alliases = []

def broadcast_message(message):
    for client in clients:
        client.send(message)

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(BYTESIZE)
            broadcast_message(message)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            alias = alliases[index]
            broadcast_message(f"{alias} has left the chatroom!".encode(ENCODER))
            alliases.remove(alias)
            break

def connect_client():
    print("Server is running and listening....")
    client_name, client_address = server_socket.accept()
    print(f"Connetion is established with {str(client_address)}")
    client_name.send("alias?".encode(ENCODER))
    alias = client_name.recv(BYTESIZE)
    alliases.append(alias)
    clients.append(client_name)
    print(f"The alias of this client is {alias}".encode(ENCODER))
    broadcast_message(f"{alias} has connected to the chat room".encode(ENCODER))
    client_name.send("You are now connected!".encode(ENCODER))
    thread = threading.Thread(target = receive_message, args=(client_name,))
    thread.start()
    
if __name__ == "__main__":
    connect_client()
    