# HANDLE ALL MESSAGE TRANSFERS. MAKE THEM PICKLE
import re

import time

import Books

import socket

import Database

import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8080))

server.listen(1)

client_socket, client_address = server.accept()

print("Listening for users.....")


class Library:

    def load_books(self):
        count = 0
        while count < 3:
            books, fault = None, None
            books, fault = Database.load_books()
            if books and not fault:
                if self.users:
                    for b in books:
                        for book in self.books:
                            if book.title == b[0] and book.author == b[2]:
                                break
                        else:
                            book = Books.Book()
                            book.title = b[0]
                            book.year = b[1]
                            book.author = b[2]
                            book.borrow_time = b[3]
                            if b[4].lower() == "yes":
                                book.borrowed = True
                            elif b[4].lower() == "no":
                                book.borrowed = False
                                self.books.append(book)
                else:
                    for b in books:
                        book = Books.Book()
                        book.title = b[0]
                        book.year = b[1]
                        book.author = b[2]
                        book.borrow_time = b[3]
                        if b[4].lower() == "yes":
                            book.borrowed = True
                        elif b[4].lower() == "no":
                            book.borrowed = False
                        self.books.append(book)

                break
            elif not books and not fault:
                print("There is no book in library.")
                break
            elif not books and fault:
                continue
            count += 1
        else:
            print("There are no books to load into library.")

    def load_users(self):
        count = 0
        while count < 3:
            users, fault = None, None
            users, fault = Database.load_users()
            if users and not fault:
                if self.users:
                    for u in users:
                        for us in self.users:
                            if u[1] == us["name"] and u[0] == us["id"]:
                                break
                        else:
                            user = {}
                            user["name"] = u[1]
                            user["id"] = u[0]
                else:
                    for u in users:
                        user = {}
                        user["name"] = u[1]
                        user["id"] = u[0]

                break
            elif not users and not fault:
                print("There is no users signed up.")
                break
            elif not users and fault:
                continue
            count += 1
        else:
            print("There are no signed up users yet.")

    def create_tables(self):
        one = Database.create_table("users")
        two = Database.create_table("borrow_history")
        three = Database.create_table("books")
        self.true_count = 0
        count = 0
        while count < 3:
            if one:
                one = Database.create_table("users")
            else:
                self.true_count += 1
            if two:
                two = Database.create_table("borrow_history")
            else:
                self.true_count += 1
            if three:
                three = Database.create_table("books")
            else:
                self.true_count += 1

            if self.true_count == 3:
                self.true_count = 0
                print("Tables created.")
                break
            else:
                self.true_count = 0
                count += 1
                continue
        else:
            print("Tables could not be created.")

    def __init__(self):
        self.books = []
        self.users = []
        self.true_count = 0

    def add_book(self, title, year, author, borrow_time):
        if self.books:
            for book in self.books:
                if book.title == title and book.year == year and book.author == author:
                    print("This book is already in library.")
                    break
            else:
                book = Books.Book(title, year, author, borrow_time)
                _id = Database.insert_into_books(
                    title, year, author, borrow_time)
                book.id = _id
                self.books.append(book)

    def add_user(self, name, sex, email, phone_number):
        count = 0
        while count < 3:
            user_id = None
            user_id = Database.insert_into_users(
                name, sex, email, phone_number)
            if user_id:
                if self.users:
                    for user in self.users:
                        if user["name"] == name and user["id"] == user_id:
                            client_socket.send(pickle.dumps("al"))
                            message = pickle.dumps(
                                "You are already signed up.")
                            length = len(message)
                            client_socket.send(pickle.dumps(length))
                            client_socket.send(message)
                            print("This user has already signed up.")
                            break
                        else:
                            continue
                    break

                else:
                    user = {"name": name, "id": user_id}
                    self.users.append(user)
                    print("User added successfully.")
                    client_socket.send(pickle.dumps("ne"))
                    length = len(pickle.dumps(user_id))
                    client_socket.send(pickle.dumps(length))
                    client_socket.send(pickle.dumps(user_id))
            else:
                count += 1
                continue

    def borrow_book(self, book_name, user_name, user_id):
        if self.books:
            for book in self.books:
                if book.title.lower() == book_name.lower():
                    if book.borrowed == True:
                        message = pickle.dumps(
                            f"{book.title.capitalize()} is not available.")
                        length = len(message)
                        client_socket.send(length)
                        client_socket.send(message)
                    elif book.borrowed == False:
                        book.borrow()
                        datetime_borrowed = book.datetime_borrowed
                        count = 0
                        while count < 3:
                            further = None
                            further = Database.insert_into_borrow_history_b(
                                user_name, user_id, book_name, datetime_borrowed)
                            if further:
                                message = pickle.dumps(
                                    "Borrow action was succesful, Happy reading!")
                                length = len(message)
                                client_socket.send(pickle.dumps(length))
                                client_socket.send(message)
                                break
                            else:
                                count += 1
                                continue

                        else:
                            message = pickle.dumps(
                                "Sorry, your borrow action was not succesful please try again later.")
                            length = len(message)
                            client_socket.send(pickle.dumps(length))
                            client_socket.send(message)
                            break
                        break
                else:
                    continue
            else:
                message = pickle.dumps(
                    f"{book_name.capitalize()} is not in this library.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                client_socket.send(message)
        else:
            message = pickle.dumps("There are no books in library.")
            length = len(message)
            client_socket.send(pickle.dumps(length))
            client_socket.send(message)

    def return_book(self, book_name, user_name, user_id):
        if self.books:
            for book in self.books:
                if book.title.lower() == book_name.lower():
                    if book.borrowed == False:
                        message = pickle.dumps(
                            f"{book.name.capitalize()} is not borrowed from this library.")
                        length = len(message)
                        client_socket.send(pickle.dumps(length))
                        client_socket.send(message)
                        break
                    elif book.borrowed == True:
                        book.return_book()
                        datetime_returned = book.returned_time
                        book_borrowed = book.title
                        count = 0
                        while count < 3:
                            further = None
                            further = Database.update_borrow_history_r(
                                user_name, user_id, datetime_returned, book_borrowed)
                            if not further:
                                message = pickle.dumps(
                                    "{book.title.capitalize()} successfully returned to library.")
                                length = len(message)
                                client_socket.send(pickle.dumps(length))
                                client_socket.send(message)
                                break
                            else:
                                count += 1
                                continue
                        else:
                            message = pickle.dumps(
                                "Sorry, your return action was not succesful please try again later.")
                            length = len(message)
                            client_socket.send(pickle.dumps(length))
                            client_socket.send(message)
                            break
                        break
                else:
                    continue
            else:
                message = pickle.dumps(
                    f"{book_name.capitalize()} is not a book of this library.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                client_socket.send(message)
        else:
            message = pickle.dumps("There is no book in library.")
            length = len(message)
            client_socket.send(pickle.dumps(length))
            client_socket.send(message)
# Handle below

    def show_books(self):
        if not self.books:
            count = 0
            while count < 3:
                data, fault = None, None
                data, fault = Database.show_table("books")
                if not data and not fault:
                    print("No books in library.")
                    break
                elif data and not fault:
                    print("BOOKS:")
                    for book in data:
                        if book[5].lower() == "yes":
                            b = True
                        elif book[5].lower() == "no":
                            b = False
                        print(f"""
Boot_id: {book[0]}
Book_name: {book[1]}
Year: {book[2]}
Author: {book[3]}
Borrow_time: {book[4]}
Borrowed: {b}
""")
                    break

                elif not data and fault:
                    continue
            else:
                print("There are no books in the library.")
        else:
            for book in self.books:
                book.book_state()

    def show_user_books(self):
        if not self.books:
            count = 0
            while count < 2:
                data, fault = None, None
                data, fault = Database.show_table("books")
                if not data and not fault:
                    message = pickle.dumps("No books in library.")
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    time.sleep(1)
                    client_socket.send(pickle.dumps((length)))
                    time.sleep(1)
                    client_socket.send(message)
                    break
                elif data and not fault:
                    message = pickle.dumps(data)
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    time.sleep(1)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)
                    break
                elif not data and fault:
                    message = pickle.dumps(
                        "An error occurred. Please try again.")
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    time.sleep(1)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)
                    count += 1
                    continue
            else:
                message = pickle.dumps(
                    "Sorry, we are trying to solve this issue. Please try again later.")
                length = len(message)
                client_socket.send(pickle.dumps("deny"))
                time.sleep(1)
                client_socket.send(message)
                print("(ALERT) A user cannot access books.")
        else:
            message = pickle.dumps(self.books)
            length = len(message)
            client_socket.send(pickle.dumps("pass"))
            client_socket.send(pickle.dumps(length))
            client_socket.send(message)

    def show_users(self):
        count = 0
        while count < 3:
            data, fault = None, None
            data, fault = Database.show_table("users")
            if data and not fault:

                print("USERS:")

                for user in data:
                    print(f"""
User_id: {user[0]}
Name: {user[1]}
Sex: {user[2]}
Email: {user[3]}
Phone_number: {user[4]}
""")
                break

            elif not data and fault:
                continue
            elif not data and not fault:
                print("There are no users.")
                break
            count += 1
        else:
            print("Please try again later.")

    def show_borrow_history(self):
        count = 0
        while count < 3:
            data, fault = None, None
            data, fault = Database.show_table("borrow_history")
            if not data and not fault:
                print("No history.")
                break
            elif data and not fault:

                print("BORROW HISTORY:")

                for user in data:
                    print(f"""
User_id: {user[0]}
Name: {user[1]}
Sex: {user[2]}
Email: {user[3]}
Phone_number: {user[4]}
Book_borrowed: {user[5]}
Datetime_borrowed: {user[6]}
Datetime_returned: {user[7]}
Returned: {user[8]}
""")
                break
            elif not data and fault:
                count += 1
                continue
        else:
            print("There are no users.")

    def show_user_borrow_history(self, name):
        count = 0
        while count < 3:
            data, fault = None, None
            data, fault = Database.show_user_borrow_history(name)
            if not data and not fault:
                print("User not found.")
                break
            elif data and not fault:

                for person in data:
                    print(f"""
User_id: {person[0]}
Name: {person[1]}
Sex: {person[2]}
Email: {person[3]}
Phone_number: {person[4]}
Book_borrowed: {person[5]}
Datetime_borrowed: {person[6]}
Datetime_returned: {person[7]}
Returned: {person[8]}
""")
                break
            elif not data and not fault:
                count += 1
                continue
        else:
            print("There is no history of this user.")

    def approval(self):
        while True:
            approve = input("Do you approve?(yes/no): ")
            if approve.lower() == "yes":
                return True
            elif approve.lower() == "no":
                return False
            else:
                continue


