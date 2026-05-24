import socket

import pickle

import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 8080))

print("Connected to server")

client.send(
    "Hello server! Can you hear me? I want to communicate with youjfmgkjrsdbgkjsrg skjbgjs adskjbgjs djgnsjksg sglngjsgnkjfgms gnshgnjfjgsj sgjlfngsj.".encode("utf-8"))
time.sleep(1)
client.send("This client message two.".encode("utf-8"))

print(client.recv(5).decode())

client.close()
