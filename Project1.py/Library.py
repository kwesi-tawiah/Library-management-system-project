import Books

import Database

import socket

import threading


class Library:

    def load_books(self):
        count = 0
        while count < 2:
            books, fault = None, None
            books, fault = Database.load_books()
            if books and not fault:
                if self.books:
                    for b in books: # the first fix is herre for b in bookes
                        for book in self.books:
                            if book.title.lower() == b[1].lower() and book.author.lower() == b[3].lower():
                                break
                        else:
                            book = Books.Book(b[1], b[2], b[3], b[4])
                            book.id = b[0]
                            if b[5].lower() == "yes":
                                book.borrowed = True
                            elif b[5].lower() == "no":
                                book.borrowed = False
                                self.books.append(book)
                else:
                    for b in books: # also here for b in bookes must refer to the fetched data
                        book = Books.Book(b[1], b[2], b[3], b[4])
                        book.id = b[0]
                        if b[5].lower() == "yes":
                            book.borrowed = True
                        elif b[5].lower() == "no":
                            book.borrowed = False
                        self.books.append(book)

                break
            elif not books and not fault:
                print("There are no book in library.")
                break
            elif not books and fault:
                continue
            count += 1
        else:
            print("There are no books in library.")

    def load_users(self):
        count = 0
        while count < 2:
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
        self.create_tables()
        self.load_books()
        self.load_users()

    def delete_table(self, table):
        if table.lower() == "books":
            self.books.clear()
        elif table.lower() == "users":
            self.users.clear()
        Database.delete(table)

    def add_book(self, title, year, author, borrow_time):
        if self.books:
            for book in self.books:
                if book.title == title and book.year == year and book.author == author:
                    print("This book is already in library.")
                    break
            else:
                _id = Database.insert_into_books(
                    title, year, author, borrow_time)
                if not _id:
                    print("This book is already in library.")
                else:
                    book = Books.Book(title, year, author, borrow_time)
                    book.id = _id
                    self.books.append(book)
                    print("Book added to library.")
        else:
            book = Books.Book(title, year, author, borrow_time)
            _id = Database.insert_into_books(
                title, year, author, borrow_time)
            book.id = _id
            self.books.append(book)
            print("Book added to library.")

    def show_books(self):
        if not self.books:
            count = 0
            while count < 1:
                data, fault = None, None
                data, fault = Database.show_table("books")
                if not data and not fault:
                    print("There are no books in the library.")
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
                print(f"Book_id: {book.id}", sep="")
                book.book_state()

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

def notifications():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 8080))

        while True:

            client.send("Update".encode("utf-8"))

            message = client.recv(20).decode("utf-8")

            if message.lower() == "new user":
                librarian.load_users()
                continue

            elif message.lower() == "borrow":
                message = client.recv(1024).decode("utf-8")
                if message:
                    print(message)
                continue

            elif message.lower() == "return":
                message = client.recv(1024).decode("utf-8")
                if message:
                    print(message)
                continue

            else:
                continue

librarian = Library()

#librarian.delete_table("users")
#librarian.delete_table("books")

print("Shown!")
librarian.show_books()
print("Shown!")

#librarian.add_book("Physics", "1990", "Bruce", 2)
#librarian.add_book("Chemistry", "2020", "Chris", 3)
#librarian.add_book("Mathematics", "1919", "Adjoa", 1)

#print("Shown!")
#librarian.show_books()
#print("Shown!")


# librarian.delete_table("borrow_history")

librarian.add_book("Physics", "1990", "Bruce", 2)
librarian.add_book("Chemistry", "2020", "Chris", 3)
librarian.add_book("Mathematics", "1919", "Adjoa", 1)

print("Shown!")
librarian.show_books()
print("Shown!")

Thread = threading.Thread(target = notifications, daemon = True)
Thread.start()
