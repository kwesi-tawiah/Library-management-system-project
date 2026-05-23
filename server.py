import socket

import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8080))

server.listen(1)

print("Server listening on port 8080. Waiting for client......")

client_socket, client_address = server.accept()

print(f"Connected to {client_address}")

name = "Bruce"
want = "wants to test"
some = "something"

lists = [(name, want, some), ("Christopher Bruce", "17", "Pku")]
num = pickle.dumps(10000)
client_socket.send(pickle.dumps(len(num)))
client_socket.send(num)

client_socket.send(str(10).encode())


print(f"{client_socket.recv(1024).decode()}")


client_socket.send(str(2.3).encode())

client_socket.close()

server.close()
