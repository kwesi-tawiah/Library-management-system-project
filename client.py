import socket

import pickle


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 8080))

print("Connected to server")
length = pickle.loads(client.recv(5))
data = pickle.loads(client.recv(length))

print(data)

num = client.recv(2).decode()
print(f"{int(num)}")


client.send("Hey server, loud and clear.".encode())

print(client.recv(5).decode())

client.close()
