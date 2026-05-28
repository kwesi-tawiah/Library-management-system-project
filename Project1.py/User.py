import socket

import re

import pickle

import time

def signin(user_id):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(("127.0.0.1", 3001))

        message = pickle.dumps(f"(SIGNIN) / ({user_id})")
        length = len(message)
        client.send(pickle.dumps(length))
        time.sleep(1)
        client.send(message)

        length = pickle.loads(client.recv(1024))
        message = pickle.loads(client.recv(length))

        if message.lower() == "please sign up":
            return False
        elif message.lower() == "please continue":
            return True

class User():
        

    def __init__(self):
        self.id = None
        answer1 = "signup"
        answer2 = "signin"
        answer = None

        while True:
            ask = input("Do you want to sign up or sign in?(signup or signin) ")

            if ask.replace(" ", "").lower() == answer1:
                 answer = "yes"
                 break
            elif ask.replace(" ", "").lower() == answer2:
                while True:
                    user_id = input("Enter you id: ")
                    if user_id.replace(" ", "").isalpha():
                        print("Please enter valid user number.")
                        continue
                    else:
                        break
                #_id = int(user_id)
                if signin(user_id):
                    return
                else:
                    answer = "yes"
                    break
            else:
                continue   

        if answer.lower() == "yes":
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client.connect(("127.0.0.1", 3001))
            while True:

                name = input("Enter name: ")
                sex = input("Enter sex: ")
                email = input("Enter email: ")
                phone_number = input("Phone_number: ")
                pattern = r"^[A-Za-z0-9_%+\-]+(?:\.[A-Za-z0-9_%+\-]+)*@[A-Za-z0-9\-]+(?:\.[A-Za-z]{2,})+$"

                if not name.replace(" ", "").isalpha() or not sex.isalpha():
                    print("Please enter only letters for the name and sex. Try again.")
                    continue
                elif sex.lower() not in ["female", "male"]:
                    print("Sex must be male or female. Please try again")
                    continue
                elif not phone_number.isdigit():
                    print("Please enter only numbers for the phone number. Try again.")
                    continue
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
                    data = pickle.loads(client.recv(1024))
                    if not data:
                        print("Server not active!")
                        return
                    if data == "ne":
                        length = pickle.loads(client.recv(1024))
                        data = pickle.loads(client.recv(length))
                        print(
                            f"Your library id is {data}. Please keep it in mind.")
                        self.id = data
                        break
                    elif data == "al":
                        length = pickle.loads(client.recv(1024))
                        data = pickle.loads(client.recv(length))
                        print(data)
                        break
                    elif data == "nr":
                        length = pickle.loads(client.recv(1024))
                        data = pickle.loads(client.recv(length))
                        print(data)
                        break
                    elif data == "de":
                        length = pickle.loads(client.recv(6))
                        data = pickle.loads(client.recv(length))
                        print(data)
                        break
                client.close()
        elif answer.replace(" ", "").lower() == "no":
            print("Okay, have a great day!")
        else:
            print("Please enter the right answer.")

    def show_library_books(self):
        if not self.id:
            print("You do not have a user name or user id. Please sign up first.")
            return
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(("127.0.0.1", 3001))
        request = pickle.dumps(
            f"(SHOW) / A user named ({self.name}) want to see books available.")
        length = len(request)

        client.send(pickle.dumps(length))
        time.sleep(1)
        client.send(request)

        correct = pickle.loads(client.recv(1024))
        
        length = pickle.loads(client.recv(1024))

        data = pickle.loads(client.recv(length))
        if correct and correct.lower() == "pass":
            if data and isinstance(data, list) and hasattr(data[0], "book_state"):
                for book in data:
                    book.book_state()
            elif data and isinstance(data, list):
                print("BOOKS:")
                for book in data:
                    print(f"""
Book_name: {book[1]}
Year: {book[2]}
Author: {book[3]}
Borrow_time: {book[4]}
Borrowed: {book[5]}""")
        elif correct and correct.lower() == "deny":
            if data:
                print(data)
            
        client.close()

    def borrow_book(self, title):
        if not self.id:
            print("You are not signed up or user id. Please sigh up first.")
            return
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(("127.0.0.1", 3001))
        request = pickle.dumps(
            f"(BORROW) / A user named ({self.name}) wants to borrow the book titled ({title}).")
        length = len(request)
        client.send(pickle.dumps(length))
        time.sleep(1)
        client.send(request)
        time.sleep(1)
        client.send(pickle.dumps(self.id))
        #time.sleep(1)
        length = pickle.loads(client.recv(1024))
        data = pickle.loads(client.recv(length))
        print(data)

        client.close()

    def return_book(self, title):
        if not self.id:
            print("You are not signed up or user id. Please sigh up first.")
            return
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(("127.0.0.1", 3001))
        request = pickle.dumps(
            f"(RETURN) / A user named ({self.name}) want to return the book titled ({title}).")
        length = len(request)
        client.send(pickle.dumps(length))
        time.sleep(1)
        client.send(request)
        time.sleep(1)
        client.send(pickle.dumps(self.id))
        length = pickle.loads(client.recv(1024))
        data = pickle.loads(client.recv(length))
        print(data)
        client.close()

User1 = User()


User1.show_library_books()
    
User1.borrow_book("Physics")

#User2 = User()

User1.show_library_books()
#User2.return_book("Physics")

User1.return_book("Physics")

User1.show_library_books()

print(User1.id)
