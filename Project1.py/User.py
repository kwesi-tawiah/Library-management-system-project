import socket

import re

import pickle

import time
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 8080))


class User():

    def __init__(self):
        self.id = None
        question = input("Do you want to sign up?(yes/no) ")

        if question.lower() == "yes":

            while True:

                name = input("Enter name: ")
                email = input("Enter email: ")
                sex = input("Enter sex: ")
                phone_number = input("Phone_number: ")
                pattern = r"^\d*[A-Za-z][A-Za-z_%!+&$?]*\d+@gmail.com$"

                if not name.isalpha() or not sex.isalpha():
                    print("Please enter only letters for the name and sex. Try again.")
                    continue
                elif sex.lower() not in ["female", "male"]:
                    print("Sex must be male or female. Please try again")
                elif not phone_number.isdigit():
                    print("Please enter only numbers for the phone number. Try again.")
                elif len(phone_number) > 10 or len(phone_number) < 10:
                    print("Please enter ten digits for the phone number. Try again.")
                    continue
                elif not re.search(pattern, email, re.I):
                    print("Please enter a valid email. Try again.")
                    continue

                else:
                    self.name = name
                    self.sex = sex
                    self.email = email
                    self.phone_number = phone_number
                    request = pickle.dumps(
                        f"(SIGNUP) ({name},{sex},{email},{phone_number})")
                    length = len(request)
                    client.send(pickle.dumps(length))
                    time.sleep(1)
                    client.send(request)
                    time.sleep(1)
                    data = pickle.loads(client.recv(20))
                    if not data:
                        print("Server not active!")
                        return
                    if data == "ne":
                        length = pickle.loads(client.recv(6))
                        data = pickle.loads(client.recv(length))
                        print(
                            f"Your library id is {data}. Please keep it in mind.")
                        self.id = data
                        break
                    elif data == "al":
                        length = pickle.loads(client.recv(6))
                        data = pickle.loads(client.recv(length))
                        print(data)
                        break
                    elif data == "nr":
                        length = pickle.loads(client.recv(6))
                        data = pickle.loads(client.recv(length))
                        break
                    elif data == "de":
                        length = pickle.loads(client.recv(6))
                        data = pickle.loads(client.recv(length))

        else:
            print("Okay, have a great day!")

    def show_library_books(self):
        request = pickle.dumps(
            f"(SHOW) / A user named ({self.name}) want to see books available.")
        length = len(request)

        client.send(pickle.dumps(length))
        time.sleep(1)
        client.send(request)
        correct = pickle.loads(client.recv(30))
        length = pickle.loads(client.recv(10))

        data = pickle.loads(client.recv(length))
        if correct and correct.lower() == "pass":
            for book in data:
                book.book_state()
            return
        if isinstance(data, str):
            print(data)
        elif isinstance(data, list):
            print("BOOKS:")
            for book in data:
                print(f"""
Book_name: {book[1]}
Year: {book[2]}
Author: {book[3]}
Borrow_time: {book[4]}
Borrowed: {book[5]}""")

    def borrow_book(self, title):
        request = pickle.dumps(
            f"(BORROW) / A user named ({self.name}) wants to borrow the book titled ({title}).")
        length = len(request)
        client.send(pickle.dumps(length))
        client.send(request)
        client.send(pickle.dumps(self.id))
        length = pickle.loads(client.recv(6))
        data = pickle.loads(client.recv(length))
        print(data)

    def return_book(self, title):
        request = pickle.dumps(
            f"(RETURN) / A user named ({self.name}) want to return the book titled ({title}).")
        length = len(request)
        client.send(pickle.dumps(length))
        client.send(request)
        client.send(pickle.dumps(self.id))
        length = pickle.loads(client.recv(6))
        data = pickle.loads(client.recv(length))
        print(data)


User1 = User()

User1.show_library_books()

User1.borrow_book("Physics")

User1.return_book("Physics")

User1.show_library_books()
