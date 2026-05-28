import re

import pickle

import socket

import Database

import time

import Books

users = []

books = []

def load_books():
        count = 0
        while count < 2:
            bookes, fault = None, None
            bookes, fault = Database.load_books()
            if bookes and not fault:
                if books:
                    for b in bookes:
                        for book in books:
                            if book.title.lower() == b[1].lower() and book.author.lower() == b[3].lower():
                                break
                        else:
                            book = Books.Book(b[1], b[2], b[3], b[4])
                            book.id = b[0]
                            if b[5].lower() == "yes":
                                book.borrowed = True
                            elif b[5].lower() == "no":
                                book.borrowed = False
                            books.append(book)
                else:
                    for b in bookes:
                        book = Books.Book(b[1], b[2], b[3], b[4])
                        book.id = b[0]
                        if b[5].lower() == "yes":
                            book.borrowed = True
                        elif b[5].lower() == "no":
                            book.borrowed = False
                        books.append(book)

                break
            elif not bookes and not fault:
                print("There are no book in library.")
                break
            elif not bookes and fault:
                continue
            count += 1
        else:
            print("There are no books in library.")

def load_users():
        count = 0
        while count < 2:
            userss, fault = None, None
            userss, fault = Database.load_users()
            if userss and not fault:
                if users:
                    for u in userss:
                        for us in users:
                            if u[1] == us["name"] and u[0] == us["id"]:
                                break
                        else:
                            user = {}
                            user["name"] = u[1]
                            user["id"] = u[0]
                            users.append(user)
                else:
                    for u in userss:
                        user = {}
                        user["name"] = u[1]
                        user["id"] = u[0]
                        users.append(user)

                break
            elif not userss and not fault:
                print("There are no users signed up.")
                break
            elif not userss and fault:
                continue
            count += 1
        else:
            print("There are no signed up users yet.")

def show_user_books():
    if not books:
        count = 0
        while count < 2:
            data, fault = None, None
            data, fault = Database.show_table("books")
            if not data and not fault:
                message = pickle.dumps("No books in library.")
                length = len(message)
                client_socket.send(pickle.dumps("deny"))
                #time.sleep(1)
                client_socket.send(pickle.dumps((length)))
                #time.sleep(1)
                client_socket.send(message)
                break
            elif data and not fault:
                message = pickle.dumps(data)
                length = len(message)
                client_socket.send(pickle.dumps("pass"))
                #time.sleep(1)
                client_socket.send(pickle.dumps(length))
                #time.sleep(1)
                client_socket.send(message)
                break
            elif not data and fault:
                message = pickle.dumps(
                    "An error occurred. Please try again.")
                length = len(message)
                client_socket.send(pickle.dumps("deny"))
                #time.sleep(1)
                client_socket.send(pickle.dumps(length))
                #time.sleep(1)
                client_socket.send(message)
                count += 1
                continue
        else:
            message = pickle.dumps(
                "Sorry, we are trying to solve this issue. Please try again later.")
            length = len(message)
            client_socket.send(pickle.dumps("deny"))
            client_socket.send(pickle.dumps(length))
            #time.sleep(1)
            client_socket.send(message)
            print("(ALERT) A user cannot access books.")
    else:
        message = pickle.dumps(books)
        length = len(message)
        client_socket.send(pickle.dumps("pass"))
        time.sleep(1)
        client_socket.send(pickle.dumps(length))
        time.sleep(1)
        client_socket.send(message)