librarian = Library()

librarian.create_tables()
librarian.load_books()
librarian.load_users()

librarian.show_books()

librarian.add_book("Physics", "1990", "Bruce", 2)
librarian.add_book("Chemistry", "2020", "Chris", 3)
librarian.add_book("Mathematic", "1919", "Adjoa", 1)

librarian.show_books()

librarian.show_books()
if client_address[0] != "127.0.0.1":
    print("This user is not of this device.")

elif client_address[0] == "127.0.0.1":

    def cont():
        while True:
            cont = input("Further?: ")
            if cont.lower() == "yes":
                return True
            elif cont.lower() == "no":
                return False
            else:
                continue

    while True:

        if not cont():
            break

        length = pickle.loads(client_socket.recv(50))
        if not length:
            continue

        data = pickle.loads(client_socket.recv(length))

        pattern = r"\(([^)]+)\)"

        search = list(re.finditer(pattern, data, re.I))

        if search:
            request = search[0].group(1)
        else:
            client_socket.send(
                f"Please check your request.".encode("utf-8"))

        if request.lower() == "show":
            print(data[9:])
            if librarian.approval():
                if librarian.users:
                    for user in librarian.users:
                        if user["name"] == (search[1].group(1)):
                            librarian.show_user_books()
                            break
                        else:
                            continue
                    else:
                        message = pickle.dumps(
                            "Please sign up first to see library books.")
                        length = len(message)
                        client_socket.send(pickle.dumps("deny"))
                        time.sleep(1)
                        client_socket.send(pickle.dumps(length))
                        time.sleep(1)
                        client_socket.send(message)
                else:
                    message = pickle.dumps(
                        "Please sign up first to see library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    time.sleep(1)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

            else:
                message = pickle.dumps(
                    "Sorry your request was disapproved.")
                length = len(message)
                client_socket.send(pickle.dumps("deny"))
                time.sleep(1)
                client_socket.send(pickle.dumps(length))
                time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "borrow":
            title = search[2].group(1)
            user_name = search[1].group(1)
            print(data[9:])
            if librarian.approval():
                # pattern = r"\((\d+)\)"
                user_id = pickle.loads(client_socket.recv(10))
                # match = re.search(pattern, rev, re.I)
                # user_id = int(match.group(1))
                if user_id:
                    librarian.borrow_book(title, user_name, user_id)
                else:
                    message = pickle.dumps(
                        "Please signup to access library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)
            else:
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "signup":
            print("A user wants to sign up")
            if librarian.approval():
                text = data[9:]
                pattern = r"(\d*[A-Za-z][A-Za-z_%&$?+]*\d*[@gmail.com]*)|\d+"
                search = list(re.finditer(pattern, text, re.I))
                if search:
                    librarian.add_user(search[0].group(1), search[1].group(
                        1), search[2].group(1), search[3].group(1))
                else:
                    client_socket.send(pickle.dumps("nr"))
                    message = pickle.dumps(
                        "Your sign up info was not received. Please try again.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

            else:
                client_socket.send(pickle.dumps("de"))
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "return":
            title = search[2].group(1)
            user_name = search[1].group(1)
            print(data[9:])
            if librarian.approval():
                # pattern = r"\((\d+)\)"
                # rev = client_socket.recv(10).decode("utf-8")
                # match = re.search(pattern, rev, re.I)
                user_id = pickle.loads(client_socket.recv(10))
                if user_id:
                    librarian.return_book(title, user_name, user_id)
                else:
                    message = pickle.dumps(
                        "Please signup to access library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

            else:
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                time.sleep(1)
                client_socket.send(message)

        else:
            continue
