import socket

import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8080))

server.listen(1)

print("Server listening on port 8080. Waiting for client......")

client_socket, client_address = server.accept()

print(f"Connected to {client_address}")

print(f"Client message 1: {client_socket.recv(1024).decode("utf-8")}")
print(f"Client message 2: {client_socket.recv(1024).decode("utf-8")}")


client_socket.close()

server.close()