def add_user(name, sex, email, phone_number, client_socket):
    count = 0
    while count < 2:
        user_id = None
        #print(f"name: {name}, sex: {sex}, phone_number: {phone_number}, email: {email}")
        user_id = Database.insert_into_users(
            name, sex, email, phone_number)
        if user_id:
            if users:
                exists = False
                for user in users:
                    if user["name"] == name and user["id"] == user_id:
                        exists = True
                        
                        #client_socket.close()
                        print("This user has already signed up.")
                        break
                    else:
                        continue
                if exists:
                    client_socket.send(pickle.dumps("al"))
                    message = pickle.dumps(
                            "You are already signed up.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)
                else:
                    user = {"name": name, "id": user_id}
                    users.append(user)
                    print("User added successfully.")
                    client_socket.send(pickle.dumps("ne"))
                    time.sleep(1)
                    length = len(pickle.dumps(user_id))
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(pickle.dumps(user_id))
                    #client_socket.close()
                break

            else:
                user = {"name": name, "id": user_id}
                users.append(user)
                print("User added successfully.")
                client_socket.send(pickle.dumps("ne"))
                time.sleep(1)
                length = len(pickle.dumps(user_id))
                client_socket.send(pickle.dumps(length))
                time.sleep(1)
                client_socket.send(pickle.dumps(user_id))
                break
        else:
            count += 1
            continue

def borrow_book(book_name, user_name, user_id, client_socket):
    if books:
        for book in books:
            if book.title.lower() == book_name.lower():
                if book.borrowed == True:
                    message = pickle.dumps(
                        f"{book.title.capitalize()} is not available.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)
                elif book.borrowed == False:
                    book.borrow()
                    datetime_borrowed = book.datetime_borrowed
                    count = 0
                    while count < 3:
                        further = None
                        #print(datetime_borrowed)
                        print(f"""
User_name: {user_name}
User_id: {user_id}
Book_borrowed: {book_name}
Datetime_borrowed: {datetime_borrowed}""")
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

def return_book(book_name, user_name, user_id, client_socket):
    if books:
        for book in books:
            if book.title.lower() == book_name.lower():
                if book.borrowed == False:
                    message = pickle.dumps(
                        f"{book.title.capitalize()} is not borrowed from this library.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)
                    break
                elif book.borrowed == True:
                    u_id = None
                    u_id = Database.get_id(book_name.lower())
                    if u_id:
                        if u_id[0] == user_id:
                            pass
                        else:
                            message = pickle.dumps("Return action denied. You did not borrow this book.")
                            length = len(message)
                            client_socket.send(pickle.dumps(length))
                            time.sleep(1)
                            client_socket.send(message)
                            return
                    else:
                        message = pickle.dumps(
                            "None Sorry, your return action was not succesful please try again later.")
                        length = len(message)
                        client_socket.send(pickle.dumps(length))
                        time.sleep(1)
                        client_socket.send(message)
                        return

                    book.return_book()
                    count = 0
                    while count < 3:
                        further = None
                        further = Database.update_borrow_history_r(
                            user_name, user_id, book.returned_time, book.title.lower())
                        if not further:
                            message = pickle.dumps(f"{book.title.capitalize()} successfully returned to library.")
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

def cont():
    while True:
        cont = input("Further?: ")
        if cont.lower() == "yes":
            return True
        elif cont.lower() == "no":
            return False
        else:
            continue

def reset():
    count = 0
    while count < 3:
        fault = Database.reset()
        if not fault:
            break
        count += 1
    else:
        print("Reset failed.")

def delete_table(table):
        if table.lower() == "books":
            books.clear()
        elif table.lower() == "users":
            users.clear()
        Database.delete(table.lower())

delete_table("users")
reset()
load_books()
load_users()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 3001))

server.listen(2)

print("Listening for users.....")

while True:

    client_socket, client_address = server.accept()
    print("Client connected:", client_address)

    if client_address[0] != "127.0.0.1":
        print("This user is not of this device.")
        client_socket.close()
        continue

    client_socket.settimeout(60)

    while True:
            try:
                length = pickle.loads(client_socket.recv(1024))
                if not length:
                    print("message: length data not receivede")
                    continue

                data = pickle.loads(client_socket.recv(length))
                print("Raw received:", data)

            except socket.timeout:
                client_socket.close()
                break

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

                            client_socket.close()
                    else:
                        message = pickle.dumps(
                        "Please sign up first to see library books.")
                        length = len(message)
                        client_socket.send(pickle.dumps("deny"))
                        # time.sleep(1)
                        client_socket.send(pickle.dumps(length))
                        # time.sleep(1)
                        client_socket.send(message)
                        
                        client_socket.close()


                else:
                    message = pickle.dumps(
                    "Sorry your request was disapproved.")
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    time.sleep(1)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

                    client_socket.close()


            elif request.lower() == "borrow":
                title = search[2].group(1)
                user_name = search[1].group(1)
                print(data[9:])
                if approval():
                # pattern = r"\((\d+)\)"
                    user_id = pickle.loads(client_socket.recv(1024))
                # match = re.search(pattern, rev, re.I)
                # user_id = int(match.group(1))
                    if user_id:
                        borrow_book(title, user_name, user_id, client_socket)
                        client_socket.close()

                    else:
                        message = pickle.dumps(
                        "Please signup to access library books.")
                        length = len(message)
                        client_socket.send(pickle.dumps(length))
                        time.sleep(1)
                        client_socket.send(message)

                        client_socket.close()
                else:
                    message = pickle.dumps(
                    "Sorry, your request was denied.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

                    client_socket.close()

            elif request.lower() == "signup":
                print("A user wants to sign up")
                if approval():
                    text = data[9:]
                    pattern = r"\(([^,]+),([^,]+),([^,]+),([^,]+)\)"
                    search = re.search(pattern, text, re.I)
                    if search:
                        add_user(search.group(1), search.group(
                        2), search.group(3), search.group(4), client_socket)
                        client_socket.close()

                    else:
                        client_socket.send(pickle.dumps("nr"))
                        message = pickle.dumps(
                        "Your sign up info was not received. Please try again.")
                        length = len(message)
                        client_socket.send(pickle.dumps(length))
                        time.sleep(1)
                        client_socket.send(message)
                        client_socket.close()

                else:
                    client_socket.send(pickle.dumps("de"))
                    message = pickle.dumps(
                    "Sorry, your request was denied.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

                    client_socket.close()

            elif request.lower() == "return":
                title = search[2].group(1)
                user_name = search[1].group(1)
                print(data[9:])
                if approval():
                # pattern = r"\((\d+)\)"
                # rev = client_socket.recv(10).decode("utf-8")
                # match = re.search(pattern, rev, re.I)
                    user_id = pickle.loads(client_socket.recv(1024))
                    if user_id:
                        return_book(title, user_name, user_id, client_socket)
                        client_socket.close()
                    else:
                        message = pickle.dumps(
                        "Please signup to access library books.")
                        length = len(message)
                        client_socket.send(pickle.dumps(length))
                        time.sleep(1)
                        client_socket.send(message)

                        client_socket.close()

                else:
                    message = pickle.dumps(
                    "Sorry, your request was denied.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    time.sleep(1)
                    client_socket.send(message)

                    client_socket.close()
            else:
                break
            break
