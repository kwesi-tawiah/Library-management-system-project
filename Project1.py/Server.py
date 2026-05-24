import re

import pickle

import socket

import Database

import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8080))

server.listen(1)

client_socket, client_address = server.accept()

print("Listening for users.....")

users = []


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
        time.sleep(1)
        client_socket.send(pickle.dumps(length))
        time.sleep(1)
        client_socket.send(message)


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
                        time.sleep(1)
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
                time.sleep(1)
                length = len(pickle.dumps(user_id))
                client_socket.send(pickle.dumps(length))
                time.sleep(1)
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
                    time.sleep(1)
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
                            time.sleep(1)
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
                        time.sleep(1)
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
            time.sleep(1)
            client_socket.send(message)
    else:
        message = pickle.dumps("There are no books in library.")
        length = len(message)
        client_socket.send(pickle.dumps(length))
        time.sleep(1)
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
                    time.sleep(1)
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
                            time.sleep(1)
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
                        time.sleep(1)
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
            time.sleep(1)
            client_socket.send(message)
    else:
        message = pickle.dumps("There is no book in library.")
        length = len(message)
        client_socket.send(pickle.dumps(length))
        time.sleep(1)
        client_socket.send(message)


def approval():
    while True:
        approve = input("Do you approve?(yes/no): ")
        if approve.lower() == "yes":
            return True
        elif approve.lower() == "no":
            return False
        else:
            continue


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

        # if not cont():
        #    break

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
            if approval():
                if users:
                    for user in users:
                        if user["name"] == (search[1].group(1)):
                            show_user_books()
                            break
                        else:
                            continue
                    else:
                        message = pickle.dumps(
                            "Please sign up first to see library books.")
                        length = len(message)
                        client_socket.send(pickle.dumps("deny"))
                        # time.sleep(1)
                        client_socket.send(pickle.dumps(length))
                        # time.sleep(1)
                        client_socket.send(message)
                else:
                    message = pickle.dumps(
                        "Please sign up first to see library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    # time.sleep(1)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)

            else:
                message = pickle.dumps(
                    "Sorry your request was disapproved.")
                length = len(message)
                client_socket.send(pickle.dumps("deny"))
                # time.sleep(1)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "borrow":
            title = search[2].group(1)
            user_name = search[1].group(1)
            print(data[9:])
            if approval():
                # pattern = r"\((\d+)\)"
                user_id = pickle.loads(client_socket.recv(10))
                # match = re.search(pattern, rev, re.I)
                # user_id = int(match.group(1))
                if user_id:
                    borrow_book(title, user_name, user_id)
                else:
                    message = pickle.dumps(
                        "Please signup to access library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)
            else:
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "signup":
            print("A user wants to sign up")
            if approval():
                text = data[9:]
                pattern = r"(\d*[A-Za-z][A-Za-z_%&$?+]*\d*[@gmail.com]*)|\d+"
                search = list(re.finditer(pattern, text, re.I))
                if search:
                    add_user(search[0].group(1), search[1].group(
                        1), search[2].group(1), search[3].group(1))
                else:
                    client_socket.send(pickle.dumps("nr"))
                    message = pickle.dumps(
                        "Your sign up info was not received. Please try again.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)

            else:
                client_socket.send(pickle.dumps("de"))
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "return":
            title = search[2].group(1)
            user_name = search[1].group(1)
            print(data[9:])
            if approval():
                # pattern = r"\((\d+)\)"
                # rev = client_socket.recv(10).decode("utf-8")
                # match = re.search(pattern, rev, re.I)
                user_id = pickle.loads(client_socket.recv(10))
                if user_id:
                    return_book(title, user_name, user_id)
                else:
                    message = pickle.dumps(
                        "Please signup to access library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)

            else:
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        else:
            continue
